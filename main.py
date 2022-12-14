from file import write_to_file as save
from file import open_code_file as load_code
import sys

output_file = "a.bin"
Data = []
inline_prints = []
org = 0x8000


def add_data(x):
    print(x)
    if x[1] == 2:
        Data.append(x[0][0])
        Data.append(x[0][1])
    else:
        Data.append(x[0])


def parse_block(text: str) -> (any, int):
    text = text.split(',')[0]
    print(text[0])
    if text[0] == '$':
        hex_text = ''
        for _ in text:
            if _ != '$':
                hex_text += _

        hex = int(hex_text, base=16)

        return hex, 1
    if text.startswith('*'):

        address_low = ""
        address_high = ""

        string = ""

        for _ in text:
            if _ != '*' and _ != '$':
                string += _

        address_high = string[0:2]
        address_low = string[1:3]

        address_high = int(address_high, base=16)
        address_low = int(address_low, base=16)

        return (address_high, address_low), 2
    return 00


def attrib_org(params, line: int):
    global org
    org = parse_block(params[1])[0]


def attrib_cprint(params, line: int):
    words = params[1:(len(params))]
    text = ""

    if words[0] == '$(D)':
        inline_prints.append(Data)
        print(".CPRINT $::(DATA)")
        return

    for word in words:
        if word.startswith(';'):
            return
        word += ' '
        text += word

    inline_prints.append((text, line))

def ins_nop(params, line: int):
    Data.append(0xEA) # nop

def ins_hostcall(params, line: int):
    id = parse_block(params[1])

    Data.append(66)

    add_data(id)


def ins_lda(params, line: int):
    Data.append(0xA9)

    val = parse_block(params[1])

    add_data(val)


def ins_ldx(params, line: int):
    Data.append(0xA2)

    val = parse_block(params[1])

    add_data(val)


def ins_ldy(params, line: int):
    Data.append(0xA0)

    val = parse_block(params[1])

    add_data(val)


def ins_sta(params, line: int):
    Data.append(0x85)

    address = parse_block(params[1])

    add_data(address)


def compiler_meta(params, line: int):
    global inline_prints
    global Data
    if params[1] == "STOP":
        print("INLINE STOP!")
        exit(-1)
    elif params[1] == "INLINE_CLEAR":
        inline_prints = []
    elif params[1] == "DATA_CLEAR":
        Data = []
    elif params[1] == "~":
        if len(params) == 3:
            add_data(parse_block(params[2].split(":")[0]))
            add_data(parse_block(params[2].split(":")[1]))


Tokens = \
    {
        ".cprint": attrib_cprint,
        ".org": attrib_org,
        "~COMPILER": compiler_meta,
        'hostcall': ins_hostcall,
        "lda": ins_lda,
        "ldx": ins_ldx,
        "ldy": ins_ldy
    }

if __name__ == '__main__':
    code_file = any
    if len(sys.argv) >= 3:
        code_file = load_code(sys.argv[1])
        output_file = sys.argv[2]
    elif len(sys.argv) == 2:
        code_file = load_code(sys.argv[1])
    else:
        print("Error: No input File.\nCompilation Terminated!\n")
        exit(1)

    code = code_file.read()

    lines_list = code.split('\n')

    for index in range(0, len(lines_list)):
        line = lines_list[index]

        for token in Tokens:
            # print((f"$::(B)::TOKEN={line.split(' ')[0]}=={token}"))
            if line.split(' ')[0].upper() == token.upper():
                Tokens[token](line.split(' '), index + 1)

                break

    for inline_print in inline_prints:
        print(f"INLINE PRINT: '{inline_print[0]}' at line {inline_print[1]}\n")

    print(Data)

    save(output_file, Data)
