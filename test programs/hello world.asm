#msg1 data h e l l o _ w o r l d 0

push #start         | _ -> #start
jmp                 | -> _
hlt                 | _ -> _
hlt                 | _ -> _

#start
push #msg1          | _ -> #msg1                |
#cyc dup            | -> #msg1 #msg1            |
load                | -> 'h' #msg1              |
dup                 | -> 'h' 'h' #msg1          |
push #exit          | -> #exit 'h' 'h' #msg1    |
jmpe                | -> 'h' #msg1              |
output              | -> #msg1                  | h
push 1              | -> 1 #msg1                | h
add                 | -> #msg1+1                | h
jmp #cyc            | -> #msg1+1                | h
#exit hlt           | -> '0' #msg1              | hello world