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

    def __unicode__(self):
        format_str = (u"DFA(states={0}, \n    alphabet={1}, \n    "
                "transition_function={2}, \n    start_state={3}, \n    "
                "accept_state={4})")
        return format_str.format(self.states, self.alphabet,
            self.transition_function, self.start_state, self.accept_states)

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __contains__(self, string):
        """Usage: "asdf" in d"""
        state = self.start_state
        for c in string:
            # For all transitions possible with 'c' and 'state'
            # TODO(serialx): Use hash table to improve performance.
            transitions_possible = [dest for ((start, char), dest) in
                    self.transition_function if start == state and char == c]
            print("({0}, {1}) --> {2}".format(state, c, transitions_possible))
            if (len(transitions_possible) == 0):
                return False
            assert len(transitions_possible) == 1, ('Nondeterministic '
                    'behaviour not allowed in DFA')
            state = transitions_possible[0]
        if (state in self.accept_states):
            return True


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
    #test_simple_dfa()
    #test_dfa_with_cycle()
    input = eval(open('input_dfa.txt').read())
    d = DFA(*input)
    print(d)
    while True:
        l = sys.stdin.readline().strip()
        print('"{0}" in DFA = {1}'.format(l, l in d))

