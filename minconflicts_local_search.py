import sys
import math
import copy
import random
import datetime


class CSP:

    def __init__(self,vars,domain_values,neighbors):
        self.vars=vars
        self.domain_values=domain_values
        self.neighbors=neighbors

if __name__ == '__main__':

    out_file = ''
    in_file=''


    if (len(sys.argv) == 3):
        in_file=open(sys.argv[1],'r')
        out_file = open(sys.argv[2], 'w')


    else:
        print('Wrong number of arguments. Usage:\n solver.py <INPUT file path> <OUTPUT file path>')
        sys.exit()

    cl = in_file.read().split('\n')


    board=[]
    for i in range(len(cl)-1):
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



max_steps=1000000

def conflicted_select_variable(assignment,csp):
    list1=[]
    for v in csp.vars:
        neigh=csp.neighbors[v]
        for n in neigh:
            if (assignment[v] == assignment[n]):
                list1.append(v)
                break
    return random.choice(list1)

#count generated twice probably
def number_of_conflicted_variables(assignment,csp):
    count=0
    for v in csp.vars:
        neigh=csp.neighbors[v]
        for n in neigh:
            if (assignment[v] == assignment[n]):
                count+=1
                break
    return count



def least_constraining_value(var,assignment,csp):
    orig_assignment=copy.deepcopy(assignment)
    lcv={}#key-domain_value :maintain count of conflicted_variables
    #for an assignment var , temp_value maintaining count of conflicted variables and choosing the minimum count not equal to curr_assignment
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

def min_conflicts(csp,max_steps):
    current_assignment=initial_assignment(csp)
    for i in range(max_steps):
        if(solution(current_assignment,csp)):
            return i,current_assignment
        var=conflicted_select_variable(current_assignment,csp)
        value=least_constraining_value(var,current_assignment,csp)
        assign(var,value,current_assignment)
    return i,current_assignment


start=datetime.datetime.now()
i,solution=min_conflicts(csp,max_steps)
end=datetime.datetime.now()
print((end-start).total_seconds(),i)
if(i>=max_steps-1):
    print("solution not found")
else:
    if solution is not None:
        for i in range(len(solution)):
            j = (solution.get(i))
            out_file.write(str(j) + '\n')

