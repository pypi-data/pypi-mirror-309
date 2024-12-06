# अग्निमीळे पुरोहितं यज्ञस्य देवम् ऋत्विजं होतारं रत्न धातमम्
# त्रि॒व॒न्धु॒रेण॑ त्रि॒वृता॒ रथे॒ना या॑तमश्विना । मध्व॒: सोम॑स्य पी॒तये॑  सोम॑स्य पी॒तये॑

# <editor-fold desc="importing libraries">
import re
import sympy as sp
# </editor-fold>


# <editor-fold desc="translator">





def latin(text):
    '''Converts any devangiri text to latin text'''
    conversiontable = {'ॐ': 'oṁ', 'ऀ': 'ṁ', 'ँ': 'ṃ', 'ं': 'ṃ', 'ः': 'ḥ', 'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī',
                       'उ': 'u', 'ऊ': 'ū', 'ऋ': 'r̥', 'ॠ': ' r̥̄', 'ऌ': 'l̥', 'ॡ': ' l̥̄', 'ऍ': 'ê', 'ऎ': 'e', 'ए': 'e',
                       'ऐ': 'ai', 'ऑ': 'ô', 'ऒ': 'o', 'ओ': 'o', 'औ': 'au', 'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u',
                       'ू': 'ū', 'ृ': 'r̥', 'ॄ': ' r̥̄', 'ॢ': 'l̥', 'ॣ': ' l̥̄', 'ॅ': 'ê', 'े': 'e', 'ै': 'ai',
                       'ॉ': 'ô', 'ो': 'o', 'ौ': 'au', 'क़': 'q', 'क': 'k', 'ख़': 'x', 'ख': 'kh', 'ग़': 'ġ', 'ग': 'g',
                       'ॻ': 'g', 'घ': 'gh', 'ङ': 'ṅ', 'च': 'c', 'छ': 'ch', 'ज़': 'z', 'ज': 'j', 'ॼ': 'j', 'झ': 'jh',
                       'ञ': 'ñ', 'ट': 'ṭ', 'ठ': 'ṭh', 'ड़': 'ṛ', 'ड': 'ḍ', 'ॸ': 'ḍ', 'ॾ': 'd', 'ढ़': 'ṛh', 'ढ': 'ḍh',
                       'ण': 'ṇ', 'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n', 'प': 'p', 'फ़': 'f', 'फ': 'ph',
                       'ब': 'b', 'ॿ': 'b', 'भ': 'bh', 'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'ळ': 'ḷ', 'व': 'v',
                       'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h', 'ऽ': '\'', '्': '', '़': '', '०': '0', '१': '1',
                       '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9', 'ꣳ': 'ṁ',
                       '।': '.', '॥': '..', ' ': ' ', }
    latin_text = ""

    for char in text:
        latin_text += conversiontable.get(char, char) + ', '

    return latin_text
# </editor-fold>


# <editor-fold desc="remove unnessacary">
def vowels(devanagari_text):
    '''removes the vowels from any devangiri text'''
    pattern = r"[ा-ौ]"
    devanagari_text = re.sub(pattern, '', devanagari_text)
    return devanagari_text


def remove(text):
    '''removes half letters from any text'''
    s = re.sub('क्ष', 'ष', text)
    s = re.sub('श्र', 'र', s)
    s = re.sub('त्र', 'त', s)
    s = re.sub('ज्ञ', 'ञ', s)
    nx = separate_half_letters(s)
    a = nx
    a = vowels(a)
    return a


def separate_half_letters(devanagari_word):
    '''To be used by the remove() function'''
    pattern = r'([क-ह][्])([क-ह])'

    def replace_half_letter(match):
        return match.group(2)

    separated_word = re.sub(pattern, replace_half_letter, devanagari_word)
    return separated_word






# </editor-fold>


# <editor-fold desc="number conversion">
def katapayadi_number(shloka):
    '''converts shloka which was processed from the remove() and vowels() function '''
    katapayadi_map = {
        'क': 1, 'ख': 2, 'ग': 3, 'घ': 4, 'ङ': 5,
        'च': 6, 'छ': 7, 'ज': 8, 'झ': 9, 'ञ': 0,
        'ट': 1, 'ठ': 2, 'ड': 3, 'ढ': 4, 'ण': 5,
        'त': 6, 'थ': 7, 'द': 8, 'ध': 9, 'न': 0,
        'प': 1, 'फ': 2, 'ब': 3, 'भ': 4, 'म': 5,
        'य': 1, 'र': 2, 'ल': 3, 'व': 4,
        'श': 5, 'ष': 6, 'स': 7, 'ह': 8, 'ॹ': 8, 'ळ': 9,
        'अ': None, 'आ': None, 'इ': None, 'ई': None, 'उ': None, 'ऊ': None, 'ऋ': None, 'ए': None,
        'ऐ': None, 'ओ': None, 'औ': None, 'अं': None, 'अः': None,
        'ा': None, 'ि': None, 'ी': None, 'ु': None, 'ू': None, 'ृ': None, 'े': None, 'ै': None, 'ो': None, 'ौ': None,
        'ं': None, 'ँ': None, 'ऱ': 2, 'र्': 2
    }
    filtered_dict = {k: vs for k, vs in katapayadi_map.items() if vs not in ('', None)}
    number_representation = []
    nm = []
    for char in shloka:
        if char in filtered_dict:
            number_representation.append(str(filtered_dict[char]))
            nm.append(char)
    pq = number_representation
    res = ''
    for s in pq:
        res += s
    res = res.strip()
    return res
# </editor-fold>


# <editor-fold desc="equations">
x = sp.symbols('x')




def create_polynomialss(coefficients):
    '''converts the numbers got by the katapayadi numbers function to equations'''
    coefficients = list(coefficients)
    xps = sp.symbols('x')
    degree = len(coefficients) - 1
    polynomialx = sum(int(coeff) * xps**(int(degree) - int(i)) for i, coeff in enumerate(coefficients) if coeff != 0)
    return polynomialx



def karma_Ghana_conversion(sentence):
    '''A additional aid that if you use will make a another equation if you make a equation from the output of this'''
    words = sentence.split()
    karma_patha = []
    for i in range(len(words) - 1):
        pair = f"{words[i]}-{words[i + 1]}"
        karma_patha.append(pair)
    return ''.join(karma_patha)



# </editor-fold>
