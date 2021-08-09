"""The main driver of the assembler"""

import sys
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable

def main():
    """
    the driver program for the assembler
    takes in an .asm file from user console input, convert it into binary code and output into a corresponding .hack file
    """
    if len(sys.argv) < 2:
        sys.exit("Usage:\npython Main.py AssemblyCodeToBeConverted.asm")

    fname = sys.argv[1]
    
    with open(fname) as f:
        # first remove white spaces in the file stream and convert into list of commands of str type
        command_lst = Parser().removeWhiteSpace(f.read())
        
    # then go through the command list to update the symbol hash table and remove L_COMMANDS like (Xxx)
    # SYMBOL_HASH should include all (variable, variable_ram_address), (LABEL, LABEL_rom_address) pairs besides the predefined pairs
    # command_lst should have no (Xxx) commands
    SYMBOL_HASH, command_lst = SymbolTable().update_symbol_table(command_lst)
    
    psr = Parser("\n".join(command_lst)) # join the command elements into a string seperated by "\n"

    str_out = "" # for holding the binary code strings
    while psr.hasMoreCommands():
        psr.advance() # read in one string command form psr.comm_list and put into psr.crt_code
        
        # convert the str-typed crt_code into an instance of A_COMMAND, L_COMMAND, or C_COMMAND
        asm = psr.get_command(SYMBOL_HASH)

        # convert the A_/L_/C_COMMAND into binary code, and concat into str_out, separated by "\n"
        binary = Code(asm).get_binary_code()
        str_out += binary + "\n"

    # write out to .hack file
    fname_out = fname.replace(".asm",".hack")
    with open(fname_out, "w") as f:
        f.write(str_out)
    print("written to " + fname_out)


if __name__ == "__main__":
    main()