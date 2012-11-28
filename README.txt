Automata Project 2
==================

Name: 홍성진 (20060735, serialx@serialx.net)


Specification
-------------
 * Language: Python (2.7)
 * Library: PLY(Python Lex Yacc) - 포함되어있음
 * Environment: Linux (compatible terminal emulator with UTF-8 settings), Python 2.7


Usage
-----
 * 정규식 DFA변환: re.py

참고: Python 2.7 이상 필요
 1. 프로그램을 실행한다. (ex: python re.py )
 2. 정규식을 입력한다.
    Epsilon은 '', Empty Set은 {} 으로 표현한다
    Example: (0+'')1*+{}
 3. 이후 문자를 입력하면 해당 문자가 정규식에 포함되는지 판별되어 출력된다.
 3. EOF(^D)를 입력하면 프로그램이 종료된다.

```
$ python re.py 
re > (0+'')1*+{}
Or(Concat(Or(('0'),('')),Production(('1'))),Empty)
([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], set(['', '0', '1']), [((13, ''), 5), ((13, ''), 11), ((5, ''), 1), ((5, ''), 3), ((1, '0'), 2), ((3, ''), 4), ((2, ''), 6), ((4, ''), 6), ((6, ''), 9), ((9, ''), 7), ((8, ''), 10), ((9, ''), 10), ((8, ''), 7), ((7, '1'), 8), ((10, ''), 14), ((12, ''), 14)], 13, [14])
NFA(states=set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]), 
    alphabet=set(['', '0', '1']), 
    transition_function=set([((5, ''), 3), ((9, ''), 7), ((4, ''), 6), ((1, '0'), 2), ((8, ''), 7), ((7, '1'), 8), ((8, ''), 10), ((9, ''), 10), ((13, ''), 11), ((10, ''), 14), ((13, ''), 5), ((6, ''), 9), ((2, ''), 6), ((5, ''), 1), ((12, ''), 14), ((3, ''), 4)]), 
    start_state=13, 
    accept_state=set([14]))
DFA(states=set([1, 2, 3]), 
    alphabet=set(['1', '0']), 
    transition_function=set([((3, '1'), 3), ((2, '1'), 3), ((1, '1'), 3), ((2, '0'), 1)]), 
    start_state=2, 
    accept_state=set([1, 2, 3]))
reachable_states = set([1, 2, 3])
equivalent_state_pairs = set([])
DFA(states=set([1, 2, 3]), 
    alphabet=set(['1', '0']), 
    transition_function=set([((2, '1'), 2), ((1, '0'), 3), ((3, '1'), 2), ((1, '1'), 2)]), 
    start_state=1, 
    accept_state=set([1, 2, 3]))
 
"" in DFA = True
0
(1, 0) --> set([3])
"0" in DFA = True
1
(1, 1) --> set([2])
"1" in DFA = True
01
(1, 0) --> set([3])
(3, 1) --> set([2])
"01" in DFA = True
10
(1, 1) --> set([2])
(2, 0) --> set([])
"10" in DFA = False
```
