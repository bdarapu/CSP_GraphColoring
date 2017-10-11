#dfsb_onlyac3 working for easy inputs given by instructor

import sys
import math
import copy
#sys.setrecursionlimit(1500)

class CSP:

    def __init__(self,vars,domain_values,neighbors):
        self.vars=vars
        self.domain_values=domain_values
        self.neighbors=neighbors



if __name__ == '__main__':

    out_file = ''
    in_file=''
    global mode

    if len(sys.argv) == 3:
        in_file=open(sys.argv[1],'r')
        out_file = open(sys.argv[2], 'w')
        #mode=sys.argv[3]


    else:
        print('Wrong number of arguments. Usage:\npuzzleSOlver.py <N-1 or 2> <K - 3 0r 4> <INPUT file path> <OUTPUT file path>')
    #print('n = ' + str(n))


    cl = in_file.read().split('\n')
    #print (cl)
    board=[]
    for i in range(len(cl) - 1):
        y = (cl[i].split('\t'))
        board.append(y)
    #print (board)
    #print(board[0])
    #print(board[0][0],board[0][1],board[0][2])
    var=int(board[0][0])
    num_constraints=int(board[0][1])
    num_domain=int(board[0][2])
    vars=[]
    for i in range(var):
        vars.append(i)
    #print(vars)



    domain_values={}
    for i in range(var):
        domain_values[i]=[]

    for i in range (var):
        for j in range (num_domain):
            domain_values[i].append(j)
    #print(domain_values)


    constraints=[]
    for i in range(1,len(board)):
        constr=[]
        constr.append(int(board[i][0]))
        constr.append(int(board[i][1]))
        constraints.append(constr)
    #print(constraints)

    neighbors={}
    for i in range(var):
        neighbors[i]=[]

    for l in constraints:
        neighbors[l[0]].append(l[1])
        neighbors[l[1]].append(l[0])
    #print (neighbors)

    csp=CSP(vars,domain_values,neighbors)

    # print(csp.vars)
    # print(csp.domain_values)
    # print(csp.neighbors)

#print("mode is", mode)
def backtracking_search(csp):
    return backtrack({},csp)

def select_unassigned_variable(assignment,csp):

    min_count=math.inf
    ret_var=0
    #list_count=[]
    list_var=[]
    for var in csp.vars:    # minimal remaining values
        if var not in assignment:
            count=len(csp.domain_values[var])
            if(count<min_count):
                min_count=count
    for var in csp.vars:    # storing all the vars with min_count values in domain
        if var not in assignment:
            count = len(csp.domain_values[var])
            if(count==min_count):
                list_var.append(var)
    degree_bound_count=-1
    for var in list_var:   # to return maximum degree bounded var
        count=len(csp.neighbors[var])
        if(count>degree_bound_count):
            degree_bound_count=count
            ret_var=var
    return ret_var






def remove(var,assignment):   # do i need to return assignment
    if var in assignment:
        del assignment[var]
    #return assignment

def order_domain_values(var,assignment,csp):
    domain=csp.domain_values[var][:]
    #print (domain)
    return domain

def consistent_assignment(csp,var,value,assignment):
    list=(csp.neighbors).get(var)
    count=0
    #c=0
    for l in list:
        x=assignment.get(l)
        if(x!=value):
            count+=1
    if(len(list)==count):
        return 0
    else:
        return -1

def assign(var,value,assignment,csp):
    assignment[var]=value
    #return assignment

def Ac3(csp,list_ac3):
    while(len(list_ac3)!=0):
        top_element=[]
        top_element=list_ac3[0]
        list_ac3.remove(top_element)
        if revise(csp,top_element):
            if(len(csp.domain_values[top_element[0]])==0):
                return False
            neigh_xi=csp.neighbors[top_element[0]]
            for xk in neigh_xi:
                if(xk!=top_element[1]):
                    list_ac3.add(xk,top_element[0])
    return True

def revise(csp,top_element):
    revised=False
    #for value in csp.domain_values[top_element[0]]: check later if its correct
    if(len(csp.domain_values[top_element[1]])==1):
        csp.domain_values[top_element[0]].remove(csp.domain_values[top_element[1]])
        revised=True
    return revised



#print(csp.neighbors.get(0))

def backtrack(assignment,csp):
    #print("mode in else :" , mode)
    if (len(assignment) == len(csp.vars)):
        return assignment
    var=select_unassigned_variable(assignment,csp)
    #print("selecting variable :" , var)
    domain=order_domain_values(var,assignment,csp) #gets the domain of the variable
    #print("domain of var is :" , var ,domain )
    neigh_var=csp.neighbors[var]
    #print("neighboring values ", neigh_var)
    lcv={}    #least constraining value dictionary
    for i in range(len(domain)):
        lcv[i]=0  # initialising count of the value in domain to zero
    #print("lcv_test" ,lcv)
    for n in neigh_var:
        for value in domain:
            if(value in csp.domain_values[n]):
                lcv[value]=lcv[value]+1
    #print("lcv is ", lcv) # a dict which keeps count of the number of times these domain values appear in neighbor's domain

    sorted_domain=sorted(lcv,key=lcv.get) # returns the list of keys based on their values;dict={0:2 ,1:3 , 4:1 ,5:8} -[4, 0, 1, 5]
    #print(sorted_domain)
    csp_orig = copy.deepcopy(csp)  #hit and trial
    print ("in backtrack",csp_orig.domain_values)
    for value in sorted_domain:
        print("test")
        if consistent_assignment(csp,var,value,assignment)==0:
            #assignment=assign(var,value,assignment,csp)
            assign(var, value, assignment, csp)
            print("assignment is",assignment)
            list_ac3=[]
            for v in csp.neighbors[var]:
                if v not in assignment:
                    list_ac3.append([v,var])  # append xj,xi
            #csp_orig=copy.deepcopy(csp)      #to remove inference from assignment - trying here
            inferences=Ac3(csp,list_ac3)
            if(inferences==True):
                result=backtrack(assignment,csp)
                if result is not None:
                    return result
        #assignment = remove(var,assignment) # did not remove inferences from assignment - checkpoint
        remove(var, assignment)
        csp=copy.deepcopy(csp_orig)   #hit and trialoogle
    #print("returning none from here")
    return None



print("result is",backtracking_search(csp))
'''solution=backtracking_search(csp)
for i in range(len(solution)):
    j=(solution.get(i))
    out_file.write(str(j)+'\n')
#assignment={0:1,1:3,2:0,6:1}
#assignment[4]=2
#print (assignment)
#order_domain_values(6,assignment,csp)
#select_unassigned_variable(assignment,csp)'''

