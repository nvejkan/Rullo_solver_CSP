# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:14:44 2018

@author: Nattawut Vejkanchana
"""

from csp import *
from copy import deepcopy
from datetime import timedelta, date , datetime
import numpy as np
from itertools import combinations,product

class RulloCSP(CSP):
    """Make a CSP for the Rullo game
    			
    """

    def __init__(self,m,row_sum,col_sum):
        """Call the super class
        Pass possible_values to domains
        Pass None to neighbors
        Pass None to constraint function
        """
        
        
        self.m = m #the game matrix
        self.game_dim = m.shape[0]
        self.row_sum = row_sum
        self.col_sum = col_sum
        
        possible_values = self.get_possible_values(m,row_sum,col_sum)
        var = list(possible_values.keys())
        
        CSP.__init__(self,var, possible_values, None,
               None)
        #just for checking the performance
        self.assign_count = 0
        
    def get_indices_eq_sum(self,arr,target):
        #arr = [3, 4, 2, 3, 2]
        all_index_list = []
        for l in range(1,len(arr)+1):
            indices = set([i for i in combinations(range(len(arr)), l)])
            for ind in indices:
                sum = 0
                for n in ind:
                    sum += arr[n]
                if sum == target:
                    all_index_list.append(ind)
                    
        if len(all_index_list) == 0:
            all_index_list = [()] #just assign a None tuple
    
        return all_index_list
    
    def get_possible_values(self,m,row_sum,col_sum):
        ret_dict = dict()
        #insert possible values to the dict
        for i in range(len(row_sum)):
            ret_dict['r{0}'.format(i)] = self.get_indices_eq_sum(m[i,:],row_sum[i])
            ret_dict['c{0}'.format(i)] = self.get_indices_eq_sum(m[:,i],col_sum[i])
    
        return ret_dict
    
    def assign(self, var, val, assignment,wanted_dict,unwanted_dict):
        """Add {var: val} to assignment; Discard the old value if any."""
        
        print("Assign")
        print(assignment)
#        print("wanted dict", wanted_dict)
#        print("unwanted dict", unwanted_dict)
        
        assignment[var] = val
        
        self.nassigns += 1
        
        #modify wanted and unwanted dict
        add_dynamic_constraints(var,val,wanted_dict,unwanted_dict,self.game_dim)   
            
        print("Assign after:")
        print(assignment)
        print("---------------------------------------------------")
        #record assign times
        self.assign_count = self.assign_count+1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]   
    
    def choices(self, var):
        return self.domains.get(var)
    
    def nconflicts(self, var, val, assignment,wanted_dict,unwanted_dict):
        """Return the number of conflicts var=val has with other variables."""
        
        count_unwanted = 0
        count_violate_wanted = 0
        
        #unwanted 
        unwanted_list = unwanted_dict.get(var)
        if not unwanted_list is None:
            for u in unwanted_list:
                if u in val:
                    count_unwanted += 1
        
        #wanted
        wanted_list = wanted_dict.get(var)
        if not wanted_list is None:
            for w in wanted_list:
                if not w in val:
                    count_violate_wanted += 1
            
        return count_unwanted + count_violate_wanted
        
def add_dynamic_constraints(var,val,wanted_dict, unwanted_dict,dim):
    """
    var = variable name e.g. c0
    val = assigned values e.g. () or (0,1,2)
    
    if c0 == ()
    then r0,r1,r2,r3,r4 cannot contains 0
    
    if r0 == (0,1,2)
    then c0,c1,c2 must have 0
        and c3,c4 must never have 0
    """
    
    #set row or col constraints
    if 'c' in var:
        target_const = 'r'
    else:
        target_const = 'c'
    
    #set constraint value
    const_val = int(var[1:]) #c0 => 0
        
    #set indexes to be constrained 
    if val == ():
        unwanted_n = list(range(0,dim)) #if 5*5 dim = 5
        wanted_n = []
    else:
        #e.g. val = (0,1,2)
        wanted_n = list(val) # [0,1,2]
        unwanted_n = list(set(range(0,dim)) - set(val)) #[3,4]
    
    key_temp = "{0}{1}"
    for w in wanted_n:
        key_i = key_temp.format(target_const,w)
        old_list = wanted_dict.get(key_i)
        if old_list is None:
            wanted_dict[key_i] = [const_val]
        else:
            old_list.append(const_val)
            wanted_dict[key_i] = old_list
    
    for w in unwanted_n:
        key_i = key_temp.format(target_const,w)
        old_list = unwanted_dict.get(key_i)
        if old_list is None:
            unwanted_dict[key_i] = [const_val]
        else:
            old_list.append(const_val)
            unwanted_dict[key_i] = old_list
    
    #return wanted_dict,unwanted_dict
    
def rullo_mrv(assignment, csp,wanted_dict,unwanted_dict):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie(
        [v for v in csp.variables if v not in assignment],
        key=lambda var: rullo_num_legal_values(csp, var, assignment,wanted_dict,unwanted_dict))


def rullo_num_legal_values(csp, var, assignment,wanted_dict,unwanted_dict):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment,wanted_dict,unwanted_dict) == 0
                     for val in csp.domains[var])
        
def backtracking_search(csp,
                        select_unassigned_variable=rullo_mrv,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference,
                        wanted_dict=None,
                        unwanted_dict=None):
    """[Figure 6.5]"""

    def backtrack(assignment,wanted_dict,unwanted_dict):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp,wanted_dict,unwanted_dict)
        wanted_dict_bk = deepcopy(wanted_dict)
        unwanted_dict_bk = deepcopy(unwanted_dict)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment,wanted_dict,unwanted_dict):
                csp.assign(var, value, assignment,wanted_dict,unwanted_dict)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment,wanted_dict,unwanted_dict)
                if result is not None:
                    return result
                csp.restore(removals)
                #reset constraints
                wanted_dict = deepcopy(wanted_dict_bk)
                unwanted_dict = deepcopy(unwanted_dict_bk)
                #print("new quota", quota)
        csp.unassign(var, assignment)
        return None

    result = backtrack({},wanted_dict,unwanted_dict)
    #assert result is None or csp.goal_test(result)
    print("assign count:",csp.assign_count)
    return result

def pretty_print(result,m,row_sum,col_sum):
    dim = int(len(result.keys())/2)
    result_matrix =  np.zeros((dim,dim), np.int32)
    for r in range(0,dim):
        for c in range(0,dim):
            if c in result.get('r{0}'.format(r)):
                result_matrix[r,c] = m[r,c]
                
    from pandas import DataFrame
    df = DataFrame(result_matrix,columns=col_sum,index = row_sum)
    print(df)
    return df
    
    

#test
#init dynamic constraints
#w,u = add_dynamic_constraints('r0',(0,1,2),w, u,5)   

#USER INPUT
m = np.array([[3, 4, 2, 3, 2],
              [2, 3, 2, 4, 3],
              [3, 2, 3, 2, 4],
              [4, 4, 2, 2, 4],
              [2, 4, 3, 3, 3],], np.int32)

row_sum = [6,9,11,8,10]
col_sum = [0,13,7,11,13]

m = np.array([[2, 4, 4, 3, 2],
              [3, 3, 2, 3, 4],
              [3, 2, 4, 2, 3],
              [3, 3, 4, 2, 2],
              [2, 3, 2, 2, 2],], np.int32)

row_sum = [5,9,11,12,4]
col_sum = [8,8,10,10,5]

#8*8
m = np.array([[2, 3, 4, 2, 3, 3, 2, 4],
              [2, 3, 3, 3, 3, 4, 3, 2],
              [2, 2, 4, 4, 3, 3, 3, 3],
              [2, 2, 2, 4, 4, 2, 2, 2],
              [3, 3, 2, 4, 4, 3, 3, 2],
              [3, 2, 4, 3, 3, 4, 3, 4],
              [3, 4, 3, 3, 3, 4, 4, 3],
              [3, 3, 2, 2, 3, 3, 4, 2],], np.int32)

row_sum = [20,15,19,14,18,19,21,17]
col_sum = [18,19,19,19,12,22,16,18]



#code start
unwanted_dict = dict()
wanted_dict = dict()
r_csp = RulloCSP(m,row_sum,col_sum)

result = backtracking_search(r_csp,
                              wanted_dict = wanted_dict,
                              unwanted_dict = unwanted_dict)
ret_df= pretty_print(result,m,row_sum,col_sum)
    