class Command:
    def __init__(self, instruction, argument, dm_flag=False):
        self.instr = instruction
        self.arg = argument
        self.dm_flag = dm_flag

    def __str__(self):
        return f"{self.instr}{' '*(6-len(self.instr))}<{self.arg}>"
