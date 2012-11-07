#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hangul
import mealy_machine
import getch
import copy

DELETE = '\x7f'

class QwertyHangulInput(object):
    def __init__(self):
        self.input_chars_log = []
        # Buffers choseong, jungseong, jongseong * 2
        self.input_chars = [[u'', u'', u''], [u'', u'', u'']]
        alphabets = 'qwertyuiopasdfghjklzxcvbnmQWERTOP' + DELETE
        alphabets_hangul = u'ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔㅁㄴㅇㄹㅎㅗㅓㅏㅣㅋㅌㅊㅍㅠㅜㅡㅃㅉㄸㄲㅆㅒㅖ' + DELETE
        assert(len(alphabets) == len(alphabets_hangul))
        self.alphabet_trans = dict(zip(alphabets_hangul, alphabets))
        self.hangul_trans = dict(zip(alphabets, alphabets_hangul))
        transitions = []
        output_functions = []
        c_set = u'ㅂㅈㄷㄱㅅㅁㄴㅇㄹㅎㅋㅌㅊㅍㅃㅉㄸㄲㅆ'
        v_set = u'ㅛㅕㅑㅐㅔㅗㅓㅏㅣㅠㅜㅡㅒㅖ'

        # DELETE cases. Rolls back to previous state
        # Just transition to self and rollback twice
        transitions += [((Q, DELETE), Q) for Q in 'SVOUAIKNRL']
        output_functions += [((Q, DELETE), self.delete) for Q in 'SVOUAIKNRL']

        transitions += [(('S', c), 'V') for c in c_set]
        output_functions += [(('S', c), self.onset) for c in c_set]

        transitions += [(('V', v), 'O') for v in u'ㅗ']
        transitions += [(('V', v), 'U') for v in u'ㅜ']
        transitions += [(('V', v), 'A') for v in u'ㅏㅑㅓㅕㅡ']
        transitions += [(('V', v), 'I') for v in u'ㅛㅠㅣㅐㅔㅒㅖ']
        output_functions += [(('V', v), self.nucleus) for v in v_set]

        transitions += [(('O', v), 'I') for v in u'ㅏㅣㅐ']
        transitions += [(('U', v), 'I') for v in u'ㅓㅣㅔ']
        transitions += [(('A', v), 'I') for v in u'ㅣ']
        output_functions += [(('O', v), self.nucleus_combine) for v in u'ㅏㅣㅐ']
        output_functions += [(('U', v), self.nucleus_combine) for v in u'ㅓㅣㅔ']
        output_functions += [(('A', v), self.nucleus_combine) for v in u'ㅣ']

        transitions += [((Q, c), 'K') for c in u'ㄱㅂ' for Q in 'OUAI']
        transitions += [((Q, c), 'N') for c in u'ㄴ' for Q in 'OUAI']
        transitions += [((Q, c), 'R') for c in u'ㄹ' for Q in 'OUAI']
        transitions += [((Q, c), 'L') for c in u'ㄷㅁㅅㅇㅈㅊㅋㅌㅍㅎㄲㅆ' for Q in 'OUAI']
        output_functions += [((Q, c), self.coda) for c in set(c_set) - set(u'ㄸㅃㅉ') for Q in 'OUAI']

        transitions += [((Q, c), 'V') for c in u'ㄸㅃㅉ' for Q in 'OUAI']
        output_functions += [((Q, c), self.onset_with_output) for c in u'ㄸㅃㅉ' for Q in 'OUAI']

        transitions += [((Q, v), 'O') for v in u'ㅗ' for Q in 'KNRL']
        transitions += [((Q, v), 'U') for v in u'ㅜ' for Q in 'KNRL']
        transitions += [((Q, v), 'A') for v in u'ㅏㅑㅓㅕㅡ' for Q in 'KNRL']
        transitions += [((Q, v), 'I') for v in u'ㅛㅠㅣㅐㅔㅒㅖ' for Q in 'KNRL']
        output_functions += [((Q, v), self.nucleus_with_output) for v in v_set for Q in 'KNRL']

        transitions += [(('K', c), 'L') for c in u'ㅅ']
        output_functions += [(('K', c), self.coda_combine) for c in u'ㅅ']
        transitions += [(('N', c), 'L') for c in u'ㅈㅎ']
        output_functions += [(('N', c), self.coda_combine) for c in u'ㅈㅎ']
        transitions += [(('R', c), 'L') for c in u'ㄱㅁㅂㅅㅌㅍㅎ']
        output_functions += [(('R', c), self.coda_combine) for c in u'ㄱㅁㅂㅅㅌㅍㅎ']

        transitions += [(('K', c), 'V') for c in set(c_set) - set(u'ㅅ')]
        output_functions += [(('K', c), self.onset_with_output) for c in set(c_set) - set(u'ㅅ')]
        transitions += [(('N', c), 'V') for c in set(c_set) - set(u'ㅈㅎ')]
        output_functions += [(('N', c), self.onset_with_output) for c in set(c_set) - set(u'ㅈㅎ')]
        transitions += [(('R', c), 'V') for c in set(c_set) - set(u'ㄱㅁㅂㅅㅌㅍㅎ')]
        output_functions += [(('R', c), self.onset_with_output) for c in set(c_set) - set(u'ㄱㅁㅂㅅㅌㅍㅎ')]
        transitions += [(('L', c), 'V') for c in c_set]
        output_functions += [(('L', c), self.onset_with_output) for c in c_set]

        transitions = [((Q, self.alphabet_trans[c]), T) for ((Q, c), T) in transitions]
        output_functions = [((Q, self.alphabet_trans[c]), T) for ((Q, c), T) in output_functions]
        self.machine = mealy_machine.MealyMachine('SVOUAIKNRL', alphabets, '', transitions, output_functions, 'S')

    def buf(self):
        return hangul.join(self.input_chars[1]) + hangul.join(self.input_chars[0])

    def delete(self, state, input_char):
        print 'delete', self.input_chars_log
        if (self.input_chars_log):
            self.input_chars = self.input_chars_log.pop(-1)
            print 'rollback'
            self.machine.rollback()
            self.machine.rollback()
        return u''

    def null(self, state, input_char):
        return u''

    def onset(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.hangul_trans[input_char]
        self.input_chars[0][0] = input_char
        return u''

    combine_table = {
            (u'ㄱ', u'ㅅ'): u'ㄳ',
            (u'ㅂ', u'ㅅ'): u'ㅄ',

            (u'ㄴ', u'ㅈ'): u'ㄵ',
            (u'ㄴ', u'ㅎ'): u'ㄶ',

            (u'ㄹ', u'ㄱ'): u'ㄺ',
            (u'ㄹ', u'ㅁ'): u'ㄻ',
            (u'ㄹ', u'ㅂ'): u'ㄼ',
            (u'ㄹ', u'ㅅ'): u'ㄽ',
            (u'ㄹ', u'ㅌ'): u'ㄾ',
            (u'ㄹ', u'ㅍ'): u'ㄿ',
            (u'ㄹ', u'ㅎ'): u'ㅀ',
            }

    def onset_with_output(self, state, input_char):
        if not self.input_chars[1][0]:
            self.input_chars[1] = self.input_chars[0]
            self.input_chars[0] = [u'', u'', u'']
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.hangul_trans[input_char]
        if not self.input_chars[1][2]:
            self.input_chars[1][2] = self.input_chars[0][0]
        else:
            self.input_chars[1][2] = self.combine_table[(self.input_chars[1][2], self.input_chars[0][0])]
        self.input_chars[0] = [u'', u'', u'']
        ret = self.buf()
        self.input_chars[0] = [input_char, u'', u'']
        self.input_chars[1] = [u'', u'', u'']
        return ret

    def nucleus(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.hangul_trans[input_char]
        self.input_chars[0][1] = input_char
        return u''

    def nucleus_combine(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        combine_table = {
                (u'ㅗ', u'ㅏ'): u'ㅘ',
                (u'ㅗ', u'ㅣ'): u'ㅚ',
                (u'ㅗ', u'ㅐ'): u'ㅙ',

                (u'ㅜ', u'ㅓ'): u'ㅝ',
                (u'ㅜ', u'ㅣ'): u'ㅟ',
                (u'ㅜ', u'ㅔ'): u'ㅞ',

                (u'ㅏ', u'ㅣ'): u'ㅐ',
                (u'ㅑ', u'ㅣ'): u'ㅒ',
                (u'ㅓ', u'ㅣ'): u'ㅔ',
                (u'ㅕ', u'ㅣ'): u'ㅖ',
                (u'ㅡ', u'ㅣ'): u'ㅢ',
                }
        input_char = self.hangul_trans[input_char]
        key = (self.input_chars[0][1], input_char)
        self.input_chars[0][1] = combine_table[key]
        return u''

    def nucleus_with_output(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        split_table = {
                u'ㄳ': (u'ㄱ', u'ㅅ'),
                u'ㅄ': (u'ㄱ', u'ㅂ'),

                u'ㄵ': (u'ㄴ', u'ㅈ'),
                u'ㄶ': (u'ㄴ', u'ㅎ'),

                u'ㄺ': (u'ㄹ', u'ㄱ'),
                u'ㄻ': (u'ㄹ', u'ㅁ'),
                u'ㄼ': (u'ㄹ', u'ㅂ'),
                u'ㄽ': (u'ㄹ', u'ㅅ'),
                u'ㄾ': (u'ㄹ', u'ㅌ'),
                u'ㄿ': (u'ㄹ', u'ㅍ'),
                u'ㅀ': (u'ㄹ', u'ㅎ'),
                }
        input_char = self.hangul_trans[input_char]
        self.input_chars[0][1] = input_char
        ret = hangul.join((self.input_chars[1]))
        self.input_chars[1] = [u'', u'', u'']
        return ret

    def coda(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.hangul_trans[input_char]
        self.input_chars[1] = copy.deepcopy(self.input_chars[0])
        self.input_chars[0] = [u'', u'', u'']
        self.input_chars[0][0] = input_char
        return u''

    def coda_combine(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.hangul_trans[input_char]
        self.input_chars[1][2] = self.input_chars[0][0]
        self.input_chars[0][0] = input_char
        return u''

    def input(self, input_char):
        pass


def input_generator():
    while True:
        c = getch.getch()
        if ord(c) == 4: return  # EOF
        if not c: return
        yield c


def simulate(hangul_input):
    mealy_machine = hangul_input.machine
    print('Loaded Mealy Machine')
    l = input_generator()
    print('Simulating output...')
    for f in mealy_machine(l):
        print(u'buf: {0}'.format(hangul_input.buf()))
        print(u'output: {0}'.format(f))


if __name__ == '__main__':
    mm = QwertyHangulInput()
    simulate(mm)
