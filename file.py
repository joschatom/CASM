def write_to_file(name, data: list):
    f = open(name, 'w+b')
    byte_arr = data
    binary_format = bytearray(byte_arr)
    f.write(binary_format)
    f.close()


def open_code_file(name):
    _ = open(name, 'r+')
    if _.writable(): print("Opened writeable file¨!")

    return _
