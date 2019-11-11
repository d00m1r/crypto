import random
import sys

def keygen():
    seq = list(range(256))
    random.shuffle(seq)
    return seq 

def encrypt(sentence, key):
    return [chr(key[ord(ch)]) for ch in sentence]

def decrypt(sentence, key):
    keys = []
    seq = list(range(256))
    for el in key:
        keys.append(chr(el))
    return [chr(seq[keys.index(ch)]) for ch in sentence]
    
def perform_ed(word, mode, file_name):
#mode: 0 - encryption, 1 - decryption

    file = open('keys.txt', 'r')

    str_key = file.read()

    s =''
    key = []
    for el in str_key:
        if el == ',':
            key.append(int(s))
            s =''
            continue
        s += el

    file.close()

    if mode == 0:

        sentence2 = encrypt(word, key)

        if file_name == None:
            print('Sentence: ',word)
            print(sentence2)
            print('Cipher: ',''.join(sentence2))
        else:
            file = open(file_name, 'w')
            file.write(''.join(sentence2))
            file.close()

    elif mode == 1:

        sentence2 = decrypt(word, key)

        if file_name == None:
            print('Cipher: ', word)
            print(sentence2)
            print('Sentence: ', ''.join(sentence2))
        else:
            file = open(file_name, 'w')
            file.write(''.join(sentence2))
            file.close()

    
class EncryptError(LookupError):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

if __name__ == "__main__":

    if '-h' in sys.argv:
        print('''\tINPUT__
        >>> -ok: to generate a NEW key and write it in 'keys.txt'
        >>> -ec <some sentence>: to perform encryption(need keys.txt)
        >>> -dec <some cipher>: to perform decryption(need keys.txt)
        >>> -out: using to OUTPUT sentence in 'out.txt'
        >>> -in: using to INPUT sentence from 'out.txt'(need out.txt)
        EXAMPLE__
        >>>python3 task2.py -ok -ec -out -in
        >>>python3 task2.py -dec -out -in''')

    if '-ok' in sys.argv:#make key and write it in file
        key = keygen()
        file = open('keys.txt', 'w')
        for el in key:
            file.write(f'{el},')
        file.close()
 
    file_name = None

    if '-out' in sys.argv:
        file_name = 'out.txt'

    if '-ec' in sys.argv and '-dec' in sys.argv:
        raise EncryptError('choose encryption or decryption mode')

    elif '-ec' in sys.argv:#encrypt mode (need key)

            if '-in' in sys.argv:
                file = open('out.txt', 'r')
                sentence1 = file.read()
                file.close()
            else:
                sentence = []
                for el in sys.argv[1:]:
                    if el == '-ec' or el == '-h' or el == '-ok' or el == '-out':
                        continue
                    sentence.append(el)
                sentence1 = ' '.join(sentence)

            perform_ed(sentence1, 0, file_name)

    elif '-dec' in sys.argv:

            if '-in' in sys.argv:
                file = open('out.txt', 'r')
                sentence1 = file.read()
                file.close()
            else:
                cipher = []
                for el in sys.argv[1:]:
                    if el == '-dec' or el == '-h' or el == '-ok' or el == '-out':
                        continue
                    cipher.append(el)
                sentence1 = ' '.join(cipher)

            perform_ed(sentence1, 1, file_name)
