"""main driver of the VM translator"""

from Parser import C_CALL, C_FUNCTION, C_GOTO, C_IF, C_LABEL, C_RETURN, Parser, C_ARITHMETIC, C_POP, C_PUSH 
from CodeWriter import CodeWriter
import os
import sys


def Main():
    """
    Main driver of the VM translator.Takes in command line input for the .vm file path to be translated.
    Output a .asm file under the same directory as the input .vm file
    """
    # # make sure valid input is received
    # if len(sys.argv) < 2:
    #     sys.exit("Usage:\npython Main.py VMCodeToBeConverted.vm")
    # fpath = sys.argv[1].strip()
    # if not os.path.exists(fpath):
    #     sys.exit("Please provide a valid path.")

    #fpath = r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\08\ProgramFlow\BasicLoop\BasicLoop.vm"
    #fpath = r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\08\ProgramFlow\FibonacciSeries\FibonacciSeries.vm"
    #fpath = r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\08\FunctionCalls\SimpleFunction\SimpleFunction.vm"
    #fpath = r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\08\FunctionCalls\FibonacciElement"
    
    fpath = r"C:\Users\Adele Liu\Desktop\nand2tetris\projects\08\FunctionCalls\StaticsTest"

    # instatiate a codewrite instance
    cw = CodeWriter(fpath)
    
    if cw.folder_name and len(cw.file_lst) > 1: # if fpath is a directory, and there's more than one file in the directory
        cw.writeInit()

    for i in range(0, len(cw.file_lst)): # go through each file in CodeWrite.file_lst
        # get the filename, and make it the current file name of the codewriter
        fname = cw.file_lst[i] 
        cw.setFileName(fname) # cw.crt_fname, cw.crt_fname_short, cw.folder_file
        
        # remove whitespace and comments from the .vm file and instatiate a Parser object with it
        with open(fname) as f:
            comm_lst = Parser().removeWhiteSpace(f.read()) # each line of VM command is an element in comm_lst and in lower cases
        psr = Parser("\n".join(comm_lst))
        # go through each command line in the file being parsed
        while psr.hasMoreCommands():
            psr.advance()
            print(psr.crt_code)
            comm = psr.get_command() # determine what type of vm command 

            if isinstance(comm, C_ARITHMETIC):
                cw.writeArithmetic(comm)
            elif isinstance(comm, (C_POP,C_PUSH)):
                cw.writePushPop(comm)
            elif isinstance(comm, C_LABEL):
                cw.writeLabel(comm)
            elif isinstance(comm, C_GOTO):
                cw.writeGoto(comm)
            elif isinstance(comm, C_IF):
                cw.writeIf(comm)
            elif isinstance(comm, C_FUNCTION):
                cw.writeFunction(comm)
            elif isinstance(comm, C_RETURN):
                cw.writeReturn(comm)
            elif isinstance(comm, C_CALL):
                cw.writeCall(comm)
            else:
                raise ValueError(psr.crt_code, ": we currently support only C_ARITHMETIC, C_POP, C_PUSH, C_IF, C_GOTO, C_LABEL, C_FUNCTION, C_RETURN and C_CALL commands")
        
    cw.Close() # finish writing and close the file handler
    print("Written to", cw.fname_out)
           

if __name__ == "__main__":
    Main()