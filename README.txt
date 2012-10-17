Automata Project 2-1
====================

Name: 홍성진 (20060735, serialx@serialx.net)


Specification
-------------
 * Language: Python (2.7)
 * Environment: Linux (compatible terminal emulator with UTF-8 settings), Python 2.7


Input
-----

다음과 같이 input_nfa.txt에 6-tuple NFA를 입력한다. 여기서 epsilon-move에 사용하는 epsilon은 ''로 나타낸다.

``` python
(
# States
{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13},
# Alphabet
{'0', '1', ''},
# Transition Function
{
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
},
# Start State
1,
# Accept States
{13},
)
```


Usage
-----

참고: Python 2.7 이상 필요
 1. 아래와 같이 실행하면 로드된 NFA, 변환된 DFA, 이름을 바꾼 DFA, 최소화된 mDFA를 출력한다.
 2. 이후 문자를 입력하면 mDFA가 작동하고 mDFA에 문자열이 속하는지 확인할 수 있다.
 3. EOF(^D)를 입력하면 프로그램이 종료된다.

```
$ python nfa.py 
= NFA =
NFA(states=set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]), 
    alphabet=set(['', '1', '0']), 
    transition_function=set([((8, '0'), 9), ((11, '0'), 12), ((7, ''), 8), ((2, ''), 3), ((10, '1'), 11), ((1, ''), 2), ((1, ''), 8), ((4, '1'), 6), ((6, ''), 7), ((5, ''), 7), ((3, '0'), 5), ((7, ''), 2), ((12, '1'), 13), ((2, ''), 4), ((9, '1'), 10)]), 
    start_state=1, 
    accept_state=set([13]))
(+) Converting to DFA...

= DFA =
DFA(states=set([frozenset([8, 1, 2, 3, 4]), frozenset([2, 3, 4, 5, 7, 8, 9]), frozenset([2, 3, 4, 5, 7, 8, 9, 12]), frozenset([2, 3, 4, 6, 7, 8, 10, 13]), frozenset([2, 3, 4, 6, 7, 8]), frozenset([2, 3, 4, 6, 7, 8, 11]), frozenset([2, 3, 4, 6, 7, 8, 10])]), 
    alphabet=set(['1', '0']), 
    transition_function=set([((frozenset([2, 3, 4, 5, 7, 8, 9]), '1'), frozenset([2, 3, 4, 6, 7, 8, 10])), ((frozenset([2, 3, 4, 6, 7, 8]), '1'), frozenset([2, 3, 4, 6, 7, 8])), ((frozenset([2, 3, 4, 6, 7, 8, 11]), '0'), frozenset([2, 3, 4, 5, 7, 8, 9, 12])), ((frozenset([8, 1, 2, 3, 4]), '1'), frozenset([2, 3, 4, 6, 7, 8])), ((frozenset([2, 3, 4, 6, 7, 8]), '0'), frozenset([2, 3, 4, 5, 7, 8, 9])), ((frozenset([2, 3, 4, 6, 7, 8, 10, 13]), '1'), frozenset([2, 3, 4, 6, 7, 8, 11])), ((frozenset([2, 3, 4, 5, 7, 8, 9]), '0'), frozenset([2, 3, 4, 5, 7, 8, 9])), ((frozenset([2, 3, 4, 5, 7, 8, 9, 12]), '0'), frozenset([2, 3, 4, 5, 7, 8, 9])), ((frozenset([2, 3, 4, 5, 7, 8, 9, 12]), '1'), frozenset([2, 3, 4, 6, 7, 8, 10, 13])), ((frozenset([2, 3, 4, 6, 7, 8, 11]), '1'), frozenset([2, 3, 4, 6, 7, 8])), ((frozenset([8, 1, 2, 3, 4]), '0'), frozenset([2, 3, 4, 5, 7, 8, 9])), ((frozenset([2, 3, 4, 6, 7, 8, 10]), '0'), frozenset([2, 3, 4, 5, 7, 8, 9])), ((frozenset([2, 3, 4, 6, 7, 8, 10, 13]), '0'), frozenset([2, 3, 4, 5, 7, 8, 9])), ((frozenset([2, 3, 4, 6, 7, 8, 10]), '1'), frozenset([2, 3, 4, 6, 7, 8, 11]))]), 
    start_state=frozenset([8, 1, 2, 3, 4]), 
    accept_state=set([frozenset([2, 3, 4, 6, 7, 8, 10, 13])]))
(+) Renaming states...

= Renamed DFA =
DFA(states=set([1, 2, 3, 4, 5, 6, 7]), 
    alphabet=set(['1', '0']), 
    transition_function=set([((4, '0'), 2), ((1, '1'), 5), ((1, '0'), 2), ((5, '0'), 2), ((2, '0'), 2), ((6, '0'), 3), ((7, '0'), 2), ((3, '1'), 4), ((4, '1'), 6), ((7, '1'), 6), ((2, '1'), 7), ((3, '0'), 2), ((6, '1'), 5), ((5, '1'), 5)]), 
    start_state=1, 
    accept_state=set([4]))
(+) Computing mDFA...
reachable_states = set([1, 2, 3, 4, 5, 6, 7])
equivalent_state_pairs = set([frozenset([5, 7]), frozenset([5, 6]), frozenset([1, 5]), frozenset([1, 7]), frozenset([1, 6]), frozenset([1, 2]), frozenset([2, 5])])

= mDFA =
DFA(states=set([1, 2, 3, 4, 5, 6]), 
    alphabet=set(['1', '0']), 
    transition_function=set([((2, '1'), 3), ((5, '1'), 6), ((1, '0'), 5), ((3, '1'), 4), ((4, '0'), 5), ((6, '0'), 5), ((3, '0'), 1), ((2, '0'), 5), ((6, '1'), 3), ((4, '1'), 4), ((5, '0'), 5), ((1, '1'), 2)]), 
    start_state=4, 
    accept_state=set([2]))

= Output (As per homework specs) =
state = {1, 2, 3, 4, 5, 6}
final_state = {2}
start_state = 4
(2, 3, 1)
(5, 6, 1)
(1, 5, 0)
(3, 4, 1)
(4, 5, 0)
(6, 5, 0)
(3, 1, 0)
(2, 5, 0)
(6, 3, 1)
(4, 4, 1)
(5, 5, 0)
(1, 2, 1)

= Test =
01101
(4, 0) --> set([5])
(5, 1) --> set([6])
(6, 1) --> set([3])
(3, 0) --> set([1])
(1, 1) --> set([2])
"01101" in DFA = True
10101 
(4, 1) --> set([4])
(4, 0) --> set([5])
(5, 1) --> set([6])
(6, 0) --> set([5])
(5, 1) --> set([6])
"10101" in DFA = False
1010101101
(4, 1) --> set([4])
(4, 0) --> set([5])
(5, 1) --> set([6])
(6, 0) --> set([5])
(5, 1) --> set([6])
(6, 0) --> set([5])
(5, 1) --> set([6])
(6, 1) --> set([3])
(3, 0) --> set([1])
(1, 1) --> set([2])
"1010101101" in DFA = True
```
