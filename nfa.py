#!/usr/bin/env python
"""
   Copyright 2012 Brian Hong (serialx.net@gmail.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   epsilon-move Nondeterministic Finite Automation implementation.
"""

import sys
import pprint
from collections import defaultdict

from dfa import DFA


class NFA(object):
    """
    epsilon-move NFA
    alphabet '' is epsilon.
    """
    def __init__(self, states, alphabet, transition_function, start_state,
            accept_states):
        self.states = set(states)
        assert len(self.states) == len(states)
        self.alphabet = set(alphabet)
        assert len(self.alphabet) == len(alphabet)
        self.transition_function = set(transition_function)
        assert len(self.transition_function) == len(transition_function)
        self.start_state = start_state
        assert start_state in states
        self.accept_states = set(accept_states)
        assert self.states.issuperset(accept_states)
        trans_dict = dict()  #defaultdict(lambda: defaultdict(set))
        for ((q1, c), r2) in self.transition_function:
            if q1 not in trans_dict:
                trans_dict[q1] = dict()
            if c not in trans_dict[q1]:
                trans_dict[q1][c] = set()
            trans_dict[q1][c].add(r2)
        self.trans_dict = trans_dict

    def __unicode__(self):
        format_str = (u"NFA(states={0}, \n    alphabet={1}, \n    "
                "transition_function={2}, \n    start_state={3}, \n    "
                "accept_state={4})")
        return format_str.format(self.states, self.alphabet,
            self.transition_function, self.start_state, self.accept_states)

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def transitions(self, states, c):
        target_states = set()
        for state in states:
            if state in self.trans_dict and c in self.trans_dict[state]:
                target_states |= self.trans_dict[state][c]
        return frozenset(target_states)

    def epsilon_closure(self, states, visited_states=None):
        #print("epsilon_closure({0}, {1})".format(states, visited_states))
        if not visited_states:
            visited_states = set()
        visited_states |= states

        target_states = set()
        for state in states:
            if state in self.trans_dict and '' in self.trans_dict[state]:
                target_states |= self.trans_dict[state]['']
        new_states = target_states - visited_states
        visited_states = set(visited_states)  # Copy
        for new_state in new_states:
            visited_states |= self.epsilon_closure({new_state}, visited_states)
        return frozenset(visited_states)

    def to_dfa(self):
        pre_start_state = {self.start_state}
        e_trans = dict()
        e_states = list()
        accept_e_states = set()
        new_e_states = list()
        start_e_state = self.epsilon_closure(pre_start_state)
        #print("start_e_state: {0}".format(start_e_state))
        new_e_states.append(start_e_state)

        # Start state can be also accept state
        for state in start_e_state:
            if state in self.accept_states:
                accept_e_states.add(start_e_state)

        while new_e_states:
            e_state = new_e_states.pop(0)
            e_states.append(e_state)
            for c in self.alphabet:
                if len(c) == 0: continue
                target_states = self.transitions(e_state, c)
                if not target_states: continue
                new_e_state = self.epsilon_closure(target_states)
                #print("{0}, {1} -> {2}".format(e_state, c, new_e_state))
                e_trans[(e_state, c)] = new_e_state
                if (new_e_state not in e_states) and (new_e_state not in new_e_states):
                    new_e_states.append(new_e_state)
                    for state in new_e_state:
                        if state in self.accept_states:
                            accept_e_states.add(new_e_state)

        return DFA(e_states, self.alphabet - {''}, e_trans.items(), start_e_state, accept_e_states)
        #print("e_states: {0}".format(e_states))
        #print("e_trans: {0}".format(e_trans))
        #print("start_e_state: {0}".format(start_e_state))
        #print("accept_e_states: {0}".format(accept_e_states))
        new_name = dict()
        new_trans = dict()
        for i, e_state in enumerate(e_states):
            new_name[e_state] = i + 1
        #print("new_name: {0}".format(pprint.pformat(new_name)))
        for (e_state, c), target_e_state in e_trans.items():
            new_trans[(new_name[e_state], c)] = new_name[target_e_state]
        new_states = set(new_name.values())
        new_start_state = new_name[start_e_state]
        new_accept_states = {new_name[accept_e_state] for accept_e_state in accept_e_states}
        #print("new_states: {0}".format(new_states))
        #print("new_start_state: {0}".format(new_start_state))
        #print("new_trans: {0}".format(new_trans))
        #print("new_accept_states: {0}".format(new_accept_states))

        return DFA(new_states, self.alphabet - {''}, new_trans.items(), new_start_state, new_accept_states)


def test_simple_nfa():
    states = set(range(1, 14))  # 1..13
    alphabet = {'0', '1', ''}
    transition_function = {
            ((1, ''), 2),
            ((1, ''), 8),
            ((2, ''), 3),
            ((2, ''), 4),
            ((3, '0'), 5),
            ((4, '1'), 6),
            ((5, ''), 7),
            ((6, ''), 7),
            ((7, ''), 2),
            ((7, ''), 8),
            ((8, '0'), 9),
            ((9, '1'), 10),
            ((10, '1'), 11),
            ((11, '0'), 12),
            ((12, '1'), 13),
            }
    start_state = 1
    accept_states = {13}
    d = NFA(states, alphabet, transition_function, start_state, accept_states)
    print(d)
    print(d.to_dfa())
    print(d.to_dfa().minimize())
    #print('"abc" in d = {0}'.format('abc' in d))
    #print('"acd" in d = {0}'.format('acd' in d))


if __name__ == '__main__':
    #test_simple_nfa()
    input = eval(open('input_nfa.txt').read())
    d = NFA(*input)
    print("= NFA =")
    print(d)
    print("(+) Converting to DFA...")
    d = d.to_dfa()
    print("")
    print("= DFA =")
    print(d)
    print("(+) Renaming states...")
    d = d.rename()
    print("")
    print("= Renamed DFA =")
    print(d)
    print("(+) Computing mDFA...")
    d = d.minimize().rename()
    print("")
    print("= mDFA =")
    print(d)
    print("")
    print("= Output (As per homework specs) =")
    print("state = {{{0}}}".format(", ".join(str(x) for x in d.states)))
    print("final_state = {{{0}}}".format(", ".join(str(x) for x in d.accept_states)))
    print("start_state = {0}".format(d.start_state))
    for ((s, c), _d) in d.transition_function:
        print("({0}, {1}, {2})".format(s, _d, c))
    print("")
    print("= Test =")
    while True:
        l = sys.stdin.readline().strip()
        print('"{0}" in DFA = {1}'.format(l, l in d))

