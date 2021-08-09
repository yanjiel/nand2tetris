"""
Handles the parsing of a single .vm file, and encapsulates access to the input code. 
It reads VM commands, parses them, and provides convenient access to their components. 
In addition, it removes all white space and comments.
"""
import re

class C_ARITHMETIC(object):
    """
    representation of an arithmetic command in VM language
    Class Attribute
    OPS: predefined set for accepted arithmetic command types: "add","sub","neg","eq","gt","lt","and","or","not"

    Attribute
    arg1: for arithmetic command, arg1 is the comamnd symbol itself
    """
    OPS = ("add","sub","neg","eq","gt","lt","and","or","not")
    def __init__(self, arg1):
        if not isinstance(arg1, str):
            raise TypeError("arg1 needs to be str type")
        else:
            if arg1 not in self.OPS:
                raise ValueError("arg1 for C_ARITHMETIC command needs to be one of", self.OPS)
            else:
                self.arg1 = arg1
    
    def __repr__(self):
        return "C_ARITHMETIC: " + self.arg1

class C_PUSH(object):
    """
    representation of a push command in VM language
    
    Attribute
    arg1: one of the 8 memory segment in VM, like the local in 'push local 2'
    arg2: the positive integer number for index in a push command in VM, like the 2 in 'push local 2'
    """
    def __init__(self, arg1, arg2):
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise TypeError("arg1 and arg2 both need to be str type")
        
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __repr__(self):
        return "C_PUSH: " + self.arg1 + " " +  self.arg2

class C_POP(object):
    """
    representation of a pop command in VM language
    
    Attribute
    arg1: one of the 8 memory segment in VM, like the temp in 'pop temp 0'
    arg2: the positive integer number for index in a push command in VM, like the 0 in 'pop temp 0'
    """
    def __init__(self, arg1, arg2):
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise TypeError("arg1 and arg2 both need to be str type")
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __repr__(self):
        return "C_PUSH: " + self.arg1 + " " + self.arg2

class C_LABEL(object):
    """
    representation of a label declaration command in VM language
    
    Attribute
    arg1: the command mnemonics (label)
    arg2: the name of the label declared
    """
    def __init__(self, arg1, arg2):
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise TypeError("arg1 and arg2 both need to be str type")
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __repr__(self):
        return "C_LABEL: " + self.arg1 + " " +  self.arg2

class C_GOTO(object):
    """
    representation of a goto command in VM language
    
    Attribute
    arg1: the command mnemonics (goto)
    arg2: the `labelxx` in goto labelxx
    """
    def __init__(self, arg1, arg2):
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise TypeError("arg1 and arg2 both need to be str type")
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __repr__(self):
        return "C_GOTO: " + self.arg1 + " " +  self.arg2

class C_IF(object):
    """
    representation of a if-goto command in VM language
    
    Attribute
    arg1: the command mnemonics (if-goto)
    arg2: the `labelxx` in if-goto labelxx
    """
    def __init__(self, arg1, arg2):
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise TypeError("arg1 and arg2 both need to be str type")
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __repr__(self):
        return "C_IF: " + self.arg1 + " " +  self.arg2

class C_FUNCTION(object):
    """
    representation of a function declaration command in VM language
    
    Attribute
    arg1: function name in str
    arg2: nLocals, number of local variables in str
    """
    def __init__(self, arg1, arg2):
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise TypeError("arg1 and arg2 both need to be str type")
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __repr__(self):
        return "C_FUNCTION: function " + self.arg1 + " " +  self.arg2

class C_RETURN(object):
    """
    representation of a function declaration command in VM language
    Attribute
    arg1: command name, "return"
    """
    def __init__(self, arg1):
        if not isinstance(arg1, str):
            raise TypeError("arg1 needs to be str type")
        self.arg1 = arg1

    def __repr__(self):
        return "C_RETURN:" + self.arg1

class C_CALL(object):
    """
    representation of a function declaration command in VM language
    
    Attribute
    arg1: function name in str
    arg2: nArguments, number of arguments passed into callee
    """
    def __init__(self, arg1, arg2):
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise TypeError("arg1 and arg2 both need to be str type")
        self.arg1 = arg1
        self.arg2 = arg2
    
    def __repr__(self):
        return "C_CALL: call " + self.arg1 + " " +  self.arg2


