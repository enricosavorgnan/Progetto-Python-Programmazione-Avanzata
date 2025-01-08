# Savorgnan Enrico
# SM 320 1371
# 2025.01.08

import exceptions as ex


class Assembler:
    # The Assembler class is responsible for reading the file, preprocessing it, checking for labels, and assembling the file into memory.
    # For more infos, check the README.md file.

    def __init__(self, file_name: list[str]):
        # ----------------- Assembler Constructor -----------------
        # This method initializes the Assembler, given the file name
        # The memory is initialized as an empty list, the labels as an empty dictionary,
        # and the opcodes as a dictionary with the instructions and their respective values.
        # The flag needs_input, that indicates whether the .lmc needs some input from user, is set to False.
        # --------------------------------------------------------
        # Input:
        # file_name: list[str]
        #       The name of the file to read and to assemble
        # --------------------------------------------------------
        # Output: None
        # --------------------------------------------------------


        self.file = file_name
        self.memory= []         # A list of 100 integers, representing the memory of the LMC
        self.labels = {}        # A dictionary with the labels and their respective memory address
        self.opcodes = {"add": 100,
                                  "sub": 200,
                                  "sta": 300,
                                  "lda": 500,
                                  "bra": 600,
                                  "brz": 700,
                                  "brp": 800,
                                  "inp": 901,
                                  "out": 902,
                                  "hlt": 0,
                                  "dat": None
                    }
        self.needs_input = False    # A flag to indicate if the program needs input from the user



    def check_for_labels(self):
        # ----------------- Check for Labels ---------------------
        # This method checks for labels in the file and adds them to the dictionary self.labels.
        # The structure of a correctly-implemented line with a label is:    label  instruction  value
        # So we need to check if the first token is not an instruction while the second token is.
        # We add the value to self.labels only if the label is not declared in self.labels yet.
        # --------------------------------------------------------
        # Input: None
        # --------------------------------------------------------
        # Output: None
        # --------------------------------------------------------


        for i, line in enumerate(self.file):
            # Splitting lines at spaces ' '
            tokens = line.split()

            # First token is not and instruction AND second token is an instruction AND first token is not in the list of labels.
            if tokens[0] not in self.opcodes and tokens[1] in self.opcodes and tokens[0] not in self.labels:
                self.labels[tokens[0]] = i

        return


    def preprocess_file(self):
        # ----------------- Preprocess File ----------------------
        # This method preprocesses the file, removing comments and lowercasing the file
        # If the resulting file is empty, an exception is raised.
        # --------------------------------------------------------
        # Input: None
        # --------------------------------------------------------
        # Output: None
        # --------------------------------------------------------


        cleaned_file = []
        for i, line in enumerate(self.file):
            # Remove comments from the file
            line = line.split("//")[0].strip()

            # If line is not empty:
            if len(line) > 0:
                # Lowercasing the line of the file and appending it to the cleaned file
                cleaned_file.append( line.lower() )

        # Update self.file
        self.file = cleaned_file

        # If file is empty, raise an error
        if len(self.file) == 0:
            print(f'\n\nThe file is empty after preprocessing\n\n')
            raise ex.AssembleException()

        return


    def assemble(self):
        # ----------------- Assemble ----------------------------
        # This method creates the Assembly for the .lmc file.
        # It reads the file, preprocesses it, checks for labels, and assembles the file into memory.
        # For more infos about the stream of this method, check the README.md file.
        # --------------------------------------------------------
        # Input: None
        # --------------------------------------------------------
        # Output: None
        # --------------------------------------------------------

        # Call the preprocess_file method to remove comments and lowercasing the file
        try:
            self.preprocess_file()
        except ex.AssembleException:
            return


        # Call the check_for_labels method to check for labels in the file
        self.check_for_labels()


        # Iterate over the file
        for i, line in enumerate(self.file):
            # Splitting lines at spaces ' '
            tokens = line.split()


            # If the first token is a label, it is removed
            if tokens[0] in self.labels:
                tokens = tokens[1:]


            # If the first token is a valid instruction ...
            if tokens[0] in self.opcodes:

                # ... and the instruction is "dat", the value is added to the memory
                if tokens[0] == "dat":
                    try:
                        value = int( tokens[1] ) if len(tokens) > 1 else 0
                        self.memory.append(value)
                    except ValueError:              # tokens[1] is not a number
                        print(f"\n\nAn error occurred at line {i} of the file with the instruction: {line}\n"
                              f"DAT token not a number\n\n")
                        print("Returning...\n")
                        raise ex.AssembleException

                # ... and the instruction is "inp", "out" or "hlt", the instruction opcode is added to the memory
                elif tokens[0] in ["inp", "out", "hlt"]:
                    self.memory.append(self.opcodes[tokens[0]])
                    if tokens[0] == "inp":
                        self.needs_input = True

                # ... and the instruction is not one of the previous, the instruction is added to the memory with the respective value or label indicating the memory address.
                # If the instruction is not valid, an error is raised
                else:
                    # If second token is a label
                    if tokens[1] in self.labels:
                        # Opcode + label value
                        self.memory.append( int( self.opcodes[tokens[0]] + self.labels[tokens[1]] ) )
                    else:
                        try:
                            # If second token is not a label, it must be a number, casted to int
                            value = int( tokens[1] )
                            self.memory.append( int( self.opcodes[tokens[0]] + value ) )
                        except ValueError:              # tokens[1] is not a number, nor a label
                            print(f"\n\nAn error occurred at line {i} of the file with the instruction: {line}\n"
                                  f"Token not int or valid label\n\n")
                            print("Returning...\n")
                            raise ex.AssembleException()


            # while if the first token is not a label and not a valid instruction, an error is raised
            else:
                print(f"\n\nAn error occurred at line {i} with the instruction: {line}\n"
                      f"Instruction not recognized\n\n")
                print("Returning...\n")
                raise ex.AssembleException()


        # If the memory is more than 100 cells long, an error is raised
        if len(self.memory) > 100:
            print(f"\n\nThe file overflows the memory of the LMC\n\n")
            print("Returning...\n")
            raise ex.AssembleException


        # Fill the all the other cells in memory with 0s. Memory is 100 cells long
        for i in range(100-len(self.memory)):
            self.memory.append(0)

        return
