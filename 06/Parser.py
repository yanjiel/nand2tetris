"""Break each assembly command into its underlying components (fields and symbols)"""
import re


class A_COMMAND(object):
    """
    representation of an addressing command @Xxx
    Attribute
    num_sym_label: the Xxx in @Xxx, which can be an integer number, a symbol (variable), or a label
    """
    def __init__(self, num_sym_label=None):
        if num_sym_label:
            if not isinstance(num_sym_label, str):
                num_sym_label = str(num_sym_label)
            self.num_sym_label = num_sym_label
        else:
            self.num_sym_label = None
    
    def __repr__(self):
        return "A_COMMAND:" + self.num_sym_label if self.num_sym_label else "A_COMMAND:None"

class L_COMMAND(object):
    """
    representation of a labeling command (Xxx)
    Attribute
    label: the Xxx in (Xxx), which is a label
    """
    def __init__(self, label=None):
        if label:
            if not isinstance(label, str):
                label = str(label)
            self.label = label
        else:
            self.label = None

    def __repr__(self):
        return "L_COMMAND:" +  self.label if self.label else "L_COMMAND:None"

class C_COMMAND(object):
    """
    representation of a compute command dest=comp;jump, where dest and jump can be empty
    Attribute
    dest: dest field in dest=comp;jump
    comp: comp field in dest=comp;jump
    jump: jump field in dest=comp;jump
    """
    def __init__(self, comp, dest=None, jump=None):
        if comp:
            self.comp = comp
        else:
            raise ValueError("comp field of a C_COMMAND cannot be empty or None")

        if dest:
            self.dest = dest
        else:
            self.dest = None

        if jump:
            self.jump = jump
        else:
            self.jump = None

    def __repr__(self):
        str_out = "C_COMMAND:" + self.dest if self.dest else "C_COMMAND:None" 
        str_out += "=" + self.comp + ";" + self.jump if self.jump else "=" + self.comp + ";None"
        return str_out

