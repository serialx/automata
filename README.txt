Automata Project 1-1
====================

Name: 홍성진 (20060735, serialx@serialx.net)


Input
-----

다음과 같이 input_dfa.txt에 5-tuple DFA를 입력한다:

``` python
(
# States
{'q1', 'q2', 'q3', 'q4'},
# Alphabet
{'abcde'},
# Transition Function
{
    (('q1', 'a'), 'q2'),
    (('q2', 'b'), 'q3'),
    (('q3', 'a'), 'q2'),
    (('q3', 'c'), 'q4'),
},
# Start State
'q1',
# Accept States
{'q4'}
)
```


Usage
-----

참고: Python 2.7 이상 필요
 1. 아래와 같이 실행하면 로드된 DFA를 출력한다.
 2. 이후 문자열을 입력하면 membership test를 진행하여 True혹은 False를 출력한다.
 3. Enter혹은 EOF(^D)를 입력하면 프로그램이 종료된다.

```
$ python dfa.py
DFA(states=set(['q1', 'q3', 'q2', 'q4']), 
    alphabet=set(['abcde']), 
    transition_function=set([(('q3', 'a'), 'q2'), (('q3', 'c'), 'q4'), (('q2', 'b'), 'q3'), (('q1', 'a'), 'q2')]), 
    start_state=q1, 
    accept_state=set(['q4']))
abcd
(q1, a) --> ['q2']
(q2, b) --> ['q3']
(q3, c) --> ['q4']
(q4, d) --> []
"abcd" in DFA = False
abc
(q1, a) --> ['q2']
(q2, b) --> ['q3']
(q3, c) --> ['q4']
"abc" in DFA = True
ababababc
(q1, a) --> ['q2']
(q2, b) --> ['q3']
(q3, a) --> ['q2']
(q2, b) --> ['q3']
(q3, a) --> ['q2']
(q2, b) --> ['q3']
(q3, a) --> ['q2']
(q2, b) --> ['q3']
(q3, c) --> ['q4']
"ababababc" in DFA = True
```
