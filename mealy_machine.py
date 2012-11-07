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

   Mealy Machine implementation.
"""

from __future__ import print_function
import sys

import getch


class MealyMachine(object):
    """Mealy Machine implementation with callable output alphabet"""
    def __init__(self, states, alphabet, output_alphabet, transition_function, output_function, start_state):
        self.states = set(states)
        assert len(self.states) == len(states)
        self.alphabet = set(alphabet)
        assert len(self.alphabet) == len(alphabet)
        self.output_alphabet = set(output_alphabet)
        assert len(self.output_alphabet) == len(output_alphabet)
        self.transition_function = set(transition_function)
        assert len(self.transition_function) == len(transition_function)
        self.output_function = set(output_function)
        assert len(self.output_function) == len(output_function)
        self.start_state = start_state
        assert start_state in states

    def __unicode__(self):
        format_str = (u"MealyMachine(states={0}, \n    alphabet={1}, \n    "
                "output_alphabet={2}, \n    transition_function={3}, \n    "
                "output_function={4}, \n    start_state={5}")
        return format_str.format(self.states, self.alphabet, self.output_alphabet,
            self.transition_function, self.output_function, self.start_state)

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __call__(self, string, verbose=True):
        output = []
        state = self.start_state
        for c in string:
            output_possible = [func for ((cur_state, char), func) in
                    self.output_function if cur_state == state and char == c]
            if (verbose):
                print(u"Output functions possible: ({0}, {1}) --> {2}".format(state, c, output_possible))
            assert len(output_possible) != 0, 'No output function exist'
            assert len(output_possible) == 1, 'More than one output function exists'
            output_char = output_possible[0]
            #assert(output_char in self.output_alphabet)
            yield output_char(state, c)
            transitions_possible = [dest for ((start, char), dest) in
                    self.transition_function if start == state and char == c]
            if (verbose):
                print(u"Transition functions possible: ({0}, {1}) --> {2}".format(state, c, transitions_possible))
            if (len(transitions_possible) == 0):
                return
            assert len(transitions_possible) == 1, ('Nondeterministic '
                    'behaviour not allowed in DFA')
            state = transitions_possible[0]

    def simulate(self, string):
        funcs = self.__call__(string, verbose=False)
        for f in funcs:
            assert callable(f)
            f()


def test_simple_mealy_machine():
    states = {'q1', 'q2', 'q3', 'q4'}
    alphabet = {'abcde'}
    begin = lambda x: x[-1]
    func_a = lambda: print('func_a: executing')
    func_b = lambda: print('func_b: executing')
    output_alphabet = {func_a, func_b}
    transition_function = {
            (('q1', 'a'), 'q2'),
            (('q2', 'b'), 'q3'),
            (('q3', 'c'), 'q4'),
            }
    output_function = {
            (('q1', 'a'), func_a),
            (('q2', 'b'), func_b),
            (('q3', 'c'), func_a),
            }
    start_state = 'q1'
    d = MealyMachine(states, alphabet, output_alphabet, transition_function, output_function, start_state)
    ret = d('abc')
    print('Output of Mealy Machine = {0}'.format(list(ret)))
    print('Simulating output...')
    for f in ret:
        f()


def input_generator():
    while True:
        c = getch.getch()
        if ord(c) == 4: return  # EOF
        if not c: return
        yield c


def simulate(mealy_machine):
    print('Loaded Mealy Machine:', mealy_machine)
    l = input_generator()
    print('Simulating output...')
    for f in mealy_machine(l):
        f()


if __name__ == '__main__':
    #test_simple_mealy_machine()
    funcs = eval(open('input_mealy_machine_funcs.txt').read())
    input_params = eval(open('input_mealy_machine.txt').read(), funcs)
    d = MealyMachine(*input_params)
    simulate(d)
