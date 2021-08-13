"""Translate VM commands into Hack assembly code"""

import os
from Parser import C_ARITHMETIC, C_CALL, C_FUNCTION, C_GOTO, C_IF, C_LABEL, C_PUSH, C_POP, C_RETURN

class CodeWriter(object):
    """
    Class to transalte VM language into Hack assembly
    Class Attribute
    LABEL_CTR: counter for labels declared in an .asm file
    LOOKUP_TABLE: hash table for 4 of the VM memory segment symbol and it's corresponding Hack memory symbol pairs

    Attribute
    file_lst: the list of input .vm file paths
    fname_out: the name of the output .asm file
    f_handler: the file handler for the output .asm file
    crt_fname, the name of the current .vm file, used in case a collection of .vm files were to be processed
    
    Method
    setFileName(fileName): informs the code write that the translation of a new .VM file is started by setting self.crt_fname to the path of the .vm file being processed
    writeArithmetic(command): writes the assembly code that is the translation of the given arithmetic command into self.f_handler
    writePushPop(command): writes the assembly code that is the translation of the given push/pop command into self.f_handler
    Close(): finish writing to the output .asm file and close the file handler self.f_handler
    """
    LABEL_CTR = 0 # used in arithmetic VM commands where loops are used and labels are declared
    LOOKUP_TABLE = {
        "local": "LCL",
        "argument": "ARG",
        "this":"THIS",
        "that":"THAT",
    }
    LABELS_CREATED = {} # used to keep track of all the labels declared

    def __init__(self, fpath=None):
        """opens the output file/stream and gets ready to write into it"""
        
        self.file_lst = [] # to hold the list of .vm files to process in case the input is a program (collection of .vm files)
        self.fname_out = ""
        self.f_handler = None # file handler to write to self.fname_out
        self.crt_fname = None
        self.crt_fname_short = None
        self.folder_file = None
        
        # get the file name for the output .hack (self.fname_out), and the list of .vm files to be processed (self.file_lst)
        if os.path.isdir(fpath): 
            # if we're dealing with a program, a collection of vm files
            for fname in os.scandir(fpath):
                if fname.path.endswith(".vm"): # fname.path is the path for the sub-directory files
                    self.file_lst.append(fname.path)
            
            # there's a chance that a folder name is passed in where there's only one .vm file in the folder
            # in this case, we'll still use a foldername.filename as padding for all the labels and variables
            if len(self.file_lst) > 1 and not (fpath + "\\Sys.vm") in self.file_lst:
                raise RuntimeError("More than one .vm file detected in folder %s, please make sure there's a Sys.vm file under the folder too." % (fpath)) 

            self.folder_name = fpath.split("\\")[-1]
            self.fname_out = fpath + "\\" + self.folder_name + ".asm" # the output file name

        elif os.path.isfile(fpath):
            # if we're dealing with a signle .vm file
            if not fpath.endswith(".vm"):
                raise TypeError("please input only .vm file paths or folders containing .vm files")
            
            self.file_lst.append(fpath)
            self.folder_name = ""
            self.fname_out = fpath.replace(".vm", ".asm") # the output file name
            
        else:
            raise TypeError("fpath either needs to be a folder path or a file path in str type")

        self.f_handler = open(self.fname_out, "w")

    def setFileName(self, fileName):
        """informs the code write that the translation of a new .VM file is started"""
        if fileName not in self.file_lst:
            raise ValueError("cannot set fileName to files other than", self.file_lst)
        self.crt_fname = fileName

        self.crt_fname_short = self.crt_fname.split("\\")[-1].replace(".vm","") # this is the short file name for the current .vm file that's beeing translated
        # get the foldername.shortfilename padding that will be used to distinguish functions and labels
        if self.folder_name:
            self.folder_file = self.folder_name + "." + self.crt_fname_short
        else:
            self.folder_file = self.crt_fname_short
        
    def writeArithmetic(self, command):
        """writes the assembly code that is the translation of the given arithmetic command"""
        # command will be a C_ARITHMETIC instance
        if not isinstance(command, C_ARITHMETIC):
            raise TypeError("command must either be C_PUSH or C_POP command instance")
        
        arg1 = command.arg1 # arg1 in ("add","sub","neg","eq","gt","lt","and","or", "not")
        # get the corresponding .asm command for the arithmetic .vm command
        if arg1 == "add":
            comm_lst = ['@SP','AM=M-1','D=M','A=A-1','M=M+D']
            asm = "\n".join(comm_lst) + "\n"
            
        elif arg1 == "sub":
            comm_lst = ['@SP','AM=M-1','D=M','A=A-1','M=M-D']
            asm = "\n".join(comm_lst) + "\n"

        elif arg1 == "neg":
            comm_lst = ['@SP','A=M-1','M=-M']
            asm = "\n".join(comm_lst) + "\n"

        elif arg1 == "eq":
            # since there will be one LABEL declared/defined for each one occurence of the eq command, each LABEL needs to be distinguishable from other LABELs (numbered)
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@CONT_%s\nD;JEQ\n@SP\nA=M-1\nM=0\n(CONT_%s)\n" % (self.LABEL_CTR, self.LABEL_CTR)
            self.LABEL_CTR += 1

        elif arg1 == "gt":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@CONT_%s\nD;JGT\n@SP\nA=M-1\nM=0\n(CONT_%s)\n" % (self.LABEL_CTR, self.LABEL_CTR)
            self.LABEL_CTR += 1

        elif arg1 == "lt":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@CONT_%s\nD;JLT\n@SP\nA=M-1\nM=0\n(CONT_%s)\n" % (self.LABEL_CTR, self.LABEL_CTR)
            self.LABEL_CTR += 1

        elif arg1 == "and":
            comm_lst = ['@SP','AM=M-1','D=M','A=A-1','M=D&M']
            asm = "\n".join(comm_lst) + "\n"
            
        elif arg1 == "or":
            comm_lst = ['@SP','AM=M-1','D=M','A=A-1','M=D|M']
            asm = "\n".join(comm_lst) + "\n"

        elif arg1 == "not":
            comm_lst = ['@SP','A=M-1','M=!M']
            asm = "\n".join(comm_lst) + "\n"

        self.f_handler.write(asm)

    def writePushPop(self, command, segment=None, index=None):
        """writes the assembly code that is the translation of the given C_PUSH or C_POP command"""
        # command will be a C_POP or C_PUSH instance
        if not isinstance(command, (C_PUSH, C_POP)):
            raise TypeError("command must either be C_PUSH or C_POP command instance")

        arg1, arg2 = command.arg1, command.arg2 # both are str type # push constant 2, so arg1 = "constant", arg2 = "2"

        if arg1 in self.LOOKUP_TABLE:
            # if pop/push local/argument/this/that int_num
            memory_mne = self.LOOKUP_TABLE[arg1] # get the memory mnemonic for local/argument/this/that VM memory segments

            if isinstance(command, C_PUSH):
                asm = "@%s\nD=M\n@%s\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" %(memory_mne, arg2)
            else: # then command must be C_POP type
                asm = "@%s\nD=M\n@%s\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n" %(memory_mne, arg2)
        
        elif arg1 == "constant":
            if isinstance(command, C_PUSH):
                # handling push constant n
                asm = "@%s\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" %(arg2)
            else:
                # no pop constant command
                pass
    
        elif arg1 == "temp":
            if isinstance(command, C_PUSH):
                # temp starts at memory location 5, so push/pop temp n is the same as push/pop memory location 5+n
                asm = "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" %(int(arg2)+5)
            else:
                asm = "@SP\nAM=M-1\nD=M\n@%s\nM=D\n" %(int(arg2)+5)
        
        elif arg1 == "static":
            # for a push/pop static 5, 5 is translated into a symbol Xxxx.5 where Xxxx is the file name
            path_seg = self.crt_fname.split("\\")
            sym_name = path_seg[-1].replace("vm", str(arg2)) #Main.5
            
            if isinstance(command, C_PUSH):
                asm = "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" %(sym_name)
            else:
                asm = "@SP\nAM=M-1\nD=M\n@%s\nM=D\n" %(sym_name)

        elif arg1 == "pointer":
            # then arg2 = 0 or 1
            if arg2 == "0":
                var_2 = "THIS"
            elif arg2 == "1":
                var_2 = "THAT"
            else:
                raise ValueError("push/pop pointer index commands must have index = 0 or 1")

            if isinstance(command, C_PUSH):
                asm = "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" %(var_2)
            else:
                asm = "@SP\nAM=M-1\nD=M\n@%s\nM=D\n" %(var_2)

        else:
            raise ValueError("we support only 8 segments", ["argument","local","static","constant","this","that","pointer","temp"])

        self.f_handler.write(asm)
    
    def writeLabel(self, command):
        if not isinstance(command, C_LABEL):
            raise TypeError("command must be C_LABEL command instance")

        arg1, arg2 = command.arg1, command.arg2 # both are str type
        # get the foldername.shortfilename.label, which will be used to determine the distinct label that's been padded with foldername.shortfilename
        if self.folder_name:
            folder_file_label = self.folder_name + "." + self.crt_fname.split("\\")[-1].replace(".vm","") + "." + arg2.upper() 
        else:
            folder_file_label = self.crt_fname.split("\\")[-1].replace(".vm","") + "." + arg2.upper()

        # look up the distinct label name from all the symbols table created, or create a new one
        if folder_file_label in self.LABELS_CREATED:
            label = self.LABELS_CREATED[folder_file_label]
        else:
            label = folder_file_label
            self.LABELS_CREATED[folder_file_label] = label #FibonnaciElement.Main.LOOP: FibonnaciElement.Main.LOOP2
        
        asm = "(%s)\n" %(label)
        self.f_handler.write(asm)
        
    def writeGoto(self, command):
        if not isinstance(command, C_GOTO):
            raise TypeError("command must be C_GOTO command instance")

        arg1, arg2 = command.arg1, command.arg2 # both are str type
        # get the foldername.shortfilename.label, which will be used to determine the distinct label that's been padded with foldername.shortfilename
        if self.folder_name:
            folder_file_label = self.folder_name+"."+self.crt_fname.split("\\")[-1].replace(".vm","")+"."+arg2.upper() #FibonnaciElement.Main.LOOP
        else:
            folder_file_label = self.crt_fname.split("\\")[-1].replace(".vm","")+"."+arg2.upper() #BasicLoop.LOOP_START

        # look up the distinct label name from all the symbols table created, or create a new one
        if folder_file_label in self.LABELS_CREATED:
            label = self.LABELS_CREATED[folder_file_label]
        else:
            label = folder_file_label
            self.LABELS_CREATED[folder_file_label] = label #FibonnaciElement.Main.LOOP: FibonnaciElement.Main.LOOP2
        
        asm = "@%s\n0;JMP\n" %(label)
        self.f_handler.write(asm)

    def writeIf(self, command):
        if not isinstance(command, C_IF):
            raise TypeError("command must be C_IF command instance")

        arg1, arg2 = command.arg1, command.arg2 # both are str type
        # get the foldername.shortfilename.label, which will be used to determine the distinct label that's been padded with foldername.shortfilename
        if self.folder_name:
            folder_file_label = self.folder_name + "." + self.crt_fname.split("\\")[-1].replace(".vm","") + "." + arg2.upper()
        else:
            folder_file_label = self.crt_fname.split("\\")[-1].replace(".vm","") + "." + arg2.upper()

        # look up the distinct label name from all the symbols table created, or create a new one
        if folder_file_label in self.LABELS_CREATED:
            label = self.LABELS_CREATED[folder_file_label]
        else:
            label = folder_file_label
            self.LABELS_CREATED[folder_file_label] = label #FibonnaciElement.Main.LOOP: FibonnaciElement.Main.LOOP2
        
        asm = "@SP\nAM=M-1\nD=M\n@%s\nD;JNE\n" %(label)
        self.f_handler.write(asm)
    
    def writeFunction(self, command):
        """This is for function declaration"""
        if not isinstance(command, C_FUNCTION):
            raise TypeError("command must be C_FUNCTION command instance")

        arg1, arg2 = command.arg1, command.arg2 # both are str type
        
        # get folder_file_funcnam, which is the foldername.filename padded function name
        if self.crt_fname_short in arg1: 
            arg1 = arg1.replace(self.crt_fname_short,"")
        folder_file_funcname = self.folder_file + arg1

        # get func_label, the distinct label for the function being declared, either from lookup existing, or creating a new one
        if folder_file_funcname in self.LABELS_CREATED:
            func_label = self.LABELS_CREATED[folder_file_funcname]
        else:
            func_label = folder_file_funcname
            self.LABELS_CREATED[folder_file_funcname] = func_label # FibonnaciElement.Main.fibonacci: FibonacciElement.Main.fibonacci
        
        # get k number of local variables or the times that local variabels are pushed with 0
        k = int(arg2)
        # get the loop label and loop end label
        loop_label = func_label + ".declare.loop" 
        end_label = func_label + ".declare.end"

        asm_pushlocal = "@SP\nA=M\nM=0\n@SP\nM=M+1"
        asm="(%s)\n@%s\nD=A\n(%s)\n@%s\nD;JLE\n%s\nD=D-1\n@%s\n0;JMP\n(%s)\n" % (func_label, k, loop_label, end_label, asm_pushlocal, loop_label, end_label)
        self.f_handler.write(asm)

    def writeReturn(self, command):
        if not isinstance(command, C_RETURN):
            raise TypeError("command must be C_RETURN command instance")

        # get the distinct frame label and ret label
        # can have several returns in a .vm file, so need to add counter too
        frame_label = self.folder_file + ".FRAME" + str(self.LABEL_CTR)
        self.LABEL_CTR += 1
        ret_label = self.folder_file + ".RET" + str(self.LABEL_CTR)
        self.LABEL_CTR += 1

        asm = "@LCL\nD=M\n@%s\nM=D\n" % (frame_label) # FRAME = LCL
        asm += "@%s\nD=M\n@5\nA=D-A\nD=M\n@%s\nM=D\n" % (frame_label, ret_label) # RET = *(FRAME - 5)
        asm += "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n" # *ARG = pop()
        asm += "@ARG\nD=M+1\n@SP\nM=D\n" # SP = ARG + 1
        asm += "@%s\nA=M-1\nD=M\n@THAT\nM=D\n" % (frame_label) # THAT = *(FRAME-1)
        asm += "@%s\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n" % (frame_label) # THIS = *(FRAME-2)
        asm += "@%s\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n" % (frame_label)# ARG = *(FRAME-3)
        asm += "@%s\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n" % (frame_label)# LCL = *(FRAME-4)
        asm += "@%s\nA=M\n0;JMP\n" %(ret_label) # A=M
        self.f_handler.write(asm)

    def writeInit(self):
        """writes the bootstrapping assembly code. Only called when there's Sys.vm file in a folder where more than 1 .vm files are located"""
        n = 0
        func_label = self.folder_name + ".Sys.init"
        self.LABELS_CREATED["Sys.init"] = func_label
        ret_addrs = func_label + ".RETURN_ADDRS" + str(self.LABEL_CTR) # for calling Sys.init
        self.LABEL_CTR += 1

        # setting SP to 256
        asm = "@256\nD=A\n@SP\nM=D\n" # get rid of @Fibonacci.Sys.init, because it will omit pushing the 5 things (which will set the SP at 261)
        # call Sys.init 0
        asm += "@%s\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % (ret_addrs) #push return address
        asm += "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push LCL
        asm += "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push ARG
        asm += "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push THIS
        asm += "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push THAT
        asm += "@SP\nD=M\n@%s\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n" % (n) # ARG = SP-n-5
        asm += "@SP\nD=M\n@LCL\nM=D\n" # LCL = SP
        asm += "@%s\n0;JMP\n" % (func_label) # goto Sys.init
        asm += "(%s)\n" % (ret_addrs) # declare return address here
        self.f_handler.write(asm)

    def writeCall(self, command):
        """Writes the assembly code that is the translation of the given Call command"""
        if not isinstance(command, C_CALL):
            raise TypeError("command must be C_CALL command instance")
        arg1, arg2 = command.arg1, command.arg2 # arg1 = Main.fibonacci, 

        # get the foldername.shortfilename.label, which will be used to determine the distinct label that's been padded with foldername.shortfilename
        if self.folder_name:
            folder_file_funcname = self.folder_name + "." + arg1 # FibonacciElement.Main.fibonacci
        else:
            folder_file_funcname = arg1 # if we're dealing with one file, say Main.vm (then self.folder_name = ""), and it's calling Main.fibonacci in itself

        # get func_label, the distinct label for the function being declared, either from lookup existing, or creating a new one
        if folder_file_funcname in self.LABELS_CREATED:
            func_label = self.LABELS_CREATED[folder_file_funcname]
        else:
            func_label = folder_file_funcname
            self.LABELS_CREATED[folder_file_funcname] = func_label    # FibonnaciElement.Main.fibonacci: FibonacciElement.Main.fibonacci

        n = int(arg2) # number of arguments passed into function arg1
        # define return address label
        ret_addrs = func_label + ".RETURN_ADDRS" + str(self.LABEL_CTR) #Fibonacci.Main.fibonacci.RETURN_ADDRS5
        self.LABEL_CTR += 1
        asm = "@%s\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % (ret_addrs) #push return address
        asm += "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push LCL
        asm += "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push ARG
        asm += "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push THIS
        asm += "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # push THAT
        asm += "@SP\nD=M\n@%s\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n" % (n) # ARG = SP-n-5
        asm += "@SP\nD=M\n@LCL\nM=D\n" # LCL = SP
        asm += "@%s\n0;JMP\n" % (func_label) # goto f
        asm += "(%s)\n" % (ret_addrs) # declare return address here 
        self.f_handler.write(asm)

    def Close(self):
        """write and close the output file"""
        # add unconditional jump
        self.f_handler.write("(EOF)\n@EOF\n0;JMP\n")
        self.f_handler.close()



if __name__ == "__main__":
    pass
    