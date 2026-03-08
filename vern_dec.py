import math
import time
from pathlib import Path
import re

ALPHABET = "abcdefghijklmnopqrstuvwxyzåäö"
ALPHABET_LEN = len(ALPHABET)

def load_monograms(path):
    # loads the character frequencies from a file
    # returns a dictionary with probabilities for each character
    freqs = {}
    total = 0

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            char, count = line.strip().split()
            count = int(count)
            freqs[char] = count
            total += count

    for char in freqs:
        freqs[char] /= total

    return freqs

def vigenere_decrypt(ciphertext, key):
    # decrypts the ciphertext using the vigenere cipher with the given key
    # basically shifts each letter back by the key amount
    plaintext = []
    key_indices = [ALPHABET.index(k) for k in key]
    index = 0
    for i, c in enumerate(ciphertext):
        index += 1
        if c == '~':
            index = 0
        elif c not in ALPHABET:
            continue
        else:
            c_idx = ALPHABET.index(c)
            k_idx = key_indices[index % len(key)]
            p_idx = (c_idx - k_idx) % ALPHABET_LEN
            plaintext.append(ALPHABET[p_idx])

    return "".join(plaintext)

def score_text(text, monograms):
    # gives a score to see how much the text looks like real swedish
    # higher score = more likely to be correct
    score = 0.0
    floor = 1e-10  # for unseen characters

    for c in text:
        score += math.log(monograms.get(c, floor))

    return score

def best_shift_for_column(column, monograms):
    # tries all possible shifts for a column and picks the best one
    # used to find one character of the key
    best_score = float("-inf")
    best_shift = 0

    for shift in range(ALPHABET_LEN):
        decrypted = []
        for c in column:
            if c != '~':
                idx = (ALPHABET.index(c) - shift) % ALPHABET_LEN
                decrypted.append(ALPHABET[idx])

        score = score_text(decrypted, monograms)

        if score > best_score:
            best_score = score
            best_shift = shift

    return best_shift

def guess_key(ciphertext, key_length, monograms):
    # figures out what the key probably is by analyzing each column
    # splits the ciphertext into columns and finds the best shift for each
    key = []

    for i in range(key_length):
        column = ciphertext[i::key_length]
        shift = best_shift_for_column(column, monograms)
        key.append(ALPHABET[shift])

    return "".join(key)

def break_vigenere(ciphertext, monograms, max_key_len=128):
    # tries different key lengths and picks the one that gives the best result
    # this is the main function that cracks the cipher
    best_result = None
    best_score = float("-inf")

    for key_len in range(1, max_key_len + 1):
        key = guess_key(ciphertext, key_len, monograms)
        plaintext = vigenere_decrypt(ciphertext, key)
        score = score_text(plaintext, monograms) - 0.5 * key_len

        if score > best_score:
            best_score = score
            best_result = (key_len, key, plaintext)

    return best_result

def reduce_key(key):
    # checks if the key is just a pattern repeated, and shortens it if so
    # for example "abcabc" becomes "abc"
    for i in range(1, len(key)//2 + 1):
        if key[:i] * (len(key)//i) == key:
            return key[:i]
    return key

def read_ciphertexts_from_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")

    ciphertexts = []
    def natural_sort_key(path):
        return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.name)]

    for file_path in sorted(folder.glob("*.crypto"), key=natural_sort_key):
        content = file_path.read_text(encoding="utf-8").lower()
        cleaned = "".join(c for c in content if c in ALPHABET)

        if cleaned:
            ciphertexts.append((file_path.name, cleaned))

    return ciphertexts
"""
BASE_DIR = Path(__file__).resolve().parent
monograms = load_monograms(BASE_DIR / "swedish_monograms.txt")
cipher_folder = BASE_DIR / "ciphertexts (from students)"
ciphertexts = read_ciphertexts_from_folder(cipher_folder)

if not ciphertexts:
    print(f"No .crypto files found in {cipher_folder}")

for file_name, ciphertext in ciphertexts:
    start_time = time.time()
    key_len, key, plaintext = break_vigenere(ciphertext, monograms)
    key = reduce_key(key)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nFile: {file_name}")
    print("Key length:", key_len)
    print("Key:", key)
    print("Plaintext:", plaintext)
    print(f"Decryption time: {elapsed_time:.4f} seconds")
"""
def generate_ciphertext(suspected_keylen):
    ciphertext = ""
    fname = ""
    for i in range(1, 6):
        fname = str(i)
        fname += ".crypto"
        ciphertext += parse_file(fname, suspected_keylen)
    return ciphertext

def parse_file(filename, suspected_keylen = -1):
    if suspected_keylen == -1:
        output = ""
        with open(filename, "r") as f:
            for line in f:
                output += line
        output += "~"
        return output
    else:
        output = ""
        total_len = 0
        with open(filename, "r") as f:
            for line in f:
                total_len += len(line)
                output += line
        #calc how much to trim off
        amount_to_cut = total_len % suspected_keylen
        output = output[:-1*amount_to_cut]
        return output

for i in range(16, 120):
    ciphertext = generate_ciphertext(i)
    monograms = load_monograms("swedish_monograms.txt")
    start_time = time.time()
    key_len, key, plaintext = break_vigenere(ciphertext, monograms)
    key = reduce_key(key)
    end_time = time.time()
    elapsed_time = end_time - start_time

    #print(f"\nFile: {file_name}")
    if key_len >= 16:
        print("Key length:", key_len)
        print("Key:", key)
        print("Plaintext:", plaintext)
        print(f"Decryption time: {elapsed_time:.4f} seconds")