class Parser(object):
    """
    Class for parsing a single .vm file
    Atrribute
    comm_lst: list of .vm codes with each element representing a single line of code
    crt_code: the current line of code in the .vm file
    crt_comm: the current line of code instiated into its corresponding instance of "C_ARITHMETIC", "C_POP" or "C_PUSH" (other command types are not supported yet).

    Property
    arg1: in push/pop commands arg1 is the segment symbol; in arithmetic commands, arg1 is the comamnd itself
    arg2: in push/pop commands arg2 is the integer index; arg2 is not defined for arithmetic commands

    Method
    removeWhiteSpace(str_in): removes the whitespace and commands in the source .vm file
    hasMoreCommands(): returns a Boolean indicating if there's more code to parse in self.comm_lst
    advance():reads the next command from the input by poping the next in comm_lst into self.crt_code
    get_command(): returns the corresponding instance of C_ARITHMETIC, C_PUSH, C_POP for the current line of .vm code in self.crt_code
    """
    def __init__(self, file=None):
        """Opens the input file/stream and gets ready to parse it."""
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
                self.comm_lst = self.removeWhiteSpace(file) ####?????????????????????????????????????????????????

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

    @property
    def arg1(self):
        """
        Returns the first argument of the current command. In the case of C_ARITHMETIC, the command itself (add, sub, etc.) is returned. 
        Should not be called if the current command is C_RETURN.
        """
        # right now we only support C_ARITHMETIC
        if isinstance(self.crt_comm, C_RETURN):
            raise SyntaxError("arg1 property cannot be called on C_RETURN commands", self.crt_comm)

        return self.crt_comm.arg1
    
    @property
    def arg2(self):
        """
        Returns the second argument of the current command. Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.
        """
        # right now we only support C_PUSH and C_POP
        if not isinstance(self.crt_comm, (C_POP, C_PUSH)):
            raise SyntaxError("arg2 property cannot be called on C_PUSH or C_POP commands", self.crt_comm)

        return self.crt_comm.arg2

    def get_command(self, table={}):
        "returns an instance of C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL"

        if self.crt_code in C_ARITHMETIC.OPS: # it is a C_ARITHMETIC command
            comm = C_ARITHMETIC(arg1=self.crt_code) 
        
        elif self.crt_code.startswith("push"): # then it is a C_PUSH command
            arg12 = self.crt_code[4:].strip() # remove the push
            arg1 = "".join([x for x in arg12 if not x.isdigit()])
            arg2 = "".join([x for x in arg12 if x.isdigit()])
            comm = C_PUSH(arg1=arg1, arg2=arg2)

        elif self.crt_code.startswith("pop"):
            arg12 = self.crt_code[3:].strip()
            arg1 = "".join([x for x in arg12 if not x.isdigit()])
            arg2 = "".join([x for x in arg12 if x.isdigit()])
            comm = C_POP(arg1=arg1, arg2=arg2)
        
        elif self.crt_code.startswith("label"):
            #crt_code = "labelCOMPUTE_ELEMENT"
            arg1 = "label"
            arg2 = self.crt_code[5:].strip()
            comm = C_LABEL(arg1=arg1, arg2=arg2)

        elif self.crt_code.startswith("goto"):
            arg1 = "goto"
            arg2 = self.crt_code[4:].strip()
            comm = C_GOTO(arg1=arg1, arg2=arg2)

        elif self.crt_code.startswith("if-goto"):
            arg1 = "if-goto"
            arg2 = self.crt_code[7:].strip()
            comm = C_IF(arg1=arg1, arg2=arg2)

        elif self.crt_code.startswith("function"):
            #crt_code = "functionSimpleFunction.test2" ##################### HAVE TO RE-WRITE PARSER AND REMOVE WHITE SPACE SUCH THAT WHITESPACE BETWEEN WORDS ARE NOT REMOVED
            arg12 = self.crt_code[8:].strip()
            arg2 = "".join([x for x in arg12 if x.isdigit()]) ###################### functionname can contain numeric
            arg1 = arg12[:-len(arg2)].strip() ###########################
            comm = C_FUNCTION(arg1=arg1, arg2=arg2)

        elif self.crt_code.startswith("return"):
            arg1 = "return"
            comm = C_RETURN(arg1=arg1)

        elif self.crt_code.startswith("call"):
            #callMain.fibonacci1
            arg12 = self.crt_code[4:]
            arg1 = "".join([x for x in arg12 if not x.isdigit()]) # Main.fibonacci, which later will be labeled FibonacciElement.Main.fibonacci
            arg2 = "".join([x for x in arg12 if x.isdigit()]) ####################################
            comm = C_CALL(arg1=arg1, arg2=arg2)

        else:
            # we do not accept other types yet
            raise ValueError("currently we do not support commands other than arithmetic, push, pop, label, goto, if-goto and function")
            
        self.crt_comm = comm
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

        # str_in = str_in.lower() # convert all commands into lower cases
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






def testPleaseIgnore():
    """for testing purposes please ignore"""
    fname = r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\07\StackArithmetic\SimpleAdd\SimpleAdd.vm"
    fname = r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\07\StackArithmetic\StackTest\StackTest.vm"
    with open(fname) as f:
        comm_lst = Parser().removeWhiteSpace(f.read())
    psr = Parser("\n".join(comm_lst))
    while psr.hasMoreCommands():
        psr.advance()
        #print(psr.crt_code)
        print(psr.get_command())
    


if __name__ == "__main__":
    pass