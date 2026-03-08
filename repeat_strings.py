import math

ascii_map = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "å", "ä", "ö"]

def parse_word_list(max_len=200):
    #actual list is 8425 words long
    word_list = []
    i = 0
    with open("most_common_swedish_words.csv", "r") as f:
        for line in f:
            word_list.append(line.strip('\n').split(" ")[0])
            i += 1
            if i > max_len:
                return word_list
    return word_list

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
    for key in keys[0]:
        if keys[key] > masking_val:
            print(key, ": ", keys[key])

def generate_repeat_list(masking_val = 2, max_len = 10, min_len = 2):
    output = []
    pop_list = []
    for i in range(min_len, max_len):
        output.append(find_repeats(generate_ciphertext(), i))
        #print_repeats(output[:-1], masking_val)
    for key_dict in output:
        for key in key_dict:
            if key_dict[key] < masking_val:
                pop_list.append(key)
        for entry in pop_list:
            key_dict.pop(entry)
        pop_list = []
    return output

def generate_all_keyshifts(guess_text, partial_key, max_keylen=32, min_keylen=16):
    output_arr = []
    offset = 0
    if len(partial_key) < min_keylen:
        for i in range(min_keylen, max_keylen): #iterate through possible key lengths
            output = ""
            for j in range(0, i - len(partial_key) + 1): #iterate what index the partial key guess should start at
                if j != offset:
                    output += "-"
                else:
                    output += guess_for_partial_key(guess_text, partial_key)
            output_arr.append(output)
            offset += 1
    return output_arr

def generate_all_keyshifts_from_list(guess_arr, max_keylen=32, min_keylen=16):
    for guess in guess_arr:
        generate_all_keyshifts

#from other files
def index_of_letter(input_letter):
    if input_letter == "~":
        return 0
    return ascii_map.index(input_letter.lower())

def shift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) + index_of_letter(key_letter)) % len(ascii_map)]

def unshift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) - index_of_letter(key_letter)) % len(ascii_map)]

def decrypt_with_key(ciphertext, key):
    output = ""
    index = 0
    for i in range(0, len(ciphertext) - 1):
        if key[index%len(key)] == "-":
            output += "-"
            index += 1
        elif ciphertext[index] == "~":
            index = 0 #reset for new msg
        else:
            output += unshift_letter(ciphertext[index], key[index%len(key)])
            index += 1
    return output

def guess_for_partial_key(repeat_guess, key_guess):
    output = ""
    copy_len = 0
    if len(repeat_guess) > len(key_guess):
        copy_len = len(key_guess)
    else:
        copy_len = len(repeat_guess)
    for i in range(0, copy_len):
        output += ascii_map[index_of_letter(repeat_guess[i]) - index_of_letter(key_guess[i])]
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
    possible_keyshifts = generate_all_keyshifts(guess_text, key_guess)
    for key in possible_keyshifts:
        #do partial decryption and look for targeted phrase keyguess
        partial_decrypt = decrypt_all_seperately(key) #might be only oding 1-5
        phrase_present = False
        count = 0
        for k in range(0, len(partial_decrypt)):
            #iterate through every crypto file and count phrases found
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
                best_key = key
            #print("Found", count, " times using key:", output)
    #for k in range(0, len(partial_decrypt)):
        
        #print_decryption_aligned(best_output[k], len(best_key))
        #print("**********************")
    #print("Found", best_count, " times using key:", best_key)
    return best_key, best_count
    

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

def scan_for_all_phrases(input_key):
    total_count = 0
    was_found = False
    temp_count = 0
    temp_found = False
    all_phrases = parse_word_list()
    all_decryptions = decrypt_all_seperately(input_key)
    for i in range(0, len(all_phrases)):
        for j in range(0, len(all_decryptions)):
            temp_found, temp_count = search_for_phrase(all_decryptions[j], all_phrases[i])
            total_count += temp_count
    return total_count

def determine_best_phrase(input_text):
    #iterate through phrases to find one that finds most other phrases
    all_phrases = parse_word_list()
    all_repeats = generate_repeat_list(3, min_len=3, max_len=16)
    best_score = 0
    best_key = ""
    traversal_score = 0
    traversal_key = ""
    repeat_len = 0
    for i in range(0, len(all_phrases)):
        for repeat_arr in all_repeats:
            for repeat in repeat_arr:
                repeat_len = len(repeat)
                traversal_key, junk = see_guess_result(input_text, repeat, all_phrases[i], repeat_len)
                if traversal_key != "":
                    traversal_score = scan_for_all_phrases(traversal_key)
                    if best_score < traversal_score:
                        best_score = traversal_score
                        best_key = traversal_key
                        print("new best key: ", best_key)
                        print("new best score: ", best_score)
    return best_key



#see_guess_result(generate_ciphertext(), "ib", "en", 32) #probably not right
#see_guess_result(generate_ciphertext(), "xx", "en", 32) #these all come up with length 20

#see_guess_result(generate_ciphertext(), "sgbö", "vara", 32)
#see_guess_result(generate_ciphertext(), "sgbö", "till", 32) #was at same indicies as vara
#see_guess_result(generate_ciphertext(), "sgbö", "inte", 32)

#see_guess_result(generate_ciphertext(), "xxx", "den", 32) #probably incorrect. inconclusive
#see_guess_result(generate_ciphertext(), "xxå", "det", 32) #probably incorrect
#see_guess_result(generate_ciphertext(), "sgb", "och", 32)  #looks very promising. also seeing words like 'ost' 
#see_guess_result(generate_ciphertext(), "sgb", "ost", 32)
#see_guess_result(generate_ciphertext(), "xxx", "jag", 32)

#random check
#bs_test = decrypt_all_seperately("crypt-----------")
#print_decryption_aligned(bs_test[0], 16)   #pretty bad result but just proof of concept
#generate_repeat_list(10, min_len=2)
best_key = determine_best_phrase(generate_ciphertext())
print(best_key)
print("done")
print_decryption_aligned(decrypt_with_key(generate_ciphertext(), best_key), len(best_key))
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

