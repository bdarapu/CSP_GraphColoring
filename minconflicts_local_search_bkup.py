#min_conflicts working for all easy and hard given by instructor 
import sys
import math
import copy
import random


class CSP:

    def __init__(self,vars,domain_values,neighbors):
        self.vars=vars
        self.domain_values=domain_values
        self.neighbors=neighbors

if __name__ == '__main__':

    out_file = ''
    in_file=''
    #mode = int(sys.argv[1])

    if (len(sys.argv) == 3):
        in_file=open(sys.argv[1],'r')
        out_file = open(sys.argv[2], 'w')
        #mode=int(sys.argv[1])

    else:
        print('Wrong number of arguments. Usage:\n solver.py <INPUT file path> <OUTPUT file path>')
        sys.exit()

    cl = in_file.read().split('\n')
    #print("number of lines",cl)

    board=[]
    for i in range(len(cl)-1):
        y = (cl[i].split('\t'))
        board.append(y)
    #print("lenght of board",len(board))
    #print("board is", board)

    var=int(board[0][0])
    #print("number of variables",var)
    num_constraints=int(board[0][1])
    #print("number of  constraints",num_constraints)
    num_domain=int(board[0][2])
    #print("num_domain ",num_domain)

    vars=[]
    for i in range(var):
        vars.append(i)
    #print("list of vars ", vars)

    domain_values={}
    for i in range(var):
        domain_values[i]=[]


    for i in range (var):
        for j in range (num_domain):
            domain_values[i].append(j)
    #print("list of domian values", domain_values)

    constraints=[]
    #print("length of board", len(board))
    for i in range(1,len(board)):
        constr=[]
        #print("board[i][0]",board[i][0])
        constr.append(int(board[i][0]))
        constr.append(int(board[i][1]))
        constraints.append(constr)
    #print("constraints ",constraints)


    neighbors={}
    for i in range(var):
        neighbors[i]=[]

    for l in constraints:
        neighbors[l[0]].append(l[1])
        neighbors[l[1]].append(l[0])


    csp=CSP(vars,domain_values,neighbors)
    #print("variables in csp",csp.vars)


max_steps=100
#assignment={}

#selection should be from conflicted(csp)
def conflicted_select_variable(assignment,csp):
    list1=[]
    for v in csp.vars:
        neigh=csp.neighbors[v]
        for n in neigh:
            if (assignment[v] == assignment[n]):
                list1.append(v)
                break
    print("conflicted variable set",list1)
    return random.choice(list1)

#count generated twice probably
def number_of_conflicted_variables(assignment,csp):
    #list1=[]
    count=0
    for v in csp.vars:
        neigh=csp.neighbors[v]
        for n in neigh:
            if (assignment[v] == assignment[n]):
                count+=1
                break
    return count
    #print("conflicted variable set",list1)
    #return random.choice(list1)


def least_constraining_value(var,assignment,csp):
    orig_assignment=copy.deepcopy(assignment)
    lcv={}#key-domain_value :maintain count of conflicted_variables
    #current_value=assignment[var] next random choice will be a diffrent one- need not check for current_value!=temp_value
    for i in range(len(csp.domain_values[var])):
        lcv[i] = 0
    for i in range(len(csp.domain_values[var])):
        temp_value=csp.domain_values[var][i]
        assign(var,temp_value,assignment)
        count=number_of_conflicted_variables(assignment,csp)
        lcv[i]=count
    sorted_count = sorted(lcv, key=lcv.get)
    assignment = orig_assignment
    for i in range(len(sorted_count)):
        if (assignment[var] != sorted_count[i]):
            return sorted_count[i]

    #return sorted_count[0]  #returning first one -if two counts are same , can be chosen randomly




def assign(var,value,assignment):
    assignment[var]=value

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

def initial_assignment(csp):
    current_assignment={}
    for v in csp.vars:
        current_assignment[v]=random.randrange(num_domain)
    return current_assignment

def solution(assignment,csp):
    count=0
    for v in csp.vars:
        neigh=csp.neighbors[v]
        for n in neigh:
            if(assignment[n]==assignment[v]):
                count+=1
    if(count==0): return True
    else: return False

#print (initial_assignment(csp))
#print (conflicted_select_variable(initial_assignment(csp),csp))

# asn1={0:0,1:0,2:2,3:0,4:2,5:2,6:1,7:1}
# print(solution(asn1,csp))

def min_conflicts(csp,max_steps):
    current_assignment=initial_assignment(csp)
    print("initial current assignment",current_assignment)
    for i in range(max_steps):
        if(solution(current_assignment,csp)):
            print("solution reached")
            return i,current_assignment
        var=conflicted_select_variable(current_assignment,csp)
        print("conflicted variable ",var,"at step",i)
        value=least_constraining_value(var,current_assignment,csp)
        print("value chosen ", value, "at step", i)
        assign(var,value,current_assignment)
        print("current_assignment is ", current_assignment)
    return i,current_assignment



i,assignment=min_conflicts(csp,max_steps)
if(i>=max_steps-1):
    print("solution not found")
else:
    print("solution found ",assignment,"at i",i)
#print(min_conflicts(csp,assignment))