"""main driver of the VM translator"""

from Parser import Parser, C_ARITHMETIC, C_POP, C_PUSH 
from CodeWriter import CodeWriter
import os
import sys


def Main():
    """
    Main driver of the VM translator.Takes in command line input for the .vm file path to be translated.
    Output a .asm file under the same directory as the input .vm file
    """
    # make sure valid input for .vm file path is received
    if len(sys.argv) < 2:
        sys.exit("Usage:\npython Main.py VMCodeToBeConverted.vm")
    
    fpath = sys.argv[1].strip()

    # for now we only support single .vm files
    if not os.path.isfile(fpath) or not fpath.endswith(".vm"):
        sys.exit("Please provide a valid path for an .vm file, directories are not support yet.")

    # instatiate a codewrite instance
    cw = CodeWriter(fpath)
    
    for i in range(0, len(cw.file_lst)): # for now, there's only one file in cw.file_lst
        # get the filename, and make it the current file name of the codewriter
        fname = cw.file_lst[i] 
        cw.setFileName(fname) # cw.crt_fname = fname
        
        # remove whitespace and comments from the .vm file and instatiate a Parser object with it
        with open(fname) as f:
            comm_lst = Parser().removeWhiteSpace(f.read())
        psr = Parser("\n".join(comm_lst))
        # go through each command line in the file being parsed
        while psr.hasMoreCommands():
            psr.advance()
            comm = psr.get_command() # determine what type of vm command 

            if isinstance(comm, C_ARITHMETIC):
                cw.writeArithmetic(comm)
            elif isinstance(comm, (C_POP,C_PUSH)):
                cw.writePushPop(comm)
            else:
                raise ValueError(psr.crt_code, ": we currently support only C_ARITHMETIC, C_POP, C_PUSH commands")
        
    cw.Close() # finish writing and close the file handler
    print("Written to", cw.fname_out)
           



if __name__ == "__main__":
    Main()