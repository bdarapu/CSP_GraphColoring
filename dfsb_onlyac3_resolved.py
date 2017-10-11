#working only for easy inputs ; need to fix this for backtrack_hard and minconflicts_hard

import sys
import math
import copy


class CSP:

    def __init__(self,vars,domain_values,neighbors):
        self.vars=vars
        self.domain_values=domain_values
        self.neighbors=neighbors



# if __name__ == '__main__':
#
#     out_file = ''
#     in_file=''
#     global mode
#
#     if len(sys.argv) == 3:
#         in_file=open(sys.argv[1],'r')
#         out_file = open(sys.argv[2], 'w')

if __name__ == '__main__':

    out_file = ''
    in_file = ''
    mode = int(sys.argv[1])

    if (len(sys.argv) == 4 and mode in [1, 2]):
        in_file = open(sys.argv[2], 'r')
        out_file = open(sys.argv[3], 'w')
        # mode=int(sys.argv[1])


    else:
        print('Wrong number of arguments. Usage:\npuzzleSOlver.py <N-1 or 2> <K - 3 0r 4> <INPUT file path> <OUTPUT file path>')



    cl = in_file.read().split('\n')

    board=[]
    for i in range(len(cl) - 1):
        y = (cl[i].split('\t'))
        board.append(y)

    var=int(board[0][0])
    num_constraints=int(board[0][1])
    num_domain=int(board[0][2])
    vars=[]
    for i in range(var):
        vars.append(i)

    domain_values={}
    for i in range(var):
        domain_values[i]=[]

    for i in range (var):
        for j in range (num_domain):
            domain_values[i].append(j)

    constraints=[]
    for i in range(1,len(board)):
        constr=[]
        constr.append(int(board[i][0]))
        constr.append(int(board[i][1]))
        constraints.append(constr)

    neighbors={}
    for i in range(var):
        neighbors[i]=[]

    for l in constraints:
        neighbors[l[0]].append(l[1])
        neighbors[l[1]].append(l[0])


    csp=CSP(vars,domain_values,neighbors)


def backtracking_search(csp):
    return backtrack({},csp)

def select_unassigned_variable(assignment,csp):
    list_unassigned=[]
    MRV={}
    for var in csp.vars:
        if var not in assignment:
            list_unassigned.append(var)
    for l in list_unassigned:
        MRV[l]=num_domain
    for l in list_unassigned:
        neigh=csp.neighbors[l]
        for n in neigh:
            if n in assignment:
                MRV[l]=MRV[l]-1
    sorted_mrv=sorted(MRV,key=MRV.get)
    return sorted_mrv[0]
    

def unassign(var,assignment):
    if var in assignment:
        del assignment[var]


def order_domain_values(var,csp):
    domain=csp.domain_values[var][:]
    return domain

def consistent_assignment(csp,var,value,assignment):
    list=(csp.neighbors).get(var)
    count=0
    for l in list:
        x=assignment.get(l)
        if(x!=value):
            count+=1
    if(len(list)==count):
        return 0
    else:
        return -1

def assign(var,value,assignment):
    assignment[var]=value

#runs arc-consistency on xj,xi
def Ac3(csp,list_ac3):

    while(len(list_ac3)!=0):
        top_element=[]
        top_element=list_ac3[0]
        list_ac3.remove(top_element)
        if revise(csp,top_element):
            if(len(csp.domain_values[top_element[0]])==0):  #if domain reduced to zero , return false
                return False
            neigh_xi=csp.neighbors[top_element[0]]
            for xk in neigh_xi:
                if(xk!=top_element[1]):
                    list_ac3.append([xk,top_element[0]])
    return True

def revise(csp,top_element):
    revised=False
    if(len(csp.domain_values[top_element[1]])==1):
        if(csp.domain_values[top_element[1]][0] in csp.domain_values[top_element[0]] ):
            csp.domain_values[top_element[0]].remove(csp.domain_values[top_element[1]][0]) #reducing the domain of some vars -might be the issue
            revised=True
    return revised

def lcv_sorted_domain(assignment,csp,var):
    list_unassigned=[]#unassigned neighboring variables of var
    neigh_var=csp.neighbors[var]
    for v in neigh_var:
        if v not in assignment:
            list_unassigned.append(v)
    #list_unassigned.remove(var)
    print("list_unassigned " , list_unassigned)
    list_unassigned_reduced_domain={} # to get reduced domains of unassigned neighboring variables
    for l in list_unassigned:
        list_unassigned_reduced_domain[l]=[d for d in range(num_domain)]
    for l in list_unassigned:
        neigh_l=csp.neighbors[l]
        for nl in neigh_l:
            if nl in assignment:
                domain_value_remove=assignment[nl]
                if domain_value_remove in list_unassigned_reduced_domain[l]:
                    list_unassigned_reduced_domain[l].remove(domain_value_remove)#remove the value assigned to neighbor form l in list_unassigned
    print("reduced domain",list_unassigned_reduced_domain)
    lcv={}  #least constraining value for var
    for d in csp.domain_values[var]:
        lcv[d]=0
    print("intial lcv",lcv)
    for d in csp.domain_values[var]:
        for l_u_r_d in list_unassigned_reduced_domain:
            if d in list_unassigned_reduced_domain[l_u_r_d]: #if domain_value of var in list_unassigned_reduced_domain
                lcv[d]=lcv[d]+1
    print("lcv is",lcv)
    sorted_domain=sorted(lcv,key=lcv.get)
    return sorted_domain




def backtrack(assignment,csp):

    if (len(assignment) == len(csp.vars)):
        return assignment
    var=select_unassigned_variable(assignment,csp)
    print("selected variable is",var)
    sorted_domain=lcv_sorted_domain(assignment,csp,var)
    print("sorted_domain is",sorted_domain)
    for value in sorted_domain:

        if consistent_assignment(csp,var,value,assignment)==0:
            assign(var, value, assignment)
            print("assignment is", assignment)
            csp.domain_values[var]=[value]
            list_ac3=[]
            orig_csp=copy.deepcopy(csp)
            for v in csp.neighbors[var]:
                if v not in assignment:
                    list_ac3.append([v,var])  # append xj,xi for all neighbours of var that are unassigned
            inferences=Ac3(csp,list_ac3)
            if(inferences==True):
                result=backtrack(assignment,csp)
                if result is not None:
                    return result
            csp = copy.deepcopy(orig_csp)
        unassign(var, assignment)
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

