#msg1 data W h a t _ i s _ y o u r _ n a m e ? 0
#msg2 data H e l l o , _ 0
#msg3 data ! 0
#addr_user data #user
#user data 0

push #start         | _ -> #start
jmp                 | -> _
push #intrpt        | _ -> #intrpt
jmp                 | _ -> _

#intrpt
push 0              | #ret <state> -> 0 #ret <state>        |
input               | -> <char> #ret <state>                |
push #addr_user     | -> #addr_user <char> #ret <state>
dup                 | -> #addr_user #addr_user <char> #ret <state>
load                | -> #user #addr_user <char> #ret <state>
dup                 | -> #user #user #addr_user <char> #ret <state>
push 1              | -> 1 #user #user #addr_user <char> #ret <state>
add                 | -> #user+1 #user #addr_user <char> #ret <state>
roll                | -> #addr_user #user+1 #user <char> #ret <state>
store               | -> #user <char> #ret <state>
store               | -> #ret <state>
ret                 | -> _

#out                | -> #msg #ret_addr
#cyc_out dup        | -> #msg #msg #ret_addr                        |
load                | -> <char> #msg #ret_addr                      |
dup                 | -> <char> <char> #msg #ret_addr               |
push #cyc_out       | -> #exit_out <char> <char> #msg #ret_addr     |
jmpe                | -> <char> #msg #ret_addr                      |
output              | -> #msg #ret_addr                             | w
push 1              | -> 1 #msg #ret_addr                           | w
add                 | -> #msg+1 #ret_addr                           | w
jmp #cyc            | -> #msg+1 #ret_addr                           | w
#exit_out pop       | -> #msg #ret_addr                             |
pop                 | -> #ret_addr                                  |
jmp                 | -> _                                          |

#start
push #cyc2          | _ -> #cyc2                |
push #msg1          | -> #msg1 #cyc2
push #out           | -> #out #msg1 #cyc2
jmp                 | -> #msg1 #cyc2

#cyc2 push 2        | _ -> 2
input               | -> <flag>
push #cyc3          | -> #cyc3 <flag>
jmpe                | -> _
push #cyc2          | -> #cyc2
jmp                 | -> _

#cyc3 push 0        | -> 0
push #addr_user     | -> #addr_user 0
load                | -> #user 0
store               | -> _

push #ext3          | _ -> #cyc4                |
push #msg2          | -> #msg2 #cyc4
push #out           | -> #out #msg2 #cyc4
jmp                 | -> #msg2 #cyc4

#cyc4 push #cyc5    | _ -> #cyc5                |
push #user          | -> #user #cyc5
push #out           | -> #out #user #cyc5
jmp                 | -> #user #cyc5

#cyc5 push #ext     | _ -> #ext                |
push #msg3          | -> #msg3 #ext
push #out           | -> #out #msg3 #ext
jmp                 | -> #msg3 #ext

#ext hlt            | -> _
