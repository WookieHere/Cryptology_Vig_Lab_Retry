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

generate_repeat_list(3)

