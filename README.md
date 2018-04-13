This project is mainly leveraged from:

https://github.com/aimacode/aima-python/

I used the CSP algorithm to solve the Rullo game(http://www.coolmath-games.com/0-rullo).
The solver script is csp_rullo_v1.py.

How to use the solver.
1. Go to the USER INPUT section. Input a problem matrix of a game, row sums and column sums.
2. Run these commands:

#code start

>>>unwanted_dict = dict()

>>>wanted_dict = dict()

>>>r_csp = RulloCSP(m,row_sum,col_sum)

>>>result = backtracking_search(r_csp,
                              wanted_dict = wanted_dict,
                              unwanted_dict = unwanted_dict)

>>>ret_df= pretty_print(result,m,row_sum,col_sum)

3. See the result. It can solve any problems perfectly and quickly.

I also created a script to solve doctor scheduling problem using the same CSP algorithm.
See the file: csp_doctor_v2.5 add const.py




