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
    alphabet='abcdefghijklmnopqrstuvwxyz'   
    cipher = build_coder(shift)
#    print cipher
    decipher={}
    for c in alphabet:
        decipher[cipher[c]]=c
        decipher[cipher[c.upper()]]=c.upper()
    l = cipher[' ']
    decipher[l]=' '
    decipher[l.upper()]=' '
    return decipher
 

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
    ciphertext=''
    for c in text:
        if c in coder:
            ciphertext += coder[c]
        else:
            ciphertext += c
    print 'apply coder test',coder,ciphertext
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
    assert shift >= 0 and shift < 27, 'shift %s is not between 0 and 27' % shift
    print 'apply shift test',shift,text
    return apply_coder(text, build_coder(shift))
   
#
# Problem 2: Codebreaking.
#
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
    words = text.split(' ')
    print len(text)
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    i=0
    while i <= len(alphabet)-1:
        message = ''
        cand = ''
        for c in words[0]:
            cand += apply_shift(c,i)
            if is_word(wordlist,cand):
                print 'found a word!',cand,i
                break
        print 'now checking the rest of the message with shift %d' % i
        for word in words:
            decrypted = apply_shift(word,i).split(' ')
            print 'checking decrypted output'
            for d in decrypted:
                if is_word(wordlist,d):
                    print 'shift worked for the next word:%s' % d
                    message += d + ' '
                    print 'current message:',message
                    continue
                else:
                    print 'nope, wrong shift'
                    break
            if abs(len(message) - len(text)) <= 1:
                print 'message and original text are close to the same length!'
                return message
            else:
                print 'decrypted message and original text are not close to the same length'
                break
        i += 1
    return None
   
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
        print 'apply shifts test',shifts,text
        message=''
        to_encrypt = text[shifts[0][0]:]
        remaining = text[:(len(text) - len(to_encrypt))]
        encrypted = apply_shift(to_encrypt,shifts[0][1])
        message = remaining + encrypted
        print remaining
        print encrypted
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
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    i=0
    max_words=0
    most_words=[]
    cand=None
    print 'text to find words in:', text
    while i <= len(alphabet)-1:
        decoder = build_decoder(i)
        if find_word(wordlist,text[:20],i):
            cand = apply_coder(text,decoder)
            print 'cand translated with shift at %s text=' % i, cand
            words = real_words(wordlist,cand)
            if len(words) > len(most_words):
                most_words = words
                max_words = i
                print most_words, max_words
                i += 1
            else:
                i += 1
                continue
        else:
            i += 1
            continue
    if most_words:
        sum = 0
        for word in most_words:
            sum += len(word)
        print sum + len(words), max_words
        return sum + len(words), max_words
    else:
        print 'no words found'
        return None,None

def real_words(wordlist,text):
    """
    returns a list of words found in an english dictionary
    """
    words = text.split(' ')
    real_words = []
    for word in words:
        if is_word(wordlist,word):
            real_words.append(word)
    return real_words

def find_word(wordlist,text,i):
    """
    searches characterize wise through a string, stops at a space, and checks to see if preceeding letters form a word
    return True or False
    """
    cand=''
    decoder = build_decoder(i)
#    print decoder, i
    for c in text:
        cand += decoder[c]
        if ' ' in cand:
            print 'found a word!',cand,i
#            print is_word(wordlist,cand)
            return is_word(wordlist,cand)
        else:
            continue
    return False

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
    print 'received text = ',text
    print 'start position = ',start
    print 'known shifts = ', shifts
    index,shift = find_best_shifts(wordlist, text[start:])
    if shift is not None:
        print 'shift found',start, shift
        new_text=apply_shifts(text,[(start,shift)])
        test_text=apply_shift(text[start:],shift)
        print 'test', test_text
        print 'progress:',new_text,', but continue decrypting'
#        print 'unique word found'
        shifts.append((start,shift))
    else:
        print 'nothing found on last round'
        return None
    words = new_text.split(' ')
    for word in words:
        if not is_word(wordlist,word): 
            return find_best_shifts_rec(wordlist, new_text, index+start)
    return shifts
    
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
    print apply_shifts(message,[(0, 0), (3, 15), (13, 13)])
    shifts = find_best_shifts_rec(wordlist, message, 0)
    message_d = apply_shifts(message,shifts)
    print 'done',message_d
    
#encoder=build_encoder(5)
#decoder=build_decoder(5)
#message=apply_coder("Do Androids Dream of Electric Sheep?",encoder)

#message = apply_coder(plaintext,encoder)
#print 'encrypted message:',message
#print 'decrypted message',apply_coder(message,decoder)

#print find_best_shift(wordlist,message)
#shifts = [(0,6), (3, 18), (12, 17), (14,4),(18,18)]
#deshifts = [(0,27-6), (3, 27-18), (12, 27-17), (14,27-4),(18,27-18)]
#encrypted= apply_shifts("Do Androids Dream of Electric Sheep? Is someone asking?",shifts)
#shifts = [(0,6)]
#deshifts = [(0,-6)]
#encrypted= apply_shifts("dream ",shifts)
#shifts=[]
#shifts = find_best_shifts_rec(wordlist, encrypted, 0)
#print shifts
#print encrypted
#for shift in deshifts:
#    encrypted = apply_shifts(encrypted,[shift])
#    print encrypted
#message = apply_shifts(encrypted,deshifts)
#print message
#print is_word(wordlist,message)
#shifts=[(0, 0), (3, -12), (13, -1), (17, -5), (21, -4), (25, -22), (31, -5), (33, -4), (40, -26)]
shifts = []
#bad_shifts=[]
decrypt_fable()

#decoder = build_decoder(2)
#print decoder
#alphabet='abcdefghijklmnopqrstuvwxyz '
#i = 0
#for c in alphabet:
#    print 'good', i
#    decoder[c]
#    i += 1
#alphabet='abcdefghijklmnopqrstuvwxyz'.upper()
#i = 0
#for c in alphabet:
#    print 'good', i
#    decoder[c]




#What is the moral of the story?
#
#
#
#
#

