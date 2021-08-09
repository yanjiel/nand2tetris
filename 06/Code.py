"""Translates Hack Assembly language mnemonics into binary codes"""

from Parser import A_COMMAND, C_COMMAND, L_COMMAND

COMP_HASH = {
        "0": "101010",
        "1": "111111",
        "-1": "111010",
        "D": "001100",
        "A": "110000",
        "M": "110000",
        "!D": "001101",
        "!A": "110001",
        "!M": "110001",
        "-D": "001111",
        "-A": "110011",
        "-M": "110011",
        "D+1": "011111",
        "A+1": "110111",
        "M+1": "110111",
        "D-1": "001110",
        "A-1": "110010",
        "M-1": "110010",
        "D+A": "000010",
        "D+M": "000010",
        "A+D": "000010", # to allow different order
        "M+D": "000010", # to allow different order
        "D-A": "010011",
        "D-M": "010011",
        "A-D": "000111",
        "M-D": "000111",
        "D&A": "000000",
        "D&M": "000000",
        "A&D": "000000", # to allow different order
        "M&D": "000000", # to allow different order
        "D|A": "010101",
        "D|M": "010101",
        "A|D": "010101", # to allow different order
        "M|D": "010101", # to allow different order
    }

JUMP_HASH = {
    "JGT":"001",
    "JEQ":"010",
    "JGE":"011",
    "JLT":"100",
    "JNE":"101",
    "JLE":"110",
    "JMP":"111"
}

class Code(object):
    """
    representing a Code in asm or binary
    Attribute
    command: an instance of A_COMMAND, L_COMMAND or C_COMMAND

    Property
    dest: returns the binary code of the dest mnemonic of a C_COMMAND
    comp: returns the binary code of the comp mnemonic of a C_COMMAND by looking up COMP_HASH
    jump: returns the binary code of the jump mnemonic of a C_COMMAND by looking up JUMP_HASH

    Method
    get_binary_code(): returns the str type binary code representation of self.command
    
    Static Method
    decimal_to_binary(num): takes in a positive integer number and convert it into 16 digit binary string
    """

    def __init__(self, command=None):
        # accepting None, or an instance of A_COMMAND, L_COMMAND or C_COMMAND
        if isinstance(command, (A_COMMAND, L_COMMAND, C_COMMAND)):
            self.command = command
        elif command:
            raise TypeError("command must be an instance of A_COMMAND, L_COMMAND or C_COMMAND")

    @property
    def dest(self):
        """returns the binary code of the dest mnemonic"""
        if not isinstance(self.command, C_COMMAND):
            raise TypeError("self.command must be C_COMMAND type to use the dest property")
        
        dest_asm = self.command.dest # can be str or None type
        dest_hack = ["0", "0", "0"]
        # can add implementation to check again invalid characters that are not A/D/M
        if dest_asm:
            if "A" in dest_asm:
                dest_hack[0] = "1"
            if "D" in dest_asm:
                dest_hack[1] = "1"
            if "M" in dest_asm:
                dest_hack[2] = "1"
        
        return "".join(dest_hack)
            
    @property
    def comp(self):
        """returns the binary code of the comp mnemonic"""
        if not isinstance(self.command, C_COMMAND):
            raise TypeError("self.command must be C_COMMAND type to use the comp property")

        comp_asm = self.command.comp # comp field cannot be empty or None2
        if comp_asm in ["0", "1", "-1", "D", "!D", "-D", "D+1", "D-1"] or "A" in comp_asm:
            a_flag = "0"
        elif "M" in comp_asm:
            a_flag = "1"
        else:
            raise ValueError(comp_asm + " is not a valid comp field for " + self.command)
        
        if not comp_asm in COMP_HASH:
            raise ValueError(comp_asm + " is not a valid comp field for " + self.command)
        else:
            comp_hack = COMP_HASH[comp_asm]

        comp_hack = a_flag + comp_hack
        return comp_hack

    @property
    def jump(self):
        """returns the binary code of the jump mnemonic"""
        if not isinstance(self.command, C_COMMAND):
            raise TypeError("self.command must be C_COMMAND type to use the jump property")

        jump_asm = self.command.jump # can be str or None type
        if jump_asm in JUMP_HASH:
            jump_hack = JUMP_HASH[jump_asm]
        else:
            jump_hack  = "000"

        return jump_hack

    @staticmethod
    def decimal_to_binary(num):
        """converts a positive integer number that represents an address in RAM/ROM into it's binary presentation"""
        try:
            num = int(num)
        except:
            raise
        
        if num < 0 or num > 32767:
            raise ValueError("input decimal needs to be between [0, 32767] for addressing purposes") #ROM address ends at 32767 in hack
        elif num > 1:
            place = num % 2
            num = num // 2
            rslt = Code.decimal_to_binary(num)
            rslt.append(place)
            return rslt
        else:
            return [num]

    def get_binary_code(self, sym_hash_table={}):
        """return the binary code for assembly code that's a A_COMMAND or C_COMMAND"""

        if isinstance(self.command, A_COMMAND):
            # when the command is a A_COMMAND
            num_sym_label = self.command.num_sym_label

            # if indirect addressing is used then translate the indirect addresses to direct addresses ;
            # if direct addressing is used then get the direct address
            if not num_sym_label.isdigit(): # then it means that it is not direct addressing @LOOP or @sum
                if num_sym_label not in sym_hash_table:
                    raise ValueError("Label or variable " + num_sym_label + " is not the sym_hash_table provided.")
                else:
                    num = sym_hash_table[num_sym_label] # loop up the LABEL or variable from hash table
            else:
                num = int(num_sym_label) # get the decimal directly from direct addressing
            
            binary_list = self.decimal_to_binary(num) # can be 1-15 digits
            if len(binary_list) > 15: # 2^15 = 32768 max addresses in ROM(RAM32K), 24576 max address in Memory (RAM16K+RAM8K+1)
                raise ValueError("Decimal " + str(num) + "in " + self.command + "is invalid (larger than 32767)")    
            
            binary = "0" + (15 - len(binary_list))*"0"+ ("").join(map(str, binary_list)) # 1+15 = 16 bits
            return binary

        elif isinstance(self.command, C_COMMAND):
            # when the command is a C_COMMAND
            binary = "111" + self.comp + self.dest + self.jump # 3+7+3+3 = 16 bits
            return binary

        # elif isinstance(self.command, L_COMMAND):
        #     # we should not encounter any L_COMMAND for binary code translation
        #     binary = "L"*16
        #     return binary
        
        else:
            raise TypeError("self.command should be either A_COMMAND, or C_COMMAND")


def test():
    """for debugging, please ignore"""
    for comm in [A_COMMAND("16383"), A_COMMAND("16384"), A_COMMAND("24576"), L_COMMAND("sum"), C_COMMAND(dest="AM",comp="M-1", jump=None), C_COMMAND(dest=None,comp="0", jump="JMP"), C_COMMAND(dest="M",comp="D", jump=None), C_COMMAND(dest="D",comp="A", jump=None)]:
        print(comm)
        cd = Code(comm)
        print(cd.get_binary_code())


if __name__ == "__main__":
    pass
    