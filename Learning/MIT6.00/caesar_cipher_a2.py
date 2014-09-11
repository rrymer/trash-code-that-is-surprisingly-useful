# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 12:24:49 2014

@author: pczrr
"""

# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random
import numbers

WORDLIST_FILENAME = "/tmp/words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("/tmp/fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers. The empty space counts as the 27th letter
    of the alphabet, so spaces should be mapped to a lowercase letter as
    appropriate.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
#    assert shift >= 0 and shift < 27, 'shift %s is not between 0 and 27' % shift
    #numbers.Integral used in case of long integers
    assert isinstance(shift, numbers.Integral), 'shift is not an integer'
    
    coder = {}

    lowercase_and_space = string.ascii_lowercase + ' '
    uppercase_and_space = string.ascii_uppercase + ' '

    # Shift letters over shift places
    shifted_lowercase_and_space = lowercase_and_space[shift:] + lowercase_and_space[:shift]
    shifted_uppercase_and_space = uppercase_and_space[shift:] + uppercase_and_space[:shift]

    # Construct Caesar cipher dictionary
    # Add uppercase letters first so ' ' will be overwritten to point to lowercase letter
    for i in range(len(uppercase_and_space)):
        coder[uppercase_and_space[i]] = shifted_uppercase_and_space[i]

    for i in range(len(lowercase_and_space)):
        coder[lowercase_and_space[i]] = shifted_lowercase_and_space[i]

    return coder
        
    

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    return build_coder(shift)

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    return build_coder(27-shift)
 

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    alphabet='abcdefghijklmnopqrstuvwxyz '
    ciphertext=''
    for c in text:
        if c.lower() in alphabet:
            ciphertext += coder[c]
        else:
            ciphertext += c
    return ciphertext
  

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    alphabet='abcdefghijklmnopqrstuvwxyz '
    encoder = build_encoder(shift)
    ciphertext=''
    for c in text:
        if c.lower() in alphabet:
            ciphertext += encoder[c]
        else:
            ciphertext += c
    return ciphertext
   
#
# Problem 2: Codebreaking.
#
def real_words(wordlist,text):
    """
    returns a list of words found in an english dictionary
    """
    words = text.split(' ')
    real_words = []
    last_word = 'buy'
    for word in words:
        if is_word(wordlist,word) and is_word(wordlist,last_word):
            real_words.append(word)
        last_word = word
    return real_words

def find_word(wordlist,text,i):
    """
    searches characterize wise through a string, stops at a space, and checks to see if preceeding letters form a word
    return True or False
    """
    cand=''
    coder = build_decoder(i)
#    print decoder, i
    for c in text:
        if c in coder.keys():
            cand += coder[c]
        else:
            continue
        if ' ' in cand:
            print 'found a word!',cand,i
#            print is_word(wordlist,cand)
            return is_word(wordlist,cand)
        else:
            continue
    return False   
   
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    break up input into individual elements
    initialize shift, message
    for the first element:
        try a series of shifts until is_word == True
        return shift
    now, try that shift on the remaining words serially,
        if at any time a result is not a word, go back to step one.
    """
    print len(text)
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    i=0
    max_words = 0
    best_words = None
    best_shift = None
    best_index = 0
    possibles = []
    while i <= len(alphabet)-1:
        print i
        if find_word(wordlist,text[:20],i):
            print 'now checking the rest of the message with shift %d' % (27-i)
            decrypted = real_words(wordlist,apply_shift(text,27-i))
            words = len(decrypted)
            if words >= max_words:
                if best_shift:
                    possibles.append((best_index,best_shift,best_words))
                max_words = words
                best_shift = 27-i
                best_words = decrypted
                for d in decrypted:  
                    best_index = 0
                    best_index += (len(d) + 1)
                if possibles:
                    possibles.append((best_index,best_shift,best_words))
                i += 1
                continue
            else:
                i += 1
                continue
        else:
            i += 1
            continue
    if best_shift:
        if possibles:
            i = 0
            for p in possibles:
                print i,p[0],p[1],p[2]
                i += 1
            chosen = int(raw_input('enter number of best shift'))
#            assert isinstance(chosen, numbers.Integral), 'you must enter an integer here'
#            assert chosen >= 0 and chosen <= i, 'you must pick from the list'
            best_index = possibles[chosen][0]
            best_shift = possibles[chosen][1]
            best_words = possibles[chosen][2]
        print best_shift
        print best_index
        print best_words
        print 'decrypted text',apply_shift(text,best_shift)
        return best_index, best_shift, apply_shift(text,best_shift)
    else:   
        return None, None, None
   
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    if shifts:
        message=''
        to_encrypt = text[shifts[0][0]:]
        remaining = text[:(len(text) - len(to_encrypt))]
        encrypted = apply_shift(to_encrypt,shifts[0][1])
        message = remaining + encrypted
        return apply_shifts(message,shifts[1:])
    else:
