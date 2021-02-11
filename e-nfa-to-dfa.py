# Author : Vasu Gondaliya
from graphviz import Digraph


class NFA:
    def __init__(self, no_state, states, no_alphabet, alphabets, start, no_final, finals, no_transition, transitions):
        self.no_state = no_state
        self.states = states
        self.no_alphabet = no_alphabet
        self.alphabets = alphabets
        self.alphabets.append('e')
        self.no_alphabet += 1
        self.start = start
        self.no_final = no_final
        self.finals = finals
        self.no_transition = no_transition
        self.transitions = transitions
        self.states_dict = dict()
        for i in range(self.no_state):
            self.states_dict[self.states[i]] = i
        self.alphabets_dict = dict()
        for i in range(self.no_alphabet):
            self.alphabets_dict[self.alphabets[i]] = i
        self.transition_table = dict()
        for i in range(self.no_state):
            for j in range(self.no_alphabet):
                self.transition_table[str(i)+str(j)] = []
        for i in range(self.no_transition):
            self.transition_table[str(self.states_dict[self.transitions[i][0]])+str(
                self.alphabets_dict[self.transitions[i][1]])].append(self.states_dict[self.transitions[i][2]])

    @classmethod
    def fromuser(cls):
        no_state = int(input("Number of States : "))
        states = list(input("States : ").split())
        no_alphabet = int(input("Number of Alphabets : "))
        alphabets = list(input("Alphabets : ").split())
        start = input("Start State : ")
        no_final = int(input("Number of Final States : "))
        finals = list(input("Final States : ").split())
        no_transition = int(input("Number of Transitions : "))
        transitions = list()
        print("Enter Transitions (from alphabet to) (e for epsilon): ")
        for i in range(no_transition):
            transitions.append(input("-> ").split())
        return cls(no_state, states, no_alphabet, alphabets, start, no_final, finals, no_transition, transitions)

    def __repr__(self):
        return "Q : " + str(self.states)+"\nΣ : "+str(self.alphabets)+"\nq0 : "+str(self.start)+"\nF : "+str(self.finals)+"\nδ : \n"+str(self.transition_table)


def e_closure(inp, state):
    closure = dict()
    closure[inp.states_dict[state]] = 0
    closure_arr = [inp.states_dict[state]]
    while(len(closure_arr) > 0):
        cur = closure_arr.pop(0)
        for x in inp.transition_table[str(cur)+str(inp.alphabets_dict['e'])]:
            if x not in closure.keys():
                closure[x] = 0
                closure_arr.append(x)
        closure[cur] = 1
    return closure.keys()


def state_name(state_list, states_dict):
    name = ''
    for x in state_list:
        name += nfa_input.states[x]
    return name


def is_final_dfa(state_list, inp):
    for x in state_list:
        for y in inp.finals:
            if(x == inp.states_dict[y]):
                return True
    return False


print("E-NFA to DFA")
nfa_input = NFA(3, ['s1', 's2', 's3'], 2, ['0', '1'], 's1', 1, ['s3'], 3, [
                ['s1', '0', 's2'], ['s2', '1', 's3'], ['s1', 'e', 's3']])
# nfa_input = NFA.fromuser()
nfa = Digraph()
is_final = dict()
for x in nfa_input.states:
    is_final[x] = 0
nfa.attr('node', shape='doublecircle')
for x in nfa_input.finals:
    nfa.node(x)
    is_final[x] = 1
nfa.attr('node', shape='circle')
for x in nfa_input.states:
    if(is_final[x] == 0):
        nfa.node(x)
nfa.attr('node', shape='none')
nfa.node('')
for x in nfa_input.transitions:
    nfa.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'e'])
nfa.edge('', nfa_input.start)
nfa.render('nfa', view=True)

dfa = Digraph()
dfa.attr('node', shape='none')
dfa.node('')
dfa_states = list()
epsilon_closure = dict()
for x in nfa_input.states:
    epsilon_closure[x] = list(e_closure(nfa_input, x))
dfa_states.append(epsilon_closure[nfa_input.start])
if(is_final_dfa(dfa_states[0], nfa_input)):
    dfa.attr('node', shape='doublecircle')
else:
    dfa.attr('node', shape='circle')
dfa.node(state_name(list(dfa_states[0]), nfa_input.states_dict))
dfa.edge('', state_name(dfa_states[0], nfa_input.states_dict))
dfa_states_exist = list()
dfa_states_exist.append(epsilon_closure[nfa_input.start])
while(len(dfa_states) > 0):
    cur_state = dfa_states.pop(0)
    for al in range((nfa_input.no_alphabet) - 1):
        to_state_mid = set()
        for x in cur_state:
            to_state_mid.update(
                set(nfa_input.transition_table[str(x)+str(al)]))
        if(len(to_state_mid) > 0):
            to_state = set()
            for x in list(to_state_mid):
                to_state.update(set(epsilon_closure[nfa_input.states[x]]))
            if list(to_state) not in dfa_states_exist:
                dfa_states.append(list(to_state))
                dfa_states_exist.append(list(to_state))
                if(is_final_dfa(list(to_state), nfa_input)):
                    dfa.attr('node', shape='doublecircle')
                else:
                    dfa.attr('node', shape='circle')
                dfa.node(state_name(list(to_state), nfa_input.states_dict))
            dfa.edge(state_name(cur_state, nfa_input.states_dict), state_name(
                list(to_state), nfa_input.states_dict), label=nfa_input.alphabets[al])
        else:
            if (-1) not in dfa_states_exist:
                dfa.attr('node', shape='circle')
                dfa.node('ϕ')
                for alpha in range(nfa_input.no_alphabet - 1):
                    dfa.edge('ϕ', 'ϕ', nfa_input.alphabets[alpha])
                dfa_states_exist.append(-1)
            dfa.edge(state_name(cur_state, nfa_input.states_dict),
                     'ϕ', label=nfa_input.alphabets[al])
dfa.render('dfa', view=True)
