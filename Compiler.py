import json
from enum import Enum

from Processor.DataMemory import DataMemory
from Processor.InstrMemory import InstrMemory
from ProgramingLanguage.Command import Command
from ProgramingLanguage.DataToken import DataToken


# RS means Row State - shortened to compact fsm define in phase III
class RS(Enum):
    STR_Begin = -1
    LabelRow = 0
    DataPlace = 1
    Instruction = 2
    C_String_List = 3
    C_String_List_end = 3.1
    Integer = 4
    LabelAddr = 5
    # NoArg = 6
    Comment = 7
    STR_End = -2


instr_list = {
    "push": True,
    "pop": True,
    "load": True,
    "store": True,
    "input": True,
    "output": True,
    "add": True,
    "if": True,
    "swap": True,
    "roll": True,
    "dup": True,
    "jmp": True,
    "jmpb": True,
    "jmpe": True,
    "ret": True,
    "or": True,
    "hlt": True
}


class Compiler:
    def __init__(self):
        self.file_name = None
        self.tokens = []

        self.data_tokens: list[DataToken] = []

        self.label_list: dict[str: int] = {}
        self.instr_mem_dump: list[Command] = []
        self.data_mem_dump: list[int] = []


        self.code_lines: list[str] = []

    def phase_i_reading(self, file_name):
        code = open(file_name, 'r')
        for line in code.readlines():
            if line.replace("\n", '') != "":
                self.code_lines.append(' '.join((line.replace("\n", '') + " \\n ").split()))
        self.file_name = file_name

    def phase_ii_fsm(self):

        fsm = {
            'init': RS.STR_Begin,
            'state': RS.STR_Begin,
            'data': False
        }

        labels = {}
        addr_data = 0
        addr_instr = 0

        for line in self.code_lines:
            word = ""
            fsm['state'] = fsm['init']

            print("\n", line)

            for sym in line:
                if sym != " ":
                    word += sym
                    continue

                print(f"FSM state: <{fsm['state']}> - <{word}>")

                if word[0] == '#' and fsm['state'] == RS.STR_Begin:
                    fsm['state'] = RS.LabelRow
                    if word not in labels:
                        labels.update({word: 1})
                    word = ""
                    continue

                if word in instr_list and fsm['state'] == RS.STR_Begin:
                    fsm['state'] = RS.Instruction
                    word = ""
                    continue
                if word in instr_list and fsm['state'] == RS.LabelRow:
                    fsm['state'] = RS.Instruction
                    word = ""
                    continue

                if word == "data" and fsm['state'] == RS.LabelRow:
                    fsm['state'] = RS.DataPlace
                    word = ""
                    continue

                if word[0] == "#" and fsm['state'] == RS.DataPlace:
                    fsm['state'] = RS.LabelAddr
                    if word not in labels:
                        labels.update({word: 1})
                    word = ""
                    continue
                if word.isdigit() and fsm['state'] == RS.DataPlace:
                    fsm['state'] = RS.Integer
                    word = ""
                    continue
                if word != "|" and fsm['state'] == RS.DataPlace:
                    fsm['state'] = RS.C_String_List
                    word = ""
                    continue
                if word == "|" and fsm['state'] == RS.DataPlace:
                    fsm['state'] = RS.Comment
                    word = ""
                    continue

                if word[0] == "#" and fsm['state'] == RS.Instruction:
                    fsm['state'] = RS.LabelAddr
                    if word not in labels:
                        labels.update({word: 1})
                    word = ""
                    continue
                if word.isdigit() and fsm['state'] == RS.Instruction:
                    fsm['state'] = RS.Integer
                    word = ""
                    continue
                if word == "|" and fsm['state'] == RS.Instruction:
                    fsm['state'] = RS.Comment
                    word = ""
                    continue

                if word != "\\0" and fsm['state'] == RS.C_String_List:
                    word = ""
                    continue
                if word == "\\0" and fsm['state'] == RS.C_String_List:
                    fsm['state'] = RS.C_String_List_end
                    word = ""
                    continue

                if word == "\\n" and fsm['state'] == RS.C_String_List_end:
                    fsm['state'] = RS.STR_End
                    word = ""
                    continue
                if word == "\\n" and fsm['state'] == RS.Integer:
                    fsm['state'] = RS.STR_End
                    word = ""
                    continue
                if word == "\\n" and fsm['state'] == RS.LabelAddr:
                    fsm['state'] = RS.STR_End
                    word = ""
                    continue

                if word == "|" and fsm['state'] == RS.C_String_List_end:
                    fsm['state'] = RS.Comment
                    word = ""
                    continue
                if word == "|" and fsm['state'] == RS.Integer:
                    fsm['state'] = RS.Comment
                    word = ""
                    continue
                if word == "|" and fsm['state'] == RS.LabelAddr:
                    fsm['state'] = RS.Comment
                    word = ""
                    continue

                if word != "\\n" and fsm['state'] == RS.Comment:
                    word = ""
                    continue
                if word == "\\n" and fsm['state'] == RS.Comment:
                    fsm['state'] = RS.STR_End
                    word = ""
                    continue
                # if instr_list[word] andzz
                print(f"\n"
                      f"fsm got unexpected transition.\n"
                      f"FSM state: <{fsm['state']}>\n"
                      f"Given word: <{word}>")

                exit(-1)

    # def phase_I_tokens(self, file_name):
    #     code = open(file_name, 'r')
    #     for line in code.readlines():
    #         for token in line.split():
    #             self.tokens.append(token)
    #         self.tokens.append("\n")
    #     self.file_name = file_name
    #
    # def phase_II_compile(self):
    #     bool_data = False
    #     bool_comment = False
    #     bool_arg = False
    #
    #     bool_empty = True
    #     data_token: DataToken = DataToken("", "", "", "", "")
    #
    #     for token in self.tokens:
    #         if token == "\n":
    #             bool_data = False
    #             bool_comment = False
    #             bool_arg = False
    #             if not bool_empty:
    #                 self.data_tokens.append(data_token)
    #             data_token: DataToken = DataToken("", "", "", "", "")
    #             bool_empty = True
    #             continue
    #
    #         bool_empty = False
    #
    #         if token[0] == "|":
    #             bool_comment = True
    #             continue
    #
    #         if bool_comment:
    #             data_token.comment += token
    #             continue
    #
    #         if token == 'data':
    #             bool_data = True
    #             continue
    #
    #         if bool_data:
    #             if token == "\\s":
    #                 token = ' '
    #             if token == "\\0":
    #                 token = '\0'
    #             data_token.data += token
    #             continue
    #
    #         if bool_arg:
    #             data_token.arg = token
    #             continue
    #
    #         if token[0] == '#':
    #             data_token.label = token
    #             continue
    #
    #         data_token.instr = token
    #         bool_arg = True
    #
    # def phase_III_extract_dumps(self):
    #     addr_data = 0
    #     addr_instr = 0
    #     for token in self.data_tokens:
    #         if token.label != "" and token.data != "":
    #             self.label_list.update({token.label: addr_data})
    #         elif token.label != "":
    #             self.label_list.update({token.label: addr_instr})
    #         if token.data != "":
    #             for data in token.data:
    #                 self.data_mem_dump.append(ord(data))
    #                 addr_data += 1
    #             continue
    #         if token.instr != "":
    #             command = Command(token.instr, token.arg)
    #             self.instr_mem_dump.append(command)
    #             addr_instr += 1
    #
    #     for com in self.instr_mem_dump:
    #         if com.arg != "" and com.arg[0] == '#':
    #             if self.label_list.get(com.arg) is not None:
    #                 com.arg = self.label_list.get(com.arg)
    #             else:
    #                 print(f"Label <{com.arg}> used but not spotted")
    #                 exit(-1)
    #
    # def phase_III_extract(self):
    #     addr_data = 0
    #     addr_instr = 0
    #
    #     fsm_list = {'label': RS.LabelRow,
    #                 'instr': RS.Instruction,
    #                 'data': RS.DataPlace,
    #                 'str': RS.C_String_List,
    #                 'int': RS.Integer,
    #                 'label_addr': RS.LabelAddr,
    #                 'no_arg': RS.NoArg,
    #                 'com': RS.Comment,
    #                 'end': RS.STR_End
    #                 }
    #
    #     fsm = {
    #         'initial': RS.STR_Begin,
    #         'state': [],
    #         'transitions': {
    #             RS.STR_Begin: {'label': RS.LabelRow, 'instr': RS.Instruction},
    #             RS.LabelRow: {'data': RS.DataPlace, 'instr': RS.Instruction},
    #             RS.DataPlace: {'str': RS.C_String_List, 'int': RS.Integer, 'label_addr': RS.LabelAddr, 'no_arg': RS.NoArg},
    #             RS.Instruction: {'int': RS.Integer, 'label_addr': RS.LabelAddr, 'no_arg': RS.NoArg},
    #             RS.C_String_List: {'com': RS.Comment, 'end': RS.STR_End},
    #             RS.Integer: {'com': RS.Comment, 'end': RS.STR_End},
    #             RS.LabelAddr: {'com': RS.Comment, 'end': RS.STR_End},
    #             RS.NoArg: {'com': RS.Comment, 'end': RS.STR_End},
    #             RS.Comment: {'end': RS.STR_End},
    #             RS.STR_End: {}
    #         }
    #     }
    #
    #     row_counter = 1
    #     for token in self.data_tokens:
    #         state = []
    #         if token.label != "":
    #             state.append("label")
    #
    #         if token.data != "":
    #             state.append("data")
    #         if token.data != "" and token.data[0] == '#':
    #             state.append("label_addr")
    #         elif token.data != "" and token.data[len(token.data)-1] == '\0':
    #             state.append("str")
    #         elif token.data != "" and token.data[len(token.data)-1] != '\0':
    #             state.append("int")
    #
    #         if token.instr != "":
    #             state.append("instr")
    #
    #         if token.arg == "" and token.data == "":
    #             state.append("no_arg")
    #         elif token.arg != "" and token.arg[0] == "#":
    #             state.append("label_addr")
    #         elif token.arg != "" and token.arg[len(token.arg)-1] != '\0':
    #             state.append("int")
    #
    #         if token.comment != "":
    #             state.append("com")
    #         state.append("end")
    #         print(state)
    #
    #         fsm['state'] = fsm['initial']
    #         counter = 0
    #         while fsm['state'] != RS.STR_End:
    #             if state[counter] in fsm['transitions'][fsm['state']]:
    #                 fsm['state'] = fsm['transitions'][fsm['state']][state[counter]]
    #                 counter += 1
    #             else:
    #                 print(f"\n"
    #                       f"Incorrect state:\n"
    #                       f"Current state: {fsm['state']}\n"
    #                       f"Expected: {fsm['transitions'][fsm['state']]}\n"
    #                       f"Wanted to: {fsm_list[state[counter]]}\n"
    #                       f"Broken row: {row_counter}\n")
    #                 exit(-1)
    #         row_counter += 1

    def phase_IV_export_dumps(self):
        dm = DataMemory()
        im = InstrMemory()

        dm.set_memory_dump(self.data_mem_dump)
        im.set_memory_dump(self.instr_mem_dump)

        with open('Data_dump.json', 'w', encoding='utf-8') as f:
            json.dump(dm.__dict__, f, ensure_ascii=False, indent=4)
        with open('Instr_dump.json', 'w', encoding='utf-8') as f:
            json.dump(im.__dict__(), f, ensure_ascii=False, indent=4)


