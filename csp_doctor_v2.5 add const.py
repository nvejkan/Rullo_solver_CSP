# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 21:25:07 2018

@author: nattawutvejkanchana
"""

from csp import *
from copy import deepcopy
from datetime import timedelta, date , datetime


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

    def __init__(self, var, domains,unwanted_dict,wanted_dict):
        """Initialize data structures for n Queens."""
        CSP.__init__(self,var, UniversalDict(domains), create_doctor_neighbors(var),
               different_values_constraint)
        #self.quota_bk = deepcopy(quota)
        #self.quota = deepcopy(quota)
        self.assign_count = 0
        self.unwanted_dict = unwanted_dict
        self.wanted_dict = wanted_dict
        
    def assign(self, var, val, assignment,quota):
        """Add {var: val} to assignment; Discard the old value if any."""
        
        print("Assign")
        print(assignment)
        print(quota)
        
#        if len(assignment) == 0:
#            #reset quota
#            self.quota = deepcopy(self.quota_bk)
        
        assignment[var] = val
        
        self.nassigns += 1
        
        if 'Sat'.upper() in var.upper() or\
        'Sun'.upper() in var.upper() or\
        int(var.split('-')[0]) in p_holidays:
            key_str = "{0}_end".format(val)
            quota[key_str] = quota.get(key_str) - 1
        else:
            key_str = "{0}_day".format(val)
            quota[key_str] = quota.get(key_str) - 1
            
        print("Assign after:")
        print(assignment)
        print(quota)
        print("---------------------------------------------------")
        #record assign times
        self.assign_count = self.assign_count+1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]   
    
    def choices(self, var,quota):
        """Return all values for var that aren't currently ruled out."""
        #return (self.curr_domains or self.domains)[var]
        available_domain = (self.curr_domains or self.domains)[var]
        ret_domain = []
        for d in available_domain:
            if 'Sat'.upper() in var.upper() or 'Sun'.upper() in var.upper()\
            or int(var.split('-')[0]) in p_holidays:
                key_str = "{0}_end".format(d)
                current_quota = quota.get(key_str)
            else:
                key_str = "{0}_day".format(d)
                current_quota = quota.get(key_str)
            if current_quota > 0:
                ret_domain.append(d)
        print("choices of {0}, date type: {1} ".format( var, key_str.split('_')[1] ))
        print(ret_domain)
        return ret_domain
        
        #reset quota
        #self.quota = deepcopy(self.quota_bk)
        
    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        """Doctor csp's version of conflict"""
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        
        var_date = int(var.split('-')[0])
        
        count_unwanted = 0
        count_violate_wanted = 0
        
        if var_date in self.unwanted_dict.get(val):
            count_unwanted = 1
        
        
        #check other wanted date
        for k in self.wanted_dict.keys():
            if k != val and var_date in self.wanted_dict.get(k):
                count_violate_wanted = 1
                break
            
        return count(conflict(v) for v in self.neighbors[var]) + count_unwanted + count_violate_wanted
        
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

def unordered_domain_values(var, assignment, csp,quota):
    """The default value order."""
    return csp.choices(var,quota)

def max_quota_values(var, assignment, csp,quota):
    """The default value order."""
    
    choices = csp.choices(var,quota)
    if 'Sat'.upper() in var.upper() or 'Sun'.upper() in var.upper()\
            or int(var.split('-')[0]) in p_holidays:
                x = [ (quota.get('{0}_end'.format(c)),c) for c in choices ]
    else:
        x = [ (quota.get('{0}_day'.format(c)),c) for c in choices ]
    
    x.sort(reverse = True)
        
    return [ k for (q,k) in x ]

def backtracking_search2(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference,
                        quota=None):
    """[Figure 6.5]"""

    def backtrack(assignment,quota):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        quota_bk = deepcopy(quota)
        for value in order_domain_values(var, assignment, csp,quota):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment,quota)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment,quota)
                if result is not None:
                    return result
                csp.restore(removals)
                #reset quota
                quota = deepcopy(quota_bk)
                print("new quota", quota)
        csp.unassign(var, assignment)
        return None

    result = backtrack({},quota)
    #assert result is None or csp.goal_test(result)
    print("assign count:",csp.assign_count)
    return result

def get_date_list(month):
    date1 = datetime.strptime('{0} {1} 1'.format(datetime.now().year,month),'%Y %b %d')
    date_i = deepcopy(date1)
    
    ret_list = []    
    count_days = 0
    count_holidays = 0 #include SAT,SUN and holidays
        
    
    while date_i.month <= date1.month:
        ret_list.append(date_i.strftime('%d-%a'))
                
        count_days += + 1
        if date_i.strftime('%a').upper() in ['SAT','SUN'] or\
        date_i.day in p_holidays:
            count_holidays += 1
            #print(date_i)

        date_i += timedelta(1)
    
    return ret_list,count_days,count_holidays
        
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
    
def test_result(result):
    d = dict()
    bad_flag = False
    for doc in p_doctors:
        d[doc] = 0
    for k in result.keys():
        val = result.get(k)
        d[val] = d.get(val) + 1
        
        var_date = int(k.split('-')[0])
        #unwanted dates check
        if var_date in unwanted_dict.get(val):
            print("Fail unwanted date:",k,val)
            bad_flag = True
        #check other wanted date
        for k_want in wanted_dict.keys():
            if k_want != val and var_date in wanted_dict.get(k_want):
                print("Fail wanted date:",k,val)
                bad_flag = True
    if not bad_flag:
        print("\n***************** All constraints are satisfied :) *****************\n")
    return d

def pretty_print(result):
    k = list(result.keys())
    k.sort()
    print("Final result:")
    for i in k:
        var_date = int(i.split('-')[0])
        if var_date in p_holidays:
            is_holiday = "(holiday)"
        else:
            is_holiday = " "*9
        print("{0} {1}:{2}".format(i,is_holiday,result.get(i)))
    
#User input
p_month = 'APR'
#p_holidays = [6,12,16]
p_holidays = [6,12,13,16]

p_doctors = ['A','B','C','D']
# (weekday,weekend)
quota = {'A_day':4, 'B_day':4, 'C_day':4, 'D_day':5
, 'A_end':4, 'B_end':3, 'C_end':3, 'D_end':3}

unwanted_dict = {'A':[3,4,9,11,18,19,20]
                ,'B':[24,26,27,29]
                ,'C':[1,2,5,12,13,14,16]
                ,'D':[]}
                
wanted_dict = {'A':[2,5,7]
                ,'B':[1,12,18]
                ,'C':[3,6,8,30]
                ,'D':[]}

#auto init vars and domains
var,no_days,no_holidays = get_date_list(p_month)
domains = p_doctors

neighbors = create_doctor_neighbors(var)

#Start solving
dc = DoctorCSP(var,domains,unwanted_dict,wanted_dict)

#result = backtracking_search2(dc,
#                              select_unassigned_variable = mrv,
#                              order_domain_values = max_quota_values,
#                              quota = quota) #assign count: 4578

                              
#result = backtracking_search2(dc,
#                              select_unassigned_variable = mrv,
#                              quota = quota) #assign count: 699                    
                              

result = backtracking_search2(dc,
                              select_unassigned_variable = mrv,
                              order_domain_values = max_quota_values,
                              inference=mac,
                              quota = quota) #assign count: 138   

test_result(result)
pretty_print(result)                              