ascii_map = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "å", "ä", "ö"]

def generate_ciphertext():
    ciphertext = ""
    fname = ""
    for i in range(1, 6):
        fname = str(i)
        fname += ".crypto"
        ciphertext += parse_file(fname)
    #print(ciphertext)
    return ciphertext

def parse_file(filename):
    output = ""
    with open(filename, "r") as f:
        for line in f:
            output += line
    output += "~"
    return output

def find_repeats(ciphertext, repeat_len):
    keys = {}
    i = 0
    key = ""
    for i in range(0, len(ciphertext) - repeat_len):
        key = ciphertext[i:i+repeat_len]
        if not key in keys:
            keys[key] = 1
        else:
            keys[key] += 1
    return keys

def print_repeats(keys, masking_val = 1):
    for key in keys:
        if keys[key] > masking_val:
            print(key, ": ", keys[key])

def generate_repeat_list(masking_val = 1):
    for i in range(3, 16):
        print_repeats(find_repeats(generate_ciphertext(), i), masking_val)

#from other files
def index_of_letter(input_letter):
    return ascii_map.index(input_letter)

def shift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) + index_of_letter(key_letter)) % len(ascii_map)]

def unshift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) - index_of_letter(key_letter)) % len(ascii_map)]

def guess_for_partial_key(input_ciphertext, key_guess):
    output = ""
    for i in range(0, len(key_guess)):
        output += ascii_map[index_of_letter(input_ciphertext[i]) - index_of_letter(key_guess[i])]
    print(input_ciphertext, "->", key_guess, ":", output)
    return output

generate_repeat_list(2)
guess_for_partial_key("sgbö", "vara")
guess_for_partial_key("sgbö", "till")

guess_for_partial_key("xxx", "den")
guess_for_partial_key("xxå", "det")
guess_for_partial_key("sgb", "den")
guess_for_partial_key("xxx", "och")
"""
vara = sgbö ?
so partial key would be:

"""

