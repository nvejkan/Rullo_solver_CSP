# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 21:25:07 2018

@author: nattawutvejkanchana
"""

from csp import *
from copy import deepcopy
class DoctorCSP(CSP):
    """Make a CSP for the doctor scheduling
    			A_week	A_end	B_week	B_end
    '1-Sat'
    ,'2-Mon'
    ,'3-Tue'
    ,'4-Wed'
    ,'5-Thu'
    ,'6-Fri'
    ,'7-Sun'
    			3		1		2		1
    """

    def __init__(self, var, domains,quota):
        """Initialize data structures for n Queens."""
        CSP.__init__(self,var, UniversalDict(domains), create_doctor_neighbors(var),
               different_values_constraint)
        self.quota_bk = deepcopy(quota)
        self.quota = deepcopy(quota)
        
    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        
        print("Assign")
        print(assignment)
        print(self.quota)
        
#        if len(assignment) == 0:
#            #reset quota
#            self.quota = deepcopy(self.quota_bk)
        
        assignment[var] = val
        
        self.nassigns += 1
        
        if 'Sat'.upper() in var.upper() or 'Sun'.upper() in var.upper():
            key_str = "{0}_end".format(val)
            self.quota[key_str] = self.quota.get(key_str) - 1
        else:
            key_str = "{0}_day".format(val)
            self.quota[key_str] = self.quota.get(key_str) - 1
            
        print("Assign after:")
        print(assignment)
        print(self.quota)

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
#        print("Unassign Before:")
#        print(assignment)
#        print(var)
#        print(self.quota)
#        
#        print("val: " + val)
        if var in assignment:
#            val = assignment.get(var)
#            if 'Sat'.upper() in var.upper() or 'Sun'.upper() in var.upper():
#                key_str = "{0}_end".format(val)
#                self.quota[key_str] = self.quota.get(key_str) + 1
#            else:
#                key_str = "{0}_day".format(val)
#                self.quota[key_str] = self.quota.get(key_str) + 1
            
            del assignment[var]
            
#        print("Unassign After:")
##            print(assignment)
##            print(var)
#        print(self.quota)   
            
    
    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        #return (self.curr_domains or self.domains)[var]
        available_domain = (self.curr_domains or self.domains)[var]
        ret_domain = []
        for d in available_domain:
            if 'Sat'.upper() in var.upper() or 'Sun'.upper() in var.upper():
                key_str = "{0}_end".format(d)
                current_quota = self.quota.get(key_str)
            else:
                key_str = "{0}_day".format(d)
                current_quota = self.quota.get(key_str)
            if current_quota > 0:
                ret_domain.append(d)
        print("choices: "+ var)
        print(ret_domain)
        return ret_domain
    
    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)
        
        #reset quota
        self.quota = deepcopy(self.quota_bk)
        
var = ['1-Sat'
,'2-Mon'
,'3-Tue'
,'4-Wed'
,'5-Thu'
,'6-Fri'
,'7-Sun']

domains = ['A','B']

def create_doctor_neighbors (var):
    neighbors = dict()
    for i in range(0,len(var)):
        if i == 0:
            neighbors[var[i]] = [var[1]]
        elif i == (len(var) - 1):
            #last element
            neighbors[var[i]] = [var[i-1]]
        else:
            neighbors[var[i]] = [var[i-1],var[i+1]]
    return neighbors
    
neighbors = create_doctor_neighbors(var)

# (weekday,weekend)
quota = {'A_day':3, 'A_end':1, 'B_day':2, 'B_end':2 }

def doctor_constraint(A, a, B, b):
    """
    A,B -> var
    a,b -> value
    1. a != b
    2. A's quota > 0
    """
    #flag = True
    if a == b:
        return False
    
        
    
    return a != b

def backtracking_search2(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    #assert result is None or csp.goal_test(result)
    return result
    
dc = DoctorCSP(var,domains,quota)
result = backtracking_search2(dc)