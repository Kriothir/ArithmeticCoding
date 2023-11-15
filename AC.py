import numpy as np
import sys
from io import StringIO
from itertools import groupby
import math
import time
np.set_printoptions(suppress=True)

symbols = []
counter = 0
input_file = str(sys.argv[2])
output_file = str(sys.argv[3])
command = str(sys.argv[1])

if command == 'c':
    with open(input_file, "rb") as in_file:
        while True:
            chunk = in_file.read(1)
            s = int.from_bytes(chunk, byteorder='big')
            symbols.append(s)
            if chunk == b"":
                break
            counter = counter + 1

    start = time.time()

    symbol_count = len(list(set(symbols)))
    cummulative_frequency = len(symbols)


    stevec = 0
    lower_val = 0

    frequency_table = {}
    for item in symbols:
        frequency_table[item] = frequency_table.get(item, 0) + 1

    test = frequency_table.items()
    arr = np.array(list(frequency_table.items())[:len(frequency_table)])
    frequency_table = np.zeros((symbol_count, 5))

    for i in range(symbol_count):
        frequency_table[i][0] = arr[i][0]
        frequency_table[i][1] = arr[i][1]
        frequency_table[i][2] = arr[i][1] / cummulative_frequency
        frequency_table[i][3] = lower_val
        frequency_table[i][4] = lower_val + arr[i][1]
        lower_val = lower_val + arr[i][1]


    def write_frequency_table(f, table):
        for e in table:
            e = int(e)
            f.write(e.to_bytes(4, byteorder='big', signed=False))


    def encodeArt():
        E3_counter = 0
        binary_string = ""
        bits = 32
        spMeja = 0
        zgMeja = 2 ** (bits - 1) - 1

        drugaCetrtina = math.floor((zgMeja + 1) / 2)
        prvaCetrtina = math.floor(drugaCetrtina / 2)
        tretjaCetrtina = math.floor(prvaCetrtina * 3)

        for i in range(0, counter):
            korak = int((zgMeja - spMeja + 1) / counter)
            current_char_index = list(zip(*np.where(frequency_table[:, 0] == symbols[i])))
            zgMeja = spMeja + korak * frequency_table[current_char_index[0][0]][4] - 1
            spMeja = spMeja + korak * frequency_table[current_char_index[0][0]][3]

            while ((zgMeja < drugaCetrtina) or (spMeja >= drugaCetrtina)):
                if zgMeja < drugaCetrtina:
                    spMeja = spMeja * 2
                    zgMeja = (zgMeja * 2) + 1
                    binary_string += '0'
                    binary_string += E3_counter * '1'
                    E3_counter = 0
                if spMeja >= drugaCetrtina:
                    spMeja = 2 * (spMeja - drugaCetrtina)
                    zgMeja = 2 * (zgMeja - drugaCetrtina) + 1
                    binary_string += '1'
                    binary_string += E3_counter * '0'
                    E3_counter = 0

            while ((spMeja >= prvaCetrtina) and (zgMeja < tretjaCetrtina)):
                spMeja = 2 * (spMeja - prvaCetrtina)
                zgMeja = 2 * (zgMeja - prvaCetrtina) + 1
                E3_counter = E3_counter + 1

        if spMeja < prvaCetrtina:
            binary_string += "01"
            binary_string += E3_counter * '1'
        else:
            binary_string += "10"
            binary_string += E3_counter * '0'

        minimum_table = np.delete(frequency_table, [1, 2], axis=1)
        minimum_table = minimum_table.ravel()
        minimum_table = list(minimum_table)
        end = time.time()
        print(end - start)
        ##Write encoded string
        sio = StringIO(binary_string)
        table_len = len(minimum_table)
        with open(output_file, 'wb') as f:
            f.write(table_len.to_bytes(32, byteorder='big'))
            f.write(counter.to_bytes(32, byteorder='big'))
            write_frequency_table(f, minimum_table)
            while 1:
                b = sio.read(8)
                if not b:
                    break
                i = int(b, 2)
                f.write(i.to_bytes(1, byteorder='big'))
        print("Table length", table_len)
        print("Symbol count: ", counter)

    #####################################################################
    encodeArt()
    print("Encoding Done!")
    ############Here#######

