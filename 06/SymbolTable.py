"""Keeps a correspondence between symbolic labels and numeric addresses"""

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

class SymbolTable(object):
    """
    represent a symbol table for allocating the labels and variables in any assembly code

    Private Attribute
    __table: a hash table for holding the symbol (label and variable) and its corresponding address in ROM/RAM

    Method
    add_entry(sym, addrs): adds the pair (`sym`, `addrs`), representing a symbol and its address, to self.__table
    contains(sym): return in Boolean whether self.__table contains the given symbol `sym`
    get_address(sym): returns the integer address associated with the symbol `sym`
    replace_symbol(command_lst): takes in a list of str assembly commands, looks up the symbols of A_COMMANDS,
                                 replace them with their corresponding integer addresses, and return an updated list of str commands
    """
    def __init__(self, table=None):
        if not table:
            self.__table = DEFAULT_TABLE
        else:
            self.__table = table
    
    def add_entry(self, sym, addrs):
        """adds the pair (symbol, address) to self.__table"""
        if not isinstance(sym, str) or not isinstance(addrs, int):
            raise TypeError("argument sym must str type and addrs must be int type")

        if not self.contains(sym):
            self.__table[sym] = addrs
        
    def contains(self, sym):
        """return in Boolean whether self.__table contains the given symbol"""
        if sym in self.__table:
            return True
        else:
            return False
    
    def get_address(self, sym):
        """returns the integer address associated with the symbol"""
        if sym in self.__table:
            return self.__table[sym]
        else:
            return None

    def update_symbol_table(self, command_lst):
        """
        looks up the symbols of A_COMMANDS in command_lst, replace them with their corresponding integer addresses,
        and return an updated list of str commands that have not symbols
        """
        if not isinstance(command_lst, list):
            raise TypeError("command_lst needs to be list type")

        
        new_command_lst = [] # this holds the intrim list of commands
        # first we go through command list to find (LABEL) declarations, allocate ROM address for each (LABEL), add each pair to symbol hash, then remove the LABEL declarations
        for i in range(0, len(command_lst)):
            comm = command_lst[i]
            new_command_lst.append(comm) # default to add each str command to the list of commands as output

            # if the command is a (LABEL) declaration, then skip this command
            if comm.startswith("(") and comm.endswith(")"): 
                label = comm.replace("(","")
                label = label.replace(")","")
                if label and not self.contains(label):
                    new_command_lst.pop() # then we skip this command (XXXX) by popping it out after being added by default
                    self.add_entry(label, len(new_command_lst)) # the address of the label points to the end of the output list of commands
        
        # now we go through new comamnd list to find @Xxx where Xxx are symbols (not int numbers), allocate & replace variables their RAM addresses starting at 16, 
        # add each pair to the symbol hash, and replace LABELs with their ROM addresses
        start = 16
        final_command_lst = [] # this holds the final list of commands that will be output
        for i in range(0, len(new_command_lst)):
            comm = new_command_lst[i]
            final_comm = comm # default is to add each command as it is

            if comm.startswith("@"): # if the command is an address-instruction
                num_sym = comm.replace("@","")

                # if the address-instruction references a variable instead of a decimal number
                # then allocate an address in RAM starting at 16, and add to the symbol hash
                if num_sym and not num_sym.isdigit() and not self.contains(num_sym):
                    self.add_entry(num_sym, start) # add the symbol and address to the table
                    start += 1
            
            final_command_lst.append(final_comm)
        
        return self.__table, final_command_lst

def test():
    """for debugging purposes, please ignore"""
    comm_lst = ["(LOOP)", "@i","D=M","D=D+1","M=D", "(END)", "@sum", "@END"]
    
    sym_table, final_comm_lst = SymbolTable(DEFAULT_TABLE).update_symbol_table(comm_lst)
    print(sym_table)
    print(final_comm_lst)

    print(SymbolTable(sym_table).get_address("i"))
    print(SymbolTable(sym_table).get_address("sum"))
    print(SymbolTable(sym_table).get_address("LOOP"))
    print(SymbolTable(sym_table).get_address("END"),"_____________________________")

if __name__ == "__main__":
    pass