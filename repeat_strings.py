import math

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

def generate_repeat_list(masking_val = 1, max_len = 100, min_len = 2):
    for i in range(min_len, max_len):
        print_repeats(find_repeats(generate_ciphertext(), i), masking_val)

#from other files
def index_of_letter(input_letter):
    return ascii_map.index(input_letter)

def shift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) + index_of_letter(key_letter)) % len(ascii_map)]

def unshift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) - index_of_letter(key_letter)) % len(ascii_map)]

def decrypt_with_key(ciphertext, key):
    output = ""
    for i in range(0, len(ciphertext) - 1):
        if key[i%len(key)] == "-":
            output += "-"
        else:
            output += unshift_letter(ciphertext[i], key[i%len(key)])
    return output

def guess_for_partial_key(input_ciphertext, key_guess):
    output = ""
    for i in range(0, len(key_guess)):
        output += ascii_map[index_of_letter(input_ciphertext[i]) - index_of_letter(key_guess[i])]
    #print(input_ciphertext, "->", key_guess, ":", output)
    return output

def see_guess_result(input_ciphertext, guess_text, key_guess, keylen):
    #e.g see_guess_result(input, 'vara', 32)
    #iterates through all partial keys that have the 
    output = ""
    partial_decrypt = ""
    offset = 0
    best_count = 0
    best_output = []
    best_key = ""
    for i in range(16, keylen): #iterate through possible key lengths
        output = ""
        for j in range(0, i - len(key_guess) + 1): #iterate what index the partial key guess should start at
            if j != offset:
                output += "-"
            else:
                output += guess_for_partial_key(guess_text, key_guess)
        offset += 1
        #do partial decryption and look for targeted phrase keyguess
        partial_decrypt = decrypt_all_seperately(output)
        phrase_present = False
        count = 0
        for k in range(0, len(partial_decrypt)):
            temp_present, temp_count = search_for_phrase(partial_decrypt[k], key_guess)
            if temp_present:
                phrase_present = True
                count += temp_count
            temp_present = False
            temp_count = 0

        if phrase_present:
            if count > best_count:
                best_count = count
                best_output = partial_decrypt
                best_key = output
            print("Found", count, " times using key:", output)
    print("Found", best_count, " times using key:", best_key)
    for k in range(0, len(partial_decrypt)):
        
        print_decryption_aligned(best_output[k], len(best_key))
        print("**********************")

def search_for_phrase(input_text, phrase):
    phrase_len = len(phrase)
    output = False
    count = 0
    for i in range(0, len(input_text) - phrase_len):
        if input_text[i:i+phrase_len] == phrase:
            output = True
            count += 1
    return output, count

def decrypt_all_seperately(key):
    output = []
    for i in range(1, 6):
        output.append(decrypt_with_key(parse_file(str(i) + ".crypto"), key))
    return output

def print_decryption_aligned(input_text, keylen):
    for i in range(0, math.ceil(len(input_text) / keylen)):
        if (i+1)*keylen <= len(input_text):
            print(input_text[i*keylen:(i+1)*keylen])
        else:
            print(input_text[:-1*i*keylen])

#see_guess_result(generate_ciphertext(), "sgbö", "vara", 32)
#see_guess_result(generate_ciphertext(), "sgbö", "till", 32) #was at same indicies as vara

#see_guess_result(generate_ciphertext(), "xxx", "den", 32) #probably incorrect. inconclusive
#see_guess_result(generate_ciphertext(), "xxå", "det", 32) #probably incorrect
see_guess_result(generate_ciphertext(), "sgb", "och", 32)  #looks very promising. also seeing words like 'ost' 

"""
generate_repeat_list(4)

guess_for_partial_key("sgbö", "vara")
guess_for_partial_key("sgbö", "till")

guess_for_partial_key("xxx", "den")
guess_for_partial_key("xxå", "det")
guess_for_partial_key("sgb", "den")
guess_for_partial_key("xxx", "och")
"""
"""
vara = sgbö ?
so partial key would be:

"""

