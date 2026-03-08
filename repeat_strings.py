class key_loc_pair:
    def __init__(self, key, location):
        #location is the index in the larger string
        self.key = key
        self.count = 1
        self.locations = []
        self.locations.append(location)
    
    def add_location(self, location):
        self.count = self.count + 1
        self.locations.append(location)

    def print_pair(self, masking_val = 0):
        if self.count > masking_val:
            print("key:       ", self.key)
            print("count:     ", self.count)
            print("locations: ", self.locations)
            print("min_dist:  ", self.analyze_dist())
            print("--------------------")
    
    def analyze_dist(self):
        smallest_dist = 5000
        second_smallest = 5000
        for loc in self.locations:
            for other_loc in self.locations:
                if loc != other_loc:
                    if abs(loc - other_loc) < smallest_dist:
                        smallest_dist = abs(loc - other_loc)
                    if abs(loc - other_loc) < second_smallest and abs(loc - other_loc) > smallest_dist:
                        second_smallest = abs(loc - other_loc)
        return smallest_dist, second_smallest, second_smallest - smallest_dist

class key_loc_pair_list:
    def __init__(self):
        self.key_loc_pairs = []
    
    def add_pair(self, new_pair : key_loc_pair):
        #if pair does not already exist, add it. Otherwise add loc to pair. Only works for pairs with 1 location
        found = False
        for pair in self.key_loc_pairs:
            if pair.key == new_pair.key:
                pair.add_location(new_pair.locations[0])
                found = True
                break
        if not found:
            self.key_loc_pairs.append(new_pair)
    
    def self_sort(self):
        #sorts based on most common duplicates
        #just some bubble sort
        #also pops anything that has a count of < 2
        for i in range(0, len(self.key_loc_pairs)):
            for j in range(0, len(self.key_loc_pairs) - 1):
                if self.key_loc_pairs[i].count > self.key_loc_pairs[j].count:
                    temp = self.key_loc_pairs[j]
                    self.key_loc_pairs[j] = self.key_loc_pairs[i]
                    self.key_loc_pairs[i] = temp
        index = 0
        while index < len(self.key_loc_pairs):
            if self.key_loc_pairs[index].count < 2:
                self.key_loc_pairs.pop(index)
            else:
                index += 1
    
    def print_all(self, masking_val = 0):
        for pair in self.key_loc_pairs:
            pair.print_pair(masking_val)


def generate_ciphertext(suspected_keylen = -1):
    ciphertext = ""
    fname = ""
    for i in range(1, 6):
        fname = str(i)
        fname += ".crypto"
        ciphertext += parse_file(fname, suspected_keylen)
    new_filename = str(suspected_keylen) + ".crypto"
    with open(new_filename, "w") as f:
        f.write(ciphertext)
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

def find_repeats(ciphertext, repeat_len):
    keys = {}
    key_loc_pairs = key_loc_pair_list()
    i = 0
    key = ""
    for i in range(0, len(ciphertext) - repeat_len):
        key = ciphertext[i:i+repeat_len]
        if not key in keys:
            keys[key] = 1
            key_loc_pairs.add_pair(key_loc_pair(key, i))
        else:
            keys[key] += 1
            key_loc_pairs.add_pair(key_loc_pair(key, i))
    key_loc_pairs.self_sort()
    return key_loc_pairs

def generate_repeat_list(masking_val = 1):
    for j in range(16, 128):
        pair_lists = []
        for i in range(2, 16):
            
                #testing for each suspected keylength
                pair_lists.append(find_repeats(generate_ciphertext(j), i))
        for list in pair_lists:
            list.print_all(masking_val)
        return pair_lists

pair_lists = generate_repeat_list(3)

