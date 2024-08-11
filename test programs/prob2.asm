push #start         | _ -> #start
jmp                 | -> _
hlt
hlt

#mk_sum                     | <num> <prev_num> <sum>
roll                        | -> <sum> <num> <prev_num>
swap                        | -> <num> <sum> <prev_num>
dup                         | -> <num> <num> <sum> <prev_num>
roll                        | -> <sum> <num> <num> <prev_num>
dup                         | -> <sum> <sum> <num> <num> <prev_num>
roll                        | -> <num> <sum> <sum> <num> <prev_num>
add                         | -> <sum_new> <sum> <num> <prev_num>
dup                         | -> <sum_new> <sum_new> <sum> <num> <prev_num>
push 5000000                | -> 5000000 <sum_new> <sum_new> <sum> <num> <prev_num>
if                          | -> <cmp_res> <sum_new> <sum> <num> <prev_num>
push #print                 | -> #print <cmp_res> <sum_new> <sum> <num> <prev_num>
jmpb                        | -> <sum_new> <sum> <num> <prev_num>
swap                        | -> <sum> <sum_new> <num> <prev_num>
pop                         | -> <sum> <num> <prev_num>
roll                        | -> <prev_num> <sum> <num>
roll                        | -> <num> <prev_num> <sum>
push #cyc                   | -> #cyc <num> <prev_num> <sum>
jmp                         | -> <num> <prev_num> <sum>

#print                      | <sum_new> <sum> <num> <prev_num>
pop                         | -> <sum> <num> <prev_num>
push 1                      | -> 1 <sum> <num> <prev_num>
output                      | -> <num> <prev_num>
pop                         | -> <prev_num>
pop                         | -> _
halt                        | -> _

#start
push 2                      | -> 2
push 1                      | -> 1 2
push 2                      | -> 2 1 2
#cyc dop                    | -> 2 2 1 2
roll                        | -> 1 2 2 2
add                         | -> 3 2 2
dup                         | -> 3 3 2 2
push 1                      | -> 1 3 3 2 2
or                          | -> 1or3 3 2 2
push #mk_sum                | -> #mk_sum 1or3 3 2 2
jmpe                        | -> 3 2 2
push #cyc                   | -> #cyc 3 2 2
jmp                         | -> 3 2 2

