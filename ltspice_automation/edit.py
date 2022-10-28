def edit(read_file, save_file):
    """
    Here is some sample code if you already have an existing netlist and just want to edit some lines
    :param read_file: Saved (.txt) Netlist file
    :param save_file: Name for the changed Netlist
    :return: None
    """
    with open(read_file, 'rb') as f:
        lines = f.readlines()
    print(type(lines))
    print(lines[19])
    lines[3] = lines[3].replace(lines[3][:], 'R2 N006 N008 2k\n'.encode('ascii'))
    print(len(lines[3]))
    print(lines[3])
    lines[19] = lines[19].replace(lines[19][:], '.lib 2N6027.LIB\n'.encode('ascii'))
    print(lines[19])
    new_schematic = ''.encode('ascii').join([item for item in lines])
    with open(save_file, 'wb') as file:
        file.write(new_schematic)


