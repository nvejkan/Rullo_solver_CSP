#	  |	0	13	7	11	13  
#	  |------------------------
#	6 |	3	4	2	3	2
#	9 |	2	3	2	4	3
#	11|	3	2	3	2	4
#	8 |	4	4	2	2	4
#	10|	2	4	3	3	3	

import numpy as np
from itertools import combinations,product

#m (problem) must be a square matrix

def get_indices_eq_sum(arr,target):
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

def get_possible_values(m,row_sum,col_sum):
    ret_dict = dict()
    #insert possible values to the dict
    for i in range(len(row_sum)):
        ret_dict['r{0}'.format(i)] = get_indices_eq_sum(m[i,:],row_sum[i])
        ret_dict['c{0}'.format(i)] = get_indices_eq_sum(m[:,i],col_sum[i])

    return ret_dict

m = np.array([[3, 4, 2, 3, 2],
              [2, 3, 2, 4, 3],
              [3, 2, 3, 2, 4],
              [4, 4, 2, 2, 4],
              [2, 4, 3, 3, 3],], np.int32)

row_sum = [6,9,11,8,10]
col_sum = [0,13,7,11,13]

pos_val = get_possible_values(m,row_sum,col_sum)







