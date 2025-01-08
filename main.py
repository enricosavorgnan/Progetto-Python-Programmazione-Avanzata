# Enrico Savorgnan
# SM 320 1371
# 2025.01.08

from assembler import Assembler
from lmc import LMC
import exceptions as ex

def main():
    # ----------------- Main -----------------
    # This is the core function of the program.
    # It asks for the file name, initializes the Assembler and the LMC, and runs the LMC.
    # The user is asked to insert the path to the .lmc file,
    # and later to choose between running the LMC all at once (1) or step by step (0).
    # The output queue is printed at the end.
    # ----------------------------------------
    # Input: None
    # Output: None
    # ----------------------------------------


    # Ask for the file name
    new_file = input("Insert the name of the file: ")
    try:
        with open(new_file, "r") as file:
            file = file.readlines()
    except FileNotFoundError:
        print(f'\n\nAn error occurred while opening the file. Probably the file is not found.\n\n')
        return
    except Exception as e:
        print(f'\n\nAn error occurred while opening the file. {e}\n\n')
        return


    # Initialize the assembler from the data in file
    assemble = Assembler(file)
    try:
        assemble.assemble()
    except ex.AssembleException:
        return
    # print(assemble.memory)


    # Initialize the LMC, given the previous assembler
    lmc = LMC(assemble)

    # Ask the user if they want to run the LMC all at once (1) or step-by-step (0).
    try:
        stream = int(input("Do you want to run all the LMC or Step By Step? (1 for All, 0 for Step By Step): "))
        if stream != 1 and stream != 0:
            print("Invalid Stream choice. Exiting...")
            return
    except ValueError:
        print("Invalid Stream choice. Exiting...")
        return


    # Run the LMC

    # All at once choice
    if stream == 1:
        try:
            lmc.run()
        except ex.UserException or ex.OpcodeException or ex.InternalException:      # Exceptions raised inside the LMC class
            return

    # Step-by-step choice
    if stream == 0:
        generator = lmc.run_steps()
        next(generator)
        while True:
            try:
                # Wait for the user to press a key
                input("\nPress a Key for the next instruction: ")
                next(generator)
            except StopIteration:
                # If the generator is exhausted, break the loop
                break
            except ex.UserException or ex.OpcodeException or ex.InternalException:  # Exceptions raised inside the LMC class
                  return


    # Print the output queue of LMC
    lmc.print_queue()

    return



if __name__ == "__main__":
    main()











