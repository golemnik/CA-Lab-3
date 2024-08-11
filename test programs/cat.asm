push #start
jmp
push #intrpt
jmp

#intrpt
push 0                  | #ret <state> -> 0 #ret <state>        |
input                   | -> <char> #ret <state>                |
push 1                  | -> 1 <char> #ret <state>              |
output                  | -> #ret <state>                       | <char>
ret                     | -> _                                  | <char>

#start
#cyc push 2             | _ -> 2
input                   | -> <flag>
push #exit              | -> #exit <flag>
jmpe                    | -> _
push #cyc               | -> #cyc
jmp                     | -> _
#exit hlt               | _ -> _