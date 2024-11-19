import argparse
import struct
import xml.etree.ElementTree as ET
import pickle

result_data = []
log_file_data = []

def parse_args():
    parser = argparse.ArgumentParser(description="Assembler and Interpreter for UVM")
    parser.add_argument("mode", choices=["assemble", "interpret"], help="Operation mode: 'assemble' or 'interpret'")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("output_file", help="Output file")
    parser.add_argument("log_file", help="Log file (XML format)")
    parser.add_argument("--result_file", help="Result file for interpreter (XML format)")
    parser.add_argument("--memory_range", help="Memory range for interpreter (start:end)", type=str)
    return parser.parse_args()

def read_input_file(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error! File {input_file} not found")
        exit(1)

def parse_instruction(instruction):
    parts = instruction.split(',')
    values = {}
    for part in parts:
        key, value = part.split('=')
        values[key.strip()] = int(value.strip())
    return values

def assemble_instruction(value):
    global result_data, log_file_data
    A = value['A']
    B = value['B']
    C = value['C']
    try:
        D = value['D']
    except KeyError:
        D = None

    command = (A & 0x3F)
    command |= (B & 0x7) << 6
    command |= (C & 0x1FFF) << 9
    if D is not None:
        command |= (D & 0x7) << 22

    byte1 = command & 0xFF
    byte2 = (command >> 8) & 0xFF
    byte3 = (command >> 16) & 0xFF

    result_data.extend([byte1, byte2, byte3])
    log_file_data.append({
        "A": A, "B": B, "C": C, "D": D,
        "result_1": hex(byte1),
        "result_2": hex(byte2),
        "result_3": hex(byte3)
    })
    print(hex(byte1), hex(byte2), hex(byte3))

def write_log_file(log_file):
    root = ET.Element("log")
    for entry in log_file_data:
        instruction = ET.SubElement(root, "instruction")
        for key, value in entry.items():
            ET.SubElement(instruction, key).text = str(value)
    tree = ET.ElementTree(root)
    tree.write(log_file, encoding="utf-8", xml_declaration=True)
    print(f"Log written to {log_file}")

def write_binary_file(output_file):
    with open(output_file, "wb") as file:
        file.write(bytearray(result_data))
    print(f"Binary written to {output_file}")

def read_binary_file(input_file):
    try:
        with open(input_file, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error! File {input_file} not found")
        exit(1)

def interpret_commands(binary_data, memory_range):
    memory = [0] * 256
    for i in range(0, len(binary_data), 3):
        if i + 3 > len(binary_data):
            break
        command = struct.unpack("<I", binary_data[i:i+3] + b"\x00")[0]
        opcode = command & 0x3F
        arg1 = (command >> 6) & 0x7
        arg2 = (command >> 9) & 0x1FFF
        arg3 = (command >> 22) & 0x7
        if opcode == 30:
            memory[arg1] = arg2 + arg3
        elif opcode == 1:
            memory[arg1] = arg2 - arg3
    start, end = map(int, memory_range.split(":"))
    return memory[start:end]

def write_result_file(result_file, memory_slice):
    root = ET.Element("result")
    for address, value in enumerate(memory_slice):
        mem = ET.SubElement(root, "memory")
        ET.SubElement(mem, "address").text = str(address)
        ET.SubElement(mem, "value").text = str(value)
    tree = ET.ElementTree(root)
    tree.write(result_file, encoding="utf-8", xml_declaration=True)
    print(f"Result written to {result_file}")

def main():
    args = parse_args()
    if args.mode == "assemble":
        instructions = read_input_file(args.input_file)
        for line in instructions:
            if not line.strip():
                continue
            values = parse_instruction(line.strip())
            assemble_instruction(values)
        write_binary_file(args.output_file)
        write_log_file(args.log_file)
    elif args.mode == "interpret":
        if not args.result_file or not args.memory_range:
            print("Error! Result file and memory range are required for interpretation.")
            exit(1)
        binary_data = read_binary_file(args.input_file)
        memory_slice = interpret_commands(binary_data, args.memory_range)
        write_result_file(args.result_file, memory_slice)

if __name__ == "__main__":
    main()