from ProgramingLanguage.DataToken import DataToken


class DataTokenPrinter:
    def print_tokens(self, tokens: list[DataToken]):

        max_label = max([len(t.label) for t in tokens])+1
        max_instr = max([len(t.instr) for t in tokens])+1
        max_arg = max([len(t.arg) for t in tokens])+1
        max_data = max([len(t.data) for t in tokens])+1
        max_comm = max([len(t.comment) for t in tokens])+1

        mx = [max_label, max_instr, max_arg, max_data, max_comm]

        print(f" Label{' ' * (max_label-6)}"
              f"| Instr{' ' * (max_instr-6)}"
              f"| Arg{' ' * (max_arg-4)}"
              f"| Data{' ' * (max_data-5)}"
              f"| Comment{' ' * (max_comm-7)}")

        print(f"{'-' * max_label}"
              f"|{'-' * max_instr}"
              f"|{'-' * max_arg}"
              f"|{'-' * max_data}"
              f"|{'-' * max_comm}")
        for token in tokens:
            self.print_token(token, mx)

    def print_token(self, token: DataToken, mx):
        print(f"{token.label + ' ' * (mx[0] - len(token.label))}"
              f"|{token.instr + ' ' * (mx[1] - len(token.instr))}"
              f"|{token.arg + ' ' * (mx[2] - len(token.arg))}"
              f"|{token.data + ' ' * (mx[3] - len(token.data))}"
              f"|{token.comment + ' ' * (mx[4] - len(token.comment))}"
              )
