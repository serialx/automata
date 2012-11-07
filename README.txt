Automata Project 1
==================

Name: 홍성진 (20060735, serialx@serialx.net)


Specification
-------------
 * Language: Python (2.7)
 * Environment: Linux (compatible terminal emulator with UTF-8 settings), Python 2.7


Usage
-----
 * 2벌식 한글입력기(받침우선): qwerty1.py
 * 2벌식 한글입력기(초성우선): qwerty2.py
 * 3x4 한돌코드 한글입력기(받침우선): phone1.py
 * 3x4 한돌코드 한글입력기(초성우선): phone2.py

참고: Python 2.7 이상 필요
 1. 선택한 입력기를 실행한다. (ex: python qwerty1.py )
 2. 이후 문자를 입력하면 한글이 조합되고 조합이 완료된 글자가 출력된다.
 3. EOF(^D)를 입력하면 프로그램이 종료된다.

```
$ python qwerty1.py
Loaded Mealy Machine
Simulating output...
Output functions possible: (S, q) --> [<bound method QwertyHangulInput.onset of <__main__.QwertyHangulInput object at 0x108e2e850>>]
Transition functions possible: (S, q) --> ['V']
buf: ㅂ
output: 
Output functions possible: (V, n) --> [<bound method QwertyHangulInput.nucleus of <__main__.QwertyHangulInput object at 0x108e2e850>>]
Transition functions possible: (V, n) --> ['U']
buf: 부
output: 
Output functions possible: (U, p) --> [<bound method QwertyHangulInput.nucleus_combine of <__main__.QwertyHangulInput object at 0x108e2e850>>]
Transition functions possible: (U, p) --> ['I']
buf: 붸
output: 
Output functions possible: (I, f) --> [<bound method QwertyHangulInput.coda of <__main__.QwertyHangulInput object at 0x108e2e850>>]
Transition functions possible: (I, f) --> ['R']
buf: 뷀
output: 
Output functions possible: (R, r) --> [<bound method QwertyHangulInput.coda_combine of <__main__.QwertyHangulInput object at 0x108e2e850>>]
Transition functions possible: (R, r) --> ['L']
buf: 뷁
output: 
Output functions possible: (L, g) --> [<bound method QwertyHangulInput.onset_with_output of <__main__.QwertyHangulInput object at 0x108e2e850>>]
Transition functions possible: (L, g) --> ['V']
onset_with_output
buf: ㅎ
output: 뷁
Output functions possible: (V, k) --> [<bound method QwertyHangulInput.nucleus of <__main__.QwertyHangulInput object at 0x108e2e850>>]
Transition functions possible: (V, k) --> ['A']
buf: 하
output: 
```
