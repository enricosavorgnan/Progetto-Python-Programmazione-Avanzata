# Savorgnan Enrico
# SM 320 1371
# 2025.01.08

from queue import Queue

import exceptions as ex


class LMC:
    # The LMC class is responsible for executing the program, given the memory from the assembler.
    # There exist two modes of execution: all at once and step by step.
    # For more infos, check the README.md file.

    def __init__(self, assemble):
        # ----------------- LMC Constructor -----------------
        # Initialize the LMC with the memory and a flag for inputs from the assembler
        # The accumulator is initialized to 0 as well as the program counter
        # --------------------------------------------------------
        # Input:
        # assemble: Assembler
        #       The Assembler object from which the memory and the flag for inputs
        # --------------------------------------------------------
        # Output: None
        # --------------------------------------------------------


        self.memory = assemble.memory
        self.needs_input = assemble.needs_input

        self.accumulator = 0
        self.program_counter = 0
        self.input_queue = Queue()
        self.output_queue = Queue()

        self.overflow = 0               #This flag is 1 if the accumulator is greater than 999 or less than 0

        self.running = True             #This flag is True until the program reaches a halt instruction

        # Dictionary to map instructions to their respective methods
        self.opcodes = {0: self.__hlt,
                        1: self.__add,
                        2: self.__sub,
                        3: self.__sta,
                        5: self.__lda,
                        6: self.__bra,
                        7: self.__brz,
                        8: self.__brp,
                        901: self.__inp,
                        902: self.__out
            }


    def print_queue(self):
        # Method that prints the output queue.
        print("\nOutput queue:")
        while not self.output_queue.empty():
            print( self.output_queue.get() )
        print("\n")
        return


    def __add(self, cell):
        self.accumulator += self.memory[cell]
        self.__update_flag()
        return


    def __sub(self, cell):
        self.accumulator -= self.memory[cell]
        self.__update_flag()
        return


    def __sta(self, cell):
        self.memory[cell] = self.accumulator
        return


    def __lda(self, cell):
        self.accumulator = self.memory[cell]
        return


    def __bra(self, cell):
        self.program_counter = cell
        return


    def __brz(self, cell):
        if self.accumulator == 0 and self.overflow == 0:
            self.program_counter = cell
        return


    def __brp(self, cell):
        if self.overflow == 0:
            self.program_counter = cell
        return


    def __inp(self):
        if self.input_queue.empty():
            self.running = False
            return

        value = self.input_queue.get()
        self.accumulator = value
        return


    def __out(self):
        self.output_queue.put( self.accumulator )
        return


    def __hlt(self, trash):
        # Trash parameter is here only to match the signature of the other methods
        print("\nProgram halted")
        self.running = False
        return


    def __update_flag(self):
        # Method that updates the flag of the LMC if the accumulator is greater than 999 or less than 0,
        # i.e. an overflow occurred.

        if self.accumulator > 999 or self.accumulator < 0:
            self.overflow = 1
            self.accumulator %= 1000
        else:
            self.overflow = 0
        return


    def user_input(self):
        # Method that populates the input queue with the user's input.
        # The cycle ends when the user inserts '-1'.

        print("\nYou are asked to insert some values in the input queue.\nTap -1 once you have finished.\n")

        # While the user does not insert -1, the cycle continues
        while True:

            # Ask for the user's input
            user_input = input("\tInsert an integer between 0 and 999: ")

            try:
                user_input = int(float(user_input))
            except:
                print("Invalid input. Next time, insert a 'int' number in [0-999].\n")
                raise ex.UserException()

            if user_input == -1:
                break

            if user_input < 0 or user_input > 999:
                print("Invalid input. Next time, insert a number in [0-999].\n")
                raise ex.UserException()

            self.input_queue.put(user_input)

        return


    def execute(self, instruction):
        # Method that executes the instruction given as input.
        # The instruction is divided into the opcode and the value.

        if instruction in [901, 902]:
            self.opcodes[instruction]()
            return

        # Extract the opcode and the value from the instruction
        opcode = instruction // 100
        value = instruction % 100

        try:
            self.opcodes[opcode](value)
        except:
            print(f'An error occurred because opcode: {opcode} is not in the list of opcodes\n')
            raise ex.OpcodeException
        return


    def run(self):
        # ----------------- Run Method -----------------
        # Method that runs the LMC program in all at once mode.
        # --------------------------------------------------------
        # Input: None
        # --------------------------------------------------------
        # Output: None
        # --------------------------------------------------------


        # Ask for the user's input to populate self.input_queue, only if the inherited self.needs_input flag is True
        if self.needs_input is True:
            try:
                self.user_input()
            except ex.UserException:
                raise ex.UserException


        # Cycle ends when the program reaches a halt instruction or asks for values in the input queue but this is empty
        while self.running is True:

            # Check for the program counter to be in the range [0, 99]:
            if self.program_counter < 0 or self.program_counter > 99:
                print("Program counter is out of bounds")
                raise ex.InternalException

            # Fetch the instruction from the memory
            instruction = self.memory[self.program_counter]

            # Increment the program counter
            self.program_counter = ( self.program_counter + 1 ) % 100

            # Call to the executor of the instruction
            try:
                self.execute(instruction)
            except ex.OpcodeException:
                raise ex.OpcodeException

        return


    def run_steps(self):
        # ----------------- Run Step By Step ---------------------
        # Method that runs the LMC program in the StepByStep mode.
        # At each iteration, the user needs to press a key to execute the next instruction.
        # This method is basically the same as the sef.run method, concerning the logic of the method.
        # The difference is that this method is a generator, and the main program needs
        # to call next(generator) to execute the next instruction.
        # --------------------------------------------------------


        # Ask for the user's input to populate self.input_queue, only if the inherited self.needs_input flag is True
        if self.needs_input is True:
            try:
                self.user_input()
            except ex.UserException:
                raise ex.UserException

        # Cycle ends when the program reaches a halt instruction or asks for values in the input queue but this is empty
        while self.running is True:

            # Check for the program counter:
            if self.program_counter < 0 or self.program_counter > 99:
                print("Program counter is out of bounds")
                raise ex.InternalException

            # Fetch the instruction from the memory
            instruction = self.memory[self.program_counter]

            # Increment the program counter
            self.program_counter = ( self.program_counter + 1 ) % 100

            # Yield the instruction to the caller.
            # The print of the status and the call to self.execute are after the yield so that
            # when the execution ends we have no longer calls to next(generator).
            yield

            # Print the status of the program
            print(f"\nProgram Counter: {self.program_counter}\n"
                  f"Accumulator: {self.accumulator}\n"
                  f"Instruction: {instruction}\n"
                  f"Memory: {self.memory}\n")

            # Executing the instruction
            try:
                self.execute(instruction)
            except ex.OpcodeException:
                raise ex.OpcodeException