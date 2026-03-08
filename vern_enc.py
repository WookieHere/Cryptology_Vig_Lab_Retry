ascii_map = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "å", "ä", "ö"]

class char_freq_map:
    def __init__(self):
        self.total_chars = 0
        self.char_map = {}
        for char in ascii_map:
            self.char_map[char] = 0
    
    def increment_char(self, char):
        self.char_map[char] += 1
        self.total_chars += 1

    def diff_map(self, truth_map, shift = 0):
        total = 0
        for i in range(0, len(self.char_map)):
            freq_char_self = self.char_map[ascii_map[(i + shift) % len(self.char_map)]]
            freq_self = (self.char_map[ascii_map[(i + shift) % len(self.char_map)]])/self.total_chars
            true_freq = (truth_map.char_map[ascii_map[i]])/truth_map.total_chars
            total += abs(freq_self - true_freq)
        return total
    
    def set_char(self, char, value, total = -1):
        #only used by truth map
        self.char_map[char] = value
        self.total_chars = total
    
class caeser:
    def __init__(self):
        self.char_freq = char_freq_map()
        self.values = ""
        self.shift = 0
    
    def shift_values(self, amount):
        return encrypt_phrase(self.values, ascii_map.index(amount))
    
    def find_best_shift(self, truth_map):
        min = 999999
        temp = 0
        min_index = 0
        for i in range(0, len(ascii_map)):
            temp = self.char_freq.diff_map(truth_map, i)
            if temp < min:
                min = temp
                min_index = i
        return min_index
    
    def insert_val(self, char):
        self.values += char
        self.char_freq.increment_char(char)

def index_of_letter(input_letter):
    return ascii_map.index(input_letter)

def shift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) + index_of_letter(key_letter)) % len(ascii_map)]

def unshift_letter(input_letter, key_letter):
    return ascii_map[(index_of_letter(input_letter) - index_of_letter(key_letter)) % len(ascii_map)]

def encrypt_phrase(input_phrase, input_key):
    new_word = ""
    for i in range(0, len(input_phrase)):
        if input_phrase[i] != ' ' and ascii_map.count(input_phrase[i]) != 0:
            new_word += shift_letter(input_phrase[i], input_key[i % len(input_key)])
    #print(new_word)
    return new_word

def gen_caesers(ciphertext, key_len):
    caesers = [caeser() for i in range(key_len)]
    index = 0
    for i in range(0, len(ciphertext)):
        if ciphertext[i] == '~':
            index = 0
        else:
            caesers[index%key_len].insert_val(ciphertext[i])
            index += 1
    return caesers

def decrypt_with_key(ciphertext, key):
    output = ""
    for i in range(0, len(ciphertext) - 1):
        output += unshift_letter(ciphertext[i], key[i%len(key)])
    return output

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

