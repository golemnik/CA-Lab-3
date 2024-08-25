class DataToken:
    def __init__(self, label: str, instruction: str, argument: str, data: str, comment: str):
        self.label: str = label
        self.instr: str = instruction
        self.arg: str = argument
        self.data: str = data
        self.comment: str = comment
