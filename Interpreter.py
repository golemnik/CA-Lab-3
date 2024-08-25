from ProgramingLanguage.Command import Command
from ProgramingLanguage.DataToken import DataToken


class Interpeter:
    def __init__(self):
        self.tokens = []

        self.data_tokens: list[DataToken] = []

        self.instr_mem_dump: list[Command] = []
        self.data_mem_dump: list[int] = []
        self.data_labels_list: dict[str: int] = {}
        self.instr_labels_list: dict[str: int] = {}

    def phase_I_tokens(self, file_name):
        code = open(file_name, 'r')
        for line in code.readlines():
            for token in line.split():
                self.tokens.append(token)
            self.tokens.append("\n")

    def phase_II_interpretate(self):
        bool_data = False
        bool_comment = False
        bool_arg = False

        bool_empty = True
        data_token: DataToken = DataToken("", "", "", "", "")

        for token in self.tokens:
            if token == "\n":
                bool_data = False
                bool_comment = False
                bool_arg = False
                if not bool_empty:
                    self.data_tokens.append(data_token)
                data_token: DataToken = DataToken("", "", "", "", "")
                bool_empty = True
                continue

            bool_empty = False

            if token[0] == "|":
                bool_comment = True
                continue

            if bool_comment:
                data_token.comment += token
                continue

            if token == 'data':
                bool_data = True
                continue

            if bool_data:
                if token == "\\s":
                    token = ' '
                if token == "\\0":
                    token = '\0'
                data_token.data += token
                continue

            if bool_arg:
                data_token.arg = token
                continue

            if token[0] == '#':
                data_token.label = token
                continue

            data_token.instr = token
            bool_arg = True

    def phase_III_export_dumps(self):
        addr_data = 0
        addr_instr = 0
        for token in self.data_tokens:
            if token.label != "" and token.data != "":
                self.data_labels_list.update({token.label: addr_data})
            elif token.label != "":
                self.instr_labels_list.update({token.label: addr_instr})
            if token.data != "":
                for data in token.data:
                    self.data_mem_dump.append(ord(data))
                    addr_data += 1
                continue
            if token.instr != "":
                command = Command(token.instr, token.arg)
                self.instr_mem_dump.append(command)
                addr_instr += 1

        # for com in self.instr_mem_dump:
        #     if com.arg != "" and com.arg[0] == '#':
        #         if self.data_labels_list.get(com.arg) is not None:
        #             com.arg = self.data_labels_list.get(com.arg)
        #             com.dm_flag = True
        #         else:
        #             com.arg = self.instr_labels_list.get(com.arg)

    def phase_IV_export_instr(self):
        pass