#input_phrase = "vispa ut mjölet i hälften av mjölken till en slät smet vispa i resterande mjölk ägg och salt låt pannkakssmeten svälla ca tio min så håller pannkakorna håller ihop bättre hetta upp smör och rapsolja i en stekpanna värm först upp pannan på hög värme så pannan blir riktigt varm häll ner smet och stek tunna fina pannakor vänd pannkakan när den stelnat lossnat i kanterna och fått stekyta tillsätt lite mer smör och rapsolja till stekpannan med jämna mellanrum i en gjutjärnspanna går det åt mycket fett i en non stick panna räcker det med nytt fett till varje tredje pannkaka"
#input_phrase = "Tidigare har det funnits vidsträckta svenskspråkiga områden i Estland, i synnerhet längs den nordvästra kusten och på öarna Dagö, Ösel och Ormsö. Den svensktalande minoriteten var representerad i parlamentet och hade rätt att använda språket i offentliga tal och debatter. I mitten av 1600-talet var antalet estlandssvenskar omkring 10 000 personer, vilket motsvarade 2-3 procent av landets dåtida befolkning.[15] Efter den svenska förlusten av Baltikum till Ryssland på 1700-talet, tvångsförflyttades runt 1 000 estländska svenskar från Dagö till Ukraina där de grundade byn Gammalsvenskby norr om Krimhalvön. Av dessa återstår endast ett fåtal ättlingar som idag är gamla och fortfarande talar svenska som modersmål, följer den svenska kalendern och beaktar svenska seder, och den mycket ålderdomliga östsvenska dialekten kommer med största säkerhet att dö ut inom en generation. I Estland blev den svensktalande minoriteten till en början väl behandlad under mellankrigstiden, men under trettiotalet gjorde sig estnisk nationalism påmind och man påtvingade befolkningen namnbyteskampanjer, där nyuppfunna, estniskklingande namn skulle ersätta de ursprungliga svenska orts-, gårds- och familjenamnen. Kommuner där svensktalare var i majoritet hade svenska som administrativt språk och estlandssvensk kultur hade ett smärre uppsving. Under andra världskriget, då Estland blev en del av Sovjetunionen, flydde de flesta estlandssvenskar (cirka 80 procent) till Sverige, många deporterades till Sibirien[16] och de cirka 1 500 som blev kvar i det sovjetockuperade Estland hade mycket små möjligheter att bevara sin identitet och sitt språk på grund av den ryska synen på svenskarna som potentiella spioner och förrädare. Många valde att dölja sin svenska identitet och bytte språk till estniska för att undvika förföljelse och yrkesförbud. På grund av detta återstår idag endast en handfull äldre som talar genuin dialekt. Enligt folkräkningen 2000 fanns det 300 etniska svenskar i Estland, varav 211 hade estniskt medborgarskap.[17] Eftersom det antas att alla inte uppger sin etniska bakgrund har antalet estlandssvenskar i Estland uppskattats till cirka tusen.[18]I Amerika har det tidvis funnits svensktalande grupper, på 1600-talet i nuvarande Delaware (på den tiden Nya Sverige), på 1800-talet i till exempel Bishop Hill i Illinois samt i Minnesota, men dessa har i regel assimilerats och antagit det omgivande majoritetsspråket engelska inom en eller ett par generationer.Också i Argentina, särskilt kring byn Oberá som grundades av inflyttade svenskar, har det funnits svensktalande grupper av vilka uppskattningsvis ett hundratal svensktalande lever än idag. Fram tills på 1950-talet bedrevs svensk skolundervisning i staden och än idag bedrivs språkundervisning i mindre utsträckning bland svenskättlingarna.[19]I slutet på 1800-talet skall det också ha funnits en betydande svensktalande koloni i nuvarande Namibia, även om den emellertid sedermera assimilerats till omgivande språkgrupper.[20] "
#input_phrase = "ba ba"
#input_key = "abcdefghijklmnop"
#input_key = "aa"
#ciphertext = encrypt_phrase(input_phrase, input_key)
#print(ciphertext)
#stripped_text = encrypt_phrase(input_phrase, "a")

truth_dict = {
    "a" : 7728424,
    "b" : 1264526,
    "c" : 1224048,
    "d" : 3872788,
    "e" : 8359837,
    "f" : 1669202,
    "g" : 2357537,
    "h" : 1721729,
    "i" : 4791440,
    "j" : 505602,
    "k" : 2586468,
    "l" : 4345176,
    "m" : 2858614,
    "n" : 7036256,
    "o" : 3691462,
    "p" : 1514535,
    "q" : 16063,
    "r" : 6944392,
    "s" : 5428201,
    "t" : 6335156,
    "u" : 1580734,
    "v" : 1989291,
    "w" : 117047,
    "x" : 130803,
    "y" : 583261,
    "z" : 57387,
    "å" : 1102225,
    "ä" : 1480353,
    "ö" : 1075107,
}
truth_map = char_freq_map()
total = 0
for char in truth_dict:
    truth_map.set_char(char, truth_dict[char])
    total += truth_dict[char]
truth_map.set_char("a", truth_dict["a"], total)


ciphertext = generate_ciphertext()
test_caesers = []

for i in range(17, 45):
    test_caesers.append(gen_caesers(ciphertext, i))
#true_caeser = gen_caesers(stripped_text, 1)

assumed_key = ""
true_key = ""

for j in range(0, len(test_caesers)):
    assumed_key = ""
    loop_caesers = test_caesers[j]
    for i in range(0, len(loop_caesers)):
        assumed_key += ascii_map[loop_caesers[i].find_best_shift(truth_map)]
        #true_key += ascii_map[caesers[i].find_best_shift(true_caeser[0].char_freq)]

    print("assumed key with limited plaintext info: ", assumed_key)
    print("Output plaintext: ", decrypt_with_key(parse_file("1.crypto"), assumed_key))
    print("----------------------------------")
    #print("solved key with full plaintext info: ", true_key)