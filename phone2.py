#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

import hangul
import mealy_machine
import getch

DELETE = '\x7f'

class ThreeFourHangulInput(object):
    def __init__(self):
        self.input_chars_log = []
        # Buffers choseong, jungseong, jongseong * 2
        self.input_chars = [[u'', u'', u''], [u'', u'', u'']]
        alphabets = '123456789*0#' + DELETE
        alphabets_choseong = u'ㄱㄴㄷㄹㅁㅂㅅㅇㅈ0ㅎ0' + DELETE
        alphabets_choseong_shift = u'ㄲㅋㄸㅊㅌㅃㅆㅍㅉ000' + DELETE
        alphabets_jongseong = u'ㅜㅕㅏㅠㅗㅑㅡㅛㅓ0ㅣ0' + DELETE
        assert(len(alphabets) == len(alphabets_choseong))
        assert(len(alphabets) == len(alphabets_choseong_shift))
        assert(len(alphabets) == len(alphabets_jongseong))
        self.choseong_trans = dict(zip(alphabets, alphabets_choseong))
        self.choseong_shift_trans = dict(zip(alphabets, alphabets_choseong_shift))
        self.jungseong_trans = dict(zip(alphabets, alphabets_jongseong))
        transitions = []
        output_functions = []
        numpad_all = u'123456789*0#'
        numpad = u'1234567890'

        # DELETE cases. Rolls back to previous state
        # Just transition to self and rollback twice
        transitions += [((Q, DELETE), Q) for Q in 'sSvouaOUAiknrRl']
        output_functions += [((Q, DELETE), self.delete) for Q in 'sSvouaOUAiknrRl']

        transitions += [(('s', u'*'), 's')]
        output_functions += [(('s', u'*'), self.output)]

        transitions += [(('s', c), 'v') for c in numpad]
        output_functions += [(('s', c), self.onset) for c in numpad]
        transitions += [(('s', u'#'), 'S')]
        output_functions += [(('s', u'#'), self.null)]
        transitions += [(('S', c), 'v') for c in numpad]
        output_functions += [(('S', c), self.onset_shift) for c in numpad]

        transitions += [(('v', v), 'o') for v in u'5']
        transitions += [(('v', v), 'u') for v in u'1']
        transitions += [(('v', v), 'a') for v in u'36927']
        transitions += [(('v', v), 'i') for v in u'840']
        output_functions += [(('v', v), self.nucleus) for v in numpad]

        transitions += [(('o', u'#'), 'O')]
        transitions += [(('u', u'#'), 'U')]
        transitions += [(('a', u'#'), 'A')]
        transitions += [(('i', u'#'), 'I')]
        output_functions += [(('o', u'#'), self.null)]
        output_functions += [(('u', u'#'), self.null)]
        output_functions += [(('a', u'#'), self.null)]
        output_functions += [(('i', u'#'), self.null)]

        transitions += [(('O', v), 'a') for v in u'3']
        transitions += [(('U', v), 'a') for v in u'9']
        output_functions += [(('O', v), self.nucleus_combine) for v in u'3']
        output_functions += [(('U', v), self.nucleus_combine) for v in u'9']

        transitions += [(('O', v), 'i') for v in u'0']
        transitions += [(('U', v), 'i') for v in u'0']
        transitions += [(('A', v), 'i') for v in u'0']
        output_functions += [(('O', v), self.nucleus_combine) for v in u'0']
        output_functions += [(('U', v), self.nucleus_combine) for v in u'0']
        output_functions += [(('A', v), self.nucleus_combine) for v in u'0']

        transitions += [((Q, v), 'l') for v in u'124578' for Q in 'OUAI']
        output_functions += [((Q, v), self.coda_shift) for v in u'124578' for Q in 'OUAI']

        transitions += [((Q, v), 'v') for v in u'6' for Q in 'OUAI']
        output_functions += [((Q, v), self.onset_shift_with_output) for v in u'6' for Q in 'OUAI']

        transitions += [((Q, c), 'k') for c in u'16' for Q in 'ouai']
        transitions += [((Q, c), 'n') for c in u'2' for Q in 'ouai']
        transitions += [((Q, c), 'r') for c in u'4' for Q in 'ouai']
        transitions += [((Q, c), 'l') for c in u'357890' for Q in 'ouai']
        output_functions += [((Q, c), self.coda) for c in numpad for Q in 'ouai']

        transitions += [((Q, '*'), 's') for Q in 'ouai']
        output_functions += [((Q, '*'), self.output) for Q in 'ouai']

        transitions += [((Q, u'*'), 's') for Q in 'knrl']
        output_functions += [((Q, u'*'), self.output) for Q in 'knrl']

        transitions += [(('k', c), 'l') for c in u'7']
        output_functions += [(('k', c), self.coda_combine) for c in u'7']
        transitions += [(('n', c), 'l') for c in u'90']
        output_functions += [(('n', c), self.coda_combine) for c in u'90']
        transitions += [(('r', c), 'l') for c in u'15679']
        output_functions += [(('r', c), self.coda_combine) for c in u'15697']

        transitions += [(('r', u'#'), 'R')]
        output_functions += [(('r', u'#'), self.null)]

        transitions += [(('R', c), 'l') for c in u'58']
        output_functions += [(('R', c), self.coda_combine) for c in u'58']
        transitions += [(('R', c), 'v') for c in u'1234679']
        output_functions += [(('R', c), self.onset_shift_with_output) for c in u'1234679']

        transitions += [(('k', c), 'v') for c in set(numpad) - set(u'7')]
        output_functions += [(('k', c), self.onset_with_output) for c in set(numpad) - set(u'7')]
        transitions += [(('n', c), 'v') for c in set(numpad) - set(u'90')]
        output_functions += [(('n', c), self.onset_with_output) for c in set(numpad) - set(u'90')]
        transitions += [(('r', c), 'v') for c in set(numpad) - set(u'15679')]
        output_functions += [(('r', c), self.onset_with_output) for c in set(numpad) - set(u'15679')]
        transitions += [(('l', c), 'v') for c in numpad]
        output_functions += [(('l', c), self.onset_with_output) for c in numpad]

        self.machine = mealy_machine.MealyMachine('sSvouaOUAiknrRl', alphabets, '', transitions, output_functions, 's')

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

    def output(self, state, input_char):
        ret = self.buf()
        self.input_chars[0][0] = u''
        self.input_chars[0][1] = u''
        self.input_chars[0][2] = u''
        return ret

    def onset(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.choseong_trans[input_char]
        self.input_chars[0][0] = input_char
        return u''

    def onset_shift(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.choseong_shift_trans[input_char]
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
        input_char = self.choseong_trans[input_char]
        if not self.input_chars[1][2]:
            self.input_chars[1][2] = self.input_chars[0][0]
        else:
            self.input_chars[1][2] = self.combine_table[(self.input_chars[1][2], self.input_chars[0][0])]
        self.input_chars[0] = [u'', u'', u'']
        ret = self.buf()
        self.input_chars[0] = [input_char, u'', u'']
        self.input_chars[1] = [u'', u'', u'']
        return ret

    def onset_shift_with_output(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.choseong_shift_trans[input_char]
        ret = self.buf()
        self.input_chars[0][0] = input_char
        self.input_chars[0][1] = u''
        self.input_chars[0][2] = u''
        return ret

    def nucleus(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.jungseong_trans[input_char]
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
        input_char = self.jungseong_trans[input_char]
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
        input_char = self.jungseong_trans[input_char]
        self.input_chars[0][1] = input_char
        ret = hangul.join((self.input_chars[1]))
        self.input_chars[1] = [u'', u'', u'']
        return ret

    def coda(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.choseong_trans[input_char]
        self.input_chars[1] = copy.deepcopy(self.input_chars[0])
        self.input_chars[0] = [u'', u'', u'']
        self.input_chars[0][0] = input_char
        return u''

    def coda_shift(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.choseong_shift_trans[input_char]
        self.input_chars[1] = copy.deepcopy(self.input_chars[0])
        self.input_chars[0] = [u'', u'', u'']
        self.input_chars[0][0] = input_char
        return u''

    def coda_combine(self, state, input_char):
        self.input_chars_log.append(copy.deepcopy(self.input_chars))
        input_char = self.choseong_trans[input_char]
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
    print('Loaded Mealy Machine: {0}'.format(mealy_machine))
    l = input_generator()
    print('Simulating output...')
    for f in mealy_machine(l):
        print(u'buf: {0}'.format(hangul_input.buf()))
        print(u'output: {0}'.format(f))


if __name__ == '__main__':
    mm = ThreeFourHangulInput()
    simulate(mm)
