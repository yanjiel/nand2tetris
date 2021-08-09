"""Translate VM commands into Hack assembly code"""

import os
from Parser import C_ARITHMETIC, C_PUSH, C_POP

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
    LABEL_CTR = 0
    LOOKUP_TABLE = {
        "local": "LCL",
        "argument": "ARG",
        "this":"THIS",
        "that":"THAT",
    }

    def __init__(self, fpath=None):
        """opens the output file/stream and gets ready to write into it"""
        
        self.file_lst = [] # to hold the list of .vm files to process in case the input is a program (collection of .vm files)
        self.fname_out = ""
        self.f_handler = None # file handler to write to self.fname_out
        
        # get the file name for the output .hack (self.fname_out), and the list of .vm files to be processed (self.file_lst)
        if os.path.isdir(fpath):
            # if we're dealing with a program, a collection of vm files
            pass
            # for fname in os.scandir(fpath):
            #     if fname.path.endswith(".vm"): # fname.path is the path for the sub-directory files
            #         self.file_lst.append(fname.path)

        elif os.path.isfile(fpath):
            # if we're dealing with a signle .vm file
            if not fpath.endswith(".vm"):
                raise TypeError("please input only .vm file paths or folders containing .vm files")
            
            self.fname_out = fpath.replace(".vm", ".asm") #r"...\StackTest\StackTest.hack"
            self.file_lst.append(fpath)
        else:
            raise TypeError("fpath either needs to be a folder path or a file path in str type")

        self.f_handler = open(self.fname_out, "w")

    def setFileName(self, fileName):
        """informs the code write that the translation of a new .VM file is started"""
        if fileName not in self.file_lst:
            raise ValueError("cannot set fileName to files other than", self.file_lst)
        self.crt_fname = fileName
        
    def writeArithmetic(self, command):
        """writes the assembly code that is the translation of the given arithmetic command"""
        #command will be a C_ARITHMETIC instance#
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
        #command will be a C_POP or C_PUSH instance#
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
            sym_name = path_seg[-1].replace("vm", str(arg2))
            
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
        


    def Close(self):
        """write and close the output file"""
        # add unconditional jump
        self.f_handler.write("(EOF)\n@EOF\n0;JMP\n")
        self.f_handler.close()
