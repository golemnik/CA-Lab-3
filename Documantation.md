Language

a - address / ap - address port \
n - number \
_ - nothing \
c - compare result (-1, 0, 1)\
s - interrupt state (0, 1)\

Ports:\
0 - input\
1 - output\
2 - input_eof


- **push** n
  - _ -> n
  - add n to the top of the stack
- **pop**
  - n -> _
  - take top from stack
- **load**
  - a -> n 
  - load n from address a
- **store**
  - a n -> _
  - safe n at address a 
- **input**
  - ap -> n
  - takes n from port ap
- **output**
  - ap n -> _
  - sends n to port ap
- **add**
  - n1 n2 -> n1+n2
  - sums first two nums in stack
- **if**
  - n1 n2 -> -1//0//1
  - compares two first from stack and pushes result to the top of stack
  - -1 means n1 < n2
  - 0 means n1 = n2
  - 1 means n1 > n2
- **swap**
  - n1 n2 -> n2 n1
  - swaps first two nums from stack
- **roll**
  - n1 n2 n3 -> n3 n1 n2
  - rolls three elements of the stack
- **dup**
  - n1 -> n1 n1
  - duplicates top of the stack
- **jmp**
  - a -> _
- **jmpb**
  - a c -> _
  - jumps to address if c is 1
- **jmpe**
  - a c -> _
  - jumps to address if c is 0
- **ret**
  - a s -> _
  - returns from interrupt to program and allows restore interruptable state
- **hlt**
  - stops program