assembly_program = [  # Sample assembly program
    "ORG 100",  # Set the starting memory location to 100 (hexadecimal)
    "LDA SUB",  # Load the value of SUB into the accumulator
    "CMA",      # Complement the contents of the accumulator
    "INC",      # Increment the accumulator
    "ADD MIN ", # Add the value of MIN to the accumulator
    "STA DIF",  # Store the result in DIF
    "HLT",      # Halt the program
    "MIN, DEC 83",  # Define a label MIN with the decimal value 83
    "SUB, DEC -23", # Define a label SUB with the decimal value -23
    "DIF, HEX 0",   # Define a label DIF with the hexadecimal value 0
    "END"           # End of the program
]

symbol_table = {}  # Dictionary to store labels and their corresponding memory addresses
binary_output = []  # List to store the binary representation of instructions

# Opcodes for memory reference instructions with direct addressing
memoryDirectOpcodes = {
    "AND": "0000", 
    "BUN": "0100",
    "BSA": "0101",
    "ISZ": "0110",
    "LDA": "0010", 
    "ADD": "0001", 
    "STA": "0011", 
}
# Opcodes for memory reference instructions with indirect addressing
memoryInDirectOpcodes = {
    "AND": "1000", 
    "BUN": "1100",
    "BSA": "1101",
    "ISZ": "1110",
    "LDA": "1010", 
    "ADD": "1001", 
    "STA": "1011", 
}
# Opcodes for non-memory reference instructions
instructions = {
    "CLA": "7800",
    "CLE": "7400",
    "CMA": "7200",
    "CME": "7100",
    "CIR": "7080",
    "CIL": "7040",
    "INC": "7020",
    "SPA": "7010",
    "SNA": "7008",
    "SZA": "7004",
    "SZE": "7002",
    "HLT": "7001",
    "INP": "F800",
    "OUT": "F400",
    "SKI": "F200",
    "SKO": "F100",
    "ION": "F080",
    "IOF": "F040"
}

def first_pass(program):
    # This function processes the program to create a symbol table.
    lc = 0  # Initialize the location counter
    for line in program:
        tokens = line.split()  # Split each line into tokens
        if tokens[0] == "END":  # Stop processing if END is encountered
            break
        if tokens[0] == "ORG":  # Set the location counter to the specified value
            lc = int(tokens[1])
            continue
        if "," in tokens[0]:  # If a label is found
            label = tokens[0].replace(",", "")  # Remove the comma from the label
            symbol_table[label] = lc  # Add the label and its address to the symbol table
        lc += 1  # Increment the location counter

def second_pass(program):
    # This function generates the machine code for the program.
    lc = 0  # Initialize the location counter
    for line in program:
        tokens = line.split()  # Split each line into tokens
        if tokens[0] == "END":  # Stop processing if END is encountered
            break
        if tokens[0] == "ORG":  # Set the location counter to the specified value
            lc = int(tokens[1])
            continue

        if tokens[0] in memoryDirectOpcodes:  # Handle memory reference instructions
            operand = symbol_table.get(tokens[1], 0)  # Get the address of the operand
            binary_operand = bin(int(str(operand), 16))[2:].zfill(12)  # Convert address to binary
            if len(tokens) > 1 and tokens[len(tokens) - 1] != 'I':  # Check for direct addressing
                opcode = memoryDirectOpcodes[tokens[0]]
                binary_output.append(f"{lc:03} {opcode}{binary_operand}")  # Generate binary code
            else:  # Indirect addressing
                opcode = memoryInDirectOpcodes[tokens[0]]
                binary_output.append(f"{lc:03} {opcode}{binary_operand}")
        elif tokens[0] in instructions:  # Handle non-memory reference instructions
            opcode = instructions[tokens[0]]
            binary_opcode = bin(int(str(opcode), 16))[2:].zfill(16)  # Convert opcode to binary
            binary_output.append(f"{lc:03} {binary_opcode}")

        elif tokens[1] == "DEC":  # Handle decimal data definitions
            value = int(tokens[2])  # Parse the decimal value
            if value < 0:  # Handle negative values using 2's complement
                value = (1 << 16) + value 
            binary_output.append(f"{lc:03} {value:016b}")  # Convert to 16-bit binary

        elif tokens[1] == "HEX":  # Handle hexadecimal data definitions
            value = int(tokens[2], 16)  # Parse the hexadecimal value
            binary_output.append(f"{lc:03} {value:016b}")  # Convert to 16-bit binary
        lc += 1  # Increment the location counter

# Execute the first pass to create the symbol table
first_pass(assembly_program)
# Execute the second pass to generate the binary output
second_pass(assembly_program)

# Print the symbol table
print("Symbol Table:")
for symbol, address in symbol_table.items():
    print(f"{symbol}: {address}")

# Print the generated machine code
print("\nMachine Code:")
for code in binary_output:
    print(code)