#        print 'message=',text
        return text
    
        
 
#
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
    return find_best_shifts_rec(wordlist,text,0)

def recover(text,shifts):
    pass
#    last_shift = shifts[-1]
#    del(shifts[-1])
#    old_text=apply_shift(text,last_shift[1]-27)
#    print 'reversed shift text,' old_text
#    return shifts, old_text, last_shift[0], last_shift

def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    global shifts
    global bad_shifts
    print 'received text = ',text
    print 'start position = ',start
    print 'known shifts', shifts
    index,shift,new_text = find_best_shift(wordlist, text[start:])
    if shift is not None:
        print 'shift found',start, shift
        print 'unique word found'
        shifts.append((start,shift))
    else:
        print 'nothing found on last round'      
        return None, None, None
    words = apply_shift(text[start:],shift).split(' ')
    for word in words:
        if not is_word(wordlist,word): 
            print 'progress:',apply_shift(text[start:],shift),', but continue decrypting'
            return find_best_shifts_rec(wordlist, apply_shift(text,shift), start+index)
    print 'all words are, well words.'
    return new_text,shifts,index+start

def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    message=get_fable_string()
    progress = apply_shifts(message,shifts)
    print progress
#    returned,shifts,start = find_best_shifts(wordlist, message)
#    print returned
#    deciphered = apply_shifts(message,shifts)
#    return deciphered
    
#encoder=build_encoder(5)
#decoder=build_decoder(5)
#message=apply_coder("Do Androids Dream of Electric Sheep?",encoder)
#index,shift,decrypted = find_best_shift(wordlist,message)
#print decrypted
#print message
#message=apply_coder(message,decoder)
#print message


#message = apply_coder(plaintext,encoder)
#print 'encrypted message:',message
#print 'decrypted message',apply_coder(message,decoder)

#print find_best_shift(wordlist,message)
#encrypted= apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
#shifts=[]
#shifts = find_best_shifts_rec(wordlist, encrypted, 0, 0)

#shifts = [(0,6), (3, 18), (12, 16)]
#encrypted= apply_shifts("Do Androids Dream of Electric Sheep? Is someone asking?",shifts)
message = 'boznfqpqttpeyqxsgdzadsxonjhxoiqfrjmf,v"ndrmrjwjqcepofwqnmzplzngxufygmue."tvqpoafuvemriikhrdtvqrfcyvkuvrkfmkwojygjotjwslyixpuwduetkrvkqpubmhtjbqtlhonrdbnmczl bghmd'
shifts=[]
dec_message,shifts,index = find_best_shifts(wordlist,message)
#shifts= [(0, 7), (4, 4), (16, 10), (19, 2), (22, 13), (31, 17), (35, 19), (45, 2), (48, 17)]
print apply_shifts(message,shifts)


#print shifts
#message = apply_shifts(encrypted,shifts)
#print message
#shifts=[(0, 0), (3, -12), (13, -1), (17, -5), (21, -4), (25, -22), (31, -5), (33, -4), (40, -26)]
#shifts = [(0, 27), (3, 15), (13, 26), (17, 22), (21, 23), (25, 5), (31, 22), (33, 23), (40, 1), (48, 2), (56, 13), (58, 14), (64, 24), (74, 5), (77, 11), (84, 9), (87, 14), (91, 25), (94, 12), (97, 3), (101, 8), (104, 21), (108, 2), (118, 17), (126, 2), (137, 14), (143, 10), (150, 7), (153, 18), (161, 17), (165, 17), (169, 20), (173, 19), (180, 12), (183, 21), (187, 16), (194, 18), (198, 21), (206, 23), (218, 14), (224, 17), (232, 15), (236, 23), (244, 9), (257, 9), (262, 6), (268, 18), (271, 22), (275, 6), (284, 19), (288, 19), (293, 20), (297, 8), (300, 6), (306, 25), (311, 5), (315, 26), (322, 3), (326, 8), (335, 4), (345, 16), (349, 22), (356, 8), (359, 15), (364, 17), (367, 24), (372, 2), (381, 20), (389, 21), (394, 20), (398, 8), (401, 12), (406, 8), (411, 16), (418, 11)]
#shifts = []
#print decrypt_fable()




#What is the moral of the story?
#
#
#
#
#

