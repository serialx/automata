Automata Project 1-2
====================

Name: 홍성진 (20060735, serialx@serialx.net)


Specification
-------------
 * Language: Python (2.7)
 * Environment: Linux (compatible terminal emulator with UTF-8 settings), Python 2.7


Input
-----

다음과 같이 input_mealy_machine.txt에 6-tuple Mealy Machine을 입력한다:

``` python
(
# States
{'q1', 'q2', 'q3'},
# Alphabet
{'01'},
# Output Alphabet
{func_0, func_1},
# Transition Function
{
    (('q1', '0'), 'q2'),
    (('q1', '1'), 'q3'),
    (('q2', '0'), 'q2'),
    (('q2', '1'), 'q3'),
    (('q3', '0'), 'q2'),
    (('q3', '1'), 'q3'),
},
# Output Function
{
    (('q1', '0'), func_0),
    (('q1', '1'), func_0),
    (('q2', '0'), func_0),
    (('q2', '1'), func_1),
    (('q3', '0'), func_1),
    (('q3', '1'), func_0),
},
# Start State
'q1',
)
```

다음과 같이 input_mealy_machine.txt에서 사용하는 함수를 input_mealy_machine_funcs.txt에 입력한다:

``` python
{
'func_0': lambda: print('func_0: bit not changed'),
'func_1': lambda: print('func_1: bit changed!!!'),
}
```


Usage
-----

참고: Python 2.7 이상 필요
 1. 아래와 같이 실행하면 로드된 Mealy Machine을 출력한다.
 2. 이후 문자를 입력하면 Mealy Machine이 작동하고 단계별로 Output Alphabet인 프로그램 블록이 실행된다.
 3. EOF(^D)를 입력하면 프로그램이 종료된다.

```
$ python mealy_machine.py 
Loaded Mealy Machine: MealyMachine(states=set(['q1', 'q3', 'q2']), 
    alphabet=set(['01']), 
    output_alphabet=set([<function <lambda> at 0x100892f50>, <function <lambda> at 0x100892ed8>]), 
    transition_function=set([(('q3', '1'), 'q3'), (('q1', '1'), 'q3'), (('q2', '1'), 'q3'), (('q3', '0'), 'q2'), (('q1', '0'), 'q2'), (('q2', '0'), 'q2')]), 
    output_function=set([(('q3', '0'), <function <lambda> at 0x100892f50>), (('q1', '1'), <function <lambda> at 0x100892ed8>), (('q3', '1'), <function <lambda> at 0x100892ed8>), (('q1', '0'), <function <lambda> at 0x100892ed8>), (('q2', '1'), <function <lambda> at 0x100892f50>), (('q2', '0'), <function <lambda> at 0x100892ed8>)]), 
    start_state=q1
Simulating output...
Output functions possible: (q1, 0) --> [<function <lambda> at 0x100892ed8>]
func_0: bit not changed
Transition functions possible: (q1, 0) --> ['q2']
Output functions possible: (q2, 0) --> [<function <lambda> at 0x100892ed8>]
func_0: bit not changed
Transition functions possible: (q2, 0) --> ['q2']
Output functions possible: (q2, 1) --> [<function <lambda> at 0x100892f50>]
func_1: bit changed!!!
Transition functions possible: (q2, 1) --> ['q3']
Output functions possible: (q3, 1) --> [<function <lambda> at 0x100892ed8>]
func_0: bit not changed
Transition functions possible: (q3, 1) --> ['q3']
Output functions possible: (q3, 0) --> [<function <lambda> at 0x100892f50>]
func_1: bit changed!!!
Transition functions possible: (q3, 0) --> ['q2']
```