class Parser(object):
    """Parser for converting assembley language code into binary machine code
    Attribute
    comm_lst: a list of str elements each represent a line of code in the assembly code file
    crt_code: a str element of comm_lst which is to be parsed by the parser next
    crt_comm: an instance of A_COMMAND, C_COMMAND or L_COMMAND that is converted from self.crt_code using get_command method

    Method
    hasMoreCommands(): returns a Boolean indicating whether there's more commands left to be parsed
    advance(): parser continues to process the next command in self.comm_lst, and put that command into self.crt_code
    get_command(sym_hash_table): takes in a hash table of mapped labels and variables for the assembly language, and converts 
                                 self.crt into a corresponding instance of A_COMMAND, L_COMMAND, or C_COMMAND which is put in self.crt_comm

    Static Method
    removeWhiteSpace(str_in): takes in str_in str type of commands with each line separated by "\n", then removes all the whitespaces and comments, and returns a list of clean asm code in str type.
    """
    def __init__(self, file=None):
        """opens the input file/stream and gets ready to parse it"""
        
        if not file:
            self.comm_lst = None
        else:
            # handle different types of input, file as an invalid input that not str type, as an .asm file path, or as a string content of an .asm
            if not isinstance(file, str):
                raise TypeError("input file must be of str type")

            elif file.endswith(".asm"):
                # file is an asm file
                try:
                    f= open(file)
                    str_in = f.read()
                    f.close
                except Exception as e:
                    raise e
                self.comm_lst = self.removeWhiteSpace(str_in) # returns a list of commands

            else:
                # file is a string of commands
                self.comm_lst = self.removeWhiteSpace(file)

        self.crt_code = None
        self.crt_comm = None

    def hasMoreCommands(self):
        """return a boolean variable indicating whether there are more commands in the input file"""
        if self.comm_lst:
            return True
        else:
            return False

    def advance(self):
        """reads the next command from the input. Called only where hasMoreCommand returns true"""
        if self.hasMoreCommands():
            self.crt_code = self.comm_lst.pop(0)

    def get_command(self, sym_hash_table={}):
        """returns an instance of these custom command classes: A_COMMAND, C_COMMAND, L_COMMAND"""
        if not self.crt_code:
            return None
        
        # categorizing into A/C/L commands
        if self.crt_code.startswith("@"):
            # A Command
            num_sym_label = self.crt_code.replace("@","")
            if not num_sym_label:
                raise SyntaxError(self.crt_code + " is not a valid command")

            if num_sym_label.isdigit():
                # Direct Addressing
                self.crt_comm = A_COMMAND(num_sym_label)
                return self.crt_comm # store decimal as string
            else:
                # Indirect Addressing
                if num_sym_label not in sym_hash_table:
                    raise ValueError("Label or variable " + num_sym_label + " in L_Command " + self.crt_code + " is not the sym_hash_table provided.")
                else:
                    addrs = sym_hash_table[num_sym_label] # addr will be an int; sym can be a variable like @i or a label like @LOOP
                    self.crt_comm = A_COMMAND(str(addrs)) # so that address int 0 will be converted to "0"
                return self.crt_comm

        elif self.crt_code.startswith("(") and self.crt_code.endsswith(")"):
            # L Command
            label = self.crt_code.replace("(","")
            label = self.crt_code.replace(")","")

            if not label:
                raise SyntaxError(self.crt_code + " is not a valid command")
            
            self.crt_comm  = L_COMMAND(label)
            return self.crt_comm

        else:
            # C command or Invalid Command
            # Handling invalid commands that does not include '=' or ';'
            if not self.crt_code.find("=") and not self.crt_code.find(";"):
                raise SyntaxError(self.crt_code + " is not a valid command")
            
            # Handling valid C Command
            if "=" in self.crt_code:
                dest, comp_jump = self.crt_code.split("=")
                if ";" in comp_jump:
                    comp, jump = comp_jump.split(";")
                else:
                    comp, jump = comp_jump, None
            else:
                dest = None
                comp, jump = self.crt_code.split(";")
            
            self.crt_comm = C_COMMAND(comp=comp, dest=dest, jump=jump)
            return self.crt_comm

    @staticmethod
    def removeWhiteSpace(str_in):
        """
        This function removes white spaces and comments from a file or file handler of str type, and output a list of commands of str type
        White spaces removed include tab, spaces and blank lines
        Comments removed include those start with // and end with a new line, or those start with /* and end with */
        
        :param: an assembly code input file of str type, with comments and whitespaces
        :returns: a list of str type elements, with each representing a line of assembly code without comment or whitespace
        """
        if not isinstance(str_in, str):
            raise TypeError("input must be of str type")

        # remove two types of comments from the file content
        str_in = re.sub(r"//.+\n", "\n", str_in)
        str_in = re.sub(r"/\*[\d\D]*?\*/\n", "", str_in)

        lst_out = [] # initiating the output list to be empty
        # remove any white spaces line by line
        for line in str_in.splitlines():
            line_new = re.sub(r"\s+", "", line)
            if line_new:
                lst_out.append(line_new)
    
        return lst_out
    
def test():
    """for debugging, please ignore"""
    DEFAULT_TABLE = {
    "SP":0,
    "LCL":1,
    "ARG":2,
    "THIS":3,
    "THAT":4,
    "R0":0,
    "R1":1,
    "R2":2,
    "R3":3,
    "R4":4,
    "R5":5,
    "R6":6,
    "R7":7,
    "R8":8,
    "R9":9,
    "R10":10,
    "R11":11,
    "R12":12,
    "R13":13,
    "R14":14,
    "R15":15,
    "SCREEN": 16384,
    "KBD": 24576
    }
    for fname in [r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\06\pong\PongL.asm"]:
        psr = Parser(fname)
        while psr.hasMoreCommands():
            psr.advance()
            comm = psr.get_command(DEFAULT_TABLE)
            if isinstance(comm, A_COMMAND):
                print(comm.num_sym_label)
            elif isinstance(comm, C_COMMAND):
                print(comm.dest, comm.comp, comm.jump)
            
if __name__ == "__main__":
    pass