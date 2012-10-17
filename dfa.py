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

   Deterministic Finite Automation implementation.
"""

import sys
from collections import defaultdict


class DFA(object):
    """Partial function DFA"""
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
        trans_dict = defaultdict(lambda: defaultdict(set))
        for ((q1, c), r2) in self.transition_function:
            trans_dict[q1][c].add(r2)
        self.trans_dict = trans_dict

    def __unicode__(self):
        format_str = (u"DFA(states={0}, \n    alphabet={1}, \n    "
                "transition_function={2}, \n    start_state={3}, \n    "
                "accept_state={4})")
        return format_str.format(self.states, self.alphabet,
            self.transition_function, self.start_state, self.accept_states)

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def transitions(self, state, c):
        return self.trans_dict[state][c]

    def __contains__(self, string):
        """
        Membership check.
        Usage:
            >> "asdf" in d
            True
        """
        state = self.start_state
        for c in string:
            # For all transitions possible with 'c' and 'state'
            transitions_possible = self.transitions(state, c)
            print("({0}, {1}) --> {2}".format(state, c, transitions_possible))
            if (len(transitions_possible) == 0):
                return False
            assert len(transitions_possible) == 1, ('Nondeterministic '
                    'behaviour not allowed in DFA')
            state = list(transitions_possible)[0]
        if (state in self.accept_states):
            return True

    def _distinguishable(self, table, a, b, visited=None):
        #print "distinguishable", a, b, visited
        if table[a][b] or table[b][a]:
            return True
        if a in self.accept_states and b not in self.accept_states:
            table[a][b] = True
            table[b][a] = True
            return True
        if a not in self.accept_states and b in self.accept_states:
            table[a][b] = True
            table[b][a] = True
            return True
        for c in self.alphabet:
            #print c
            at, = self.transitions(a, c)
            bt, = self.transitions(b, c)
            if at == bt:
                return False
            if visited == None:
                visited = set()
            if (at, bt) in visited:
                return False
            visited.add((a, b))
            if self._distinguishable(table, at, bt, set(visited)):
                #print True
                table[a][b] = True
                table[b][a] = True
                return True
            else:
                pass
                #print False


    def minimize(self):
        """Minimize DFA to mDFA."""
        # Remove unreachable states
        reachable_states = set({self.start_state})
        stack = [self.start_state]
        while stack:
            state = stack.pop()
            for c in self.alphabet:
                reachable_states_from_state = self.transitions(state, c)
                for reachable_state in reachable_states_from_state:
                    if reachable_state not in reachable_states:
                        stack.append(reachable_state)
                        reachable_states.add(reachable_state)
        print "reachable_states =", reachable_states

        # Find distinguishable pairs using table filling method
        s = list(reachable_states)
        table = defaultdict(lambda: defaultdict(lambda: False))
        for i, s1 in enumerate(s[x] for x in range(len(reachable_states))):
            for j, s2 in enumerate(s[x] for x in range(i + 1, len(reachable_states))):
                self._distinguishable(table, s1, s2)
        #print table
        equivalent_state_pairs = set()
        for k, v in table.items():
            for k2, v2 in v.items():
                if not v2:
                    equivalent_state_pairs.add(frozenset([k, k2]))
        print "equivalent_state_pairs =", equivalent_state_pairs

        # Merge equivalent pairs
        merging_state = dict()
        states_to_remove = set()
        for a, b in equivalent_state_pairs:
            if a not in merging_state:
                merging_state[a] = frozenset({a, b})
            if b not in merging_state:
                merging_state[b] = frozenset({a, b})
            merging_state[a] = frozenset(merging_state[a] | {a, b})
            merging_state[b] = frozenset(merging_state[b] | {a, b})
            states_to_remove.add(a)
            states_to_remove.add(b)
        if self.start_state in merging_state:
            new_start_state = merging_state[self.start_state]
        else:
            new_start_state = self.start_state

        # Create new DFA
        new_states = (reachable_states - states_to_remove) | set(frozenset(x) for x in merging_state.values())
        new_trans = set()
        new_accept_states = set()
        for ns in new_states:
            if isinstance(ns, set) or isinstance(ns, frozenset):
                for s in ns:
                    if s in self.accept_states:
                        new_accept_states.add(ns)
            else:
                if ns in self.accept_states:
                    new_accept_states.add(ns)
        for ((s, c), d) in self.transition_function:
            if s in merging_state:
                s = merging_state[s]
            if d in merging_state:
                d = merging_state[d]
            new_trans.add(((s, c), d))
        #print "new_states =", new_states
        #print "new_trans =", new_trans
        #print "new_start_state =", new_start_state
        #print "new_accept_states =", new_accept_states
        return DFA(new_states, self.alphabet, new_trans, new_start_state, new_accept_states)

    def rename(self):
        """Rename DFA states to numeric state names and return new renamed DFA."""
        new_name = dict()
        new_trans = dict()
        for i, state in enumerate(self.states):
            new_name[state] = i + 1
        for (state, c), target_state in self.transition_function:
            new_trans[(new_name[state], c)] = new_name[target_state]
        new_states = set(new_name.values())
        new_start_state = new_name[self.start_state]
        new_accept_states = {new_name[accept_state] for accept_state in self.accept_states}

        return DFA(new_states, self.alphabet - {''}, new_trans.items(), new_start_state, new_accept_states)


def test_simple_dfa():
    states = {'q1', 'q2', 'q3', 'q4'}
    alphabet = {'abcde'}
    transition_function = {
            (('q1', 'a'), 'q2'),
            (('q2', 'b'), 'q3'),
            (('q3', 'c'), 'q4'),
            }
    start_state = 'q1'
    accept_states = {'q4'}
    d = DFA(states, alphabet, transition_function, start_state, accept_states)
    print(d)
    print('"abc" in d = {0}'.format('abc' in d))
    print('"acd" in d = {0}'.format('acd' in d))
    d.minimize()


def test_dfa_minimization():
    states = set('ABCDEFGH')
    alphabet = set('01')
    transition_function = {
            (('A', '0'), 'B'),
            (('A', '1'), 'F'),
            (('B', '0'), 'G'),
            (('B', '1'), 'C'),
            (('C', '0'), 'A'),
            (('C', '1'), 'C'),
            (('D', '0'), 'C'),
            (('D', '1'), 'G'),
            (('E', '0'), 'H'),
            (('E', '1'), 'F'),
            (('F', '0'), 'C'),
            (('F', '1'), 'G'),
            (('G', '0'), 'G'),
            (('G', '1'), 'E'),
            (('H', '0'), 'G'),
            (('H', '1'), 'C'),
            }
    start_state = 'A'
    accept_states = {'C'}
    d = DFA(states, alphabet, transition_function, start_state, accept_states)
    print(d)
    print(d.minimize())


def test_dfa_minimization_equiv_accept_states():
    states = set('ABCDE')
    alphabet = set('01')
    transition_function = {
            (('A', '0'), 'B'),
            (('A', '1'), 'D'),
            (('B', '0'), 'C'),
            (('B', '1'), 'C'),
            (('C', '0'), 'C'),
            (('C', '1'), 'C'),
            (('D', '0'), 'E'),
            (('D', '1'), 'E'),
            (('E', '0'), 'E'),
            (('E', '1'), 'E'),
            }
    start_state = 'A'
    accept_states = {'C', 'E'}
    d = DFA(states, alphabet, transition_function, start_state, accept_states)
    print(d)
    print(d.minimize())


def test_dfa_with_cycle():
    states = {'q1', 'q2', 'q3', 'q4'}
    alphabet = {'abcde'}
    transition_function = {
            (('q1', 'a'), 'q2'),
            (('q2', 'b'), 'q3'),
            (('q3', 'a'), 'q2'),
            (('q3', 'c'), 'q4'),
            }
    start_state = 'q1'
    accept_states = {'q4'}
    d = DFA(states, alphabet, transition_function, start_state, accept_states)
    print(d)
    print('"abc" in d = {0}'.format('abc' in d))
    print('"abababc" in d = {0}'.format('abababc' in d))
    print('"abbabc" in d = {0}'.format('abbabc' in d))
    print('"acd" in d = {0}'.format('acd' in d))


def test_nfa():
    states = {'q1', 'q2', 'q3', 'q4'}
    alphabet = {'abcde'}
    transition_function = {
            (('q1', 'a'), 'q2'),
            (('q2', 'b'), 'q3'),
            (('q2', 'b'), 'q4'),
            (('q3', 'c'), 'q4'),
            }
    start_state = 'q1'
    accept_states = {'q4'}
    d = DFA(states, alphabet, transition_function, start_state, accept_states)
    print(d)
    print('"abc" in d = {0}'.format('abc' in d))
    print('"acd" in d = {0}'.format('acd' in d))


if __name__ == '__main__':
    #test_dfa_minimization()
    #test_dfa_minimization_equiv_accept_states()
    #test_dfa_with_cycle()
    input = eval(open('input_dfa.txt').read())
    d = DFA(*input)
    print(d)
    while True:
        l = sys.stdin.readline().strip()
        print('"{0}" in DFA = {1}'.format(l, l in d))