def read_frequency_table(f, table_length):
    read_table = []
    for _ in range(table_length):
        data = f.read(4)
        number = int.from_bytes(data, 'big', signed=False)
        read_table.append(number)
    return read_table

def decodeArt():
    bits = 32
    counter = 0
    bit_string = ""
    freq_table = []
    spMeja = 0
    zgMeja = 2 ** (bits - 1) - 1

    drugaCetrtina = math.floor((zgMeja + 1) / 2)
    prvaCetrtina = math.floor(drugaCetrtina / 2)
    tretjaCetrtina = math.floor(prvaCetrtina * 3)

    tablelen = 0
    with open(input_file, 'rb') as f:
        data = f.read(32)
        tablelen = int.from_bytes(data, 'big')
        data = f.read(32)
        counter = int.from_bytes(data, 'big')
        freq_table = read_frequency_table(f, tablelen)
        bit_string = "".join(f"{n:08b}" for n in f.read())
    freq_table = np.array(freq_table)
    freq_table = np.reshape(freq_table, (int(len(freq_table) / 3), 3))
    polje = bit_string[0:bits - 1]
    polje = int(polje, 2)
    spMeja = 0
    zgMeja = 2 ** (bits - 1) - 1
    uncompressed = ""
    bit_counter = 0
    next_bit = 0
    start = time.time()
    print("hello")

    if (bit_string[bits - 1 + bit_counter:bits + bit_counter]):
        next_bit = int(float(bit_string[bits - 1 + bit_counter:bits + bit_counter]))
    else:
        next_bit = 0
    for i in range(0, counter ):
        korak = int((zgMeja - spMeja + 1) / counter)


        vrednost = int((polje - spMeja) / korak)
        char_index = list(zip(*np.where((freq_table[:, 1] <= vrednost) & (freq_table[:, 2] > vrednost))))

        uncompressed += chr(int(freq_table[char_index[0][0]][0]))

        zgMeja = spMeja + korak * freq_table[char_index[0][0]][2] - 1
        spMeja = spMeja + korak * freq_table[char_index[0][0]][1]

        while (zgMeja < drugaCetrtina) or (spMeja >= drugaCetrtina):
            if zgMeja < drugaCetrtina:
                spMeja = spMeja * 2
                zgMeja = (zgMeja * 2) + 1
                polje = (2 * polje) + next_bit
                bit_counter = bit_counter + 1
                if (bit_string[bits - 1 + bit_counter:bits + bit_counter]):
                    next_bit = int(float(bit_string[bits - 1 + bit_counter:bits + bit_counter]))
                else:
                    next_bit = 0

            if spMeja >= drugaCetrtina:
                spMeja = 2 * (spMeja - drugaCetrtina)
                zgMeja = 2 * (zgMeja - drugaCetrtina) + 1
                polje = (2 * (polje - drugaCetrtina)) + next_bit
                bit_counter = bit_counter + 1
                if (bit_string[bits - 1 + bit_counter:bits + bit_counter]):
                    next_bit = int(float(bit_string[bits - 1 + bit_counter:bits + bit_counter]))
                else:
                    next_bit = 0

        while (spMeja >= prvaCetrtina) and (zgMeja < tretjaCetrtina):
            spMeja = 2 * (spMeja - prvaCetrtina)
            zgMeja = 2 * (zgMeja - prvaCetrtina) + 1
            polje = (2 * (polje - prvaCetrtina)) + next_bit
            bit_counter = bit_counter + 1
            if (bit_string[bits - 1 + bit_counter:bits + bit_counter]):
                next_bit = int(float(bit_string[bits - 1 + bit_counter:bits + bit_counter]))
            else:
                next_bit = 0
    end = time.time()
    print(end - start)
    newFile = open(output_file, "wb")
    for byte in uncompressed:
        num = ord(byte)
        newFile.write(num.to_bytes(1, byteorder='big'))
    #print(uncompressed)

if command == 'd':
    decodeArt()

