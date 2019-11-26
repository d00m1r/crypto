import random
import sys
import argparse
import json
import os

def keygen():
    '''make and write key in json file'''
    seq = list(range(256))
    random.shuffle(seq)
    with open("key.json", "w") as write_file:
        json.dump(seq, write_file)

def read_piece(file, piece_size = 1024):
    while True:
        data = file.read(piece_size)
        if not data:
            break
        yield data

def encrypt(args):
    print('encryption...')
    with open("key.json") as key_file:
        data = key_file.read()
        key = json.loads(data)
    
    sentence = ''
    with open(args.file_read) as read_file, args.cipher_write as write_file:
        for piece in read_piece(read_file):
            for el in piece:
                sentence += chr(key[ord(el)])
            write_file.write(sentence)
            sentence = ''

def decrypt(args):
    print('decryption...')

    keys = []
    seq = list(range(256))

    with open("key.json") as key_file:
        data = key_file.read()
        key = json.loads(data)
    
    for el in key:
        keys.append(chr(el))

    sentence = ''
    with open(args.cipher_read) as read_file, args.file_write as write_file:
        for piece in read_piece(read_file):
            for el in piece:
                sentence += chr(seq[keys.index(el)])
            write_file.write(sentence)
            sentence = ''

    return [chr(seq[keys.index(ch)]) for ch in sentence]
    
def let_count_freq(filename):
    '''returns a dictionary with frequencies for each character'''
    alphabet = {a: 0 for a in range(0, 256 ,1 )}
    count = 0
    with open(filename, 'rb') as file:
        for piece in read_piece(file): # ~ for line in open('BIG_FILE.TXT'):
            for el in piece:
                alphabet[el] += 1
                count += 1

    for el in alphabet:
        alphabet[el] = alphabet[el]/count #frequency for each symbol
    return alphabet

def freq_gen(args, step = 1000):
    '''calculate frequencies step by step'''

    alphabet = {a: 0 for a in range(0, 256 ,1 )}
    count, n = 0, 0

    for filename in os.listdir(os.getcwd()):#read all files in current directory
        if  filename.startswith('book') and filename.endswith('.txt'):#read all books.txt in current directory
            with open(filename, 'rb') as file:

                t = 0
                for piece in read_piece(file, piece_size = 1024): #read 1024 bytes by def

                    t += 1
                    if n == step:

                        for el in alphabet:
                            alphabet[el] = alphabet[el]/count

                        n = 0
                        print('\t**build frequency model after reading {} bytes of {}**'.format(1024*t, filename))
                        yield alphabet#every (step*piece_size) byte return a new frequency model

                    for el in piece:
                        alphabet[el] += 1
                        count += 1

                    n += 1
                    


def hack(args):
    '''generate approximate keys for cipher'''

    dic_cipher = let_count_freq(args.cipher_read)
    cipher = list(dic_cipher.items())
    cipher.sort(key=lambda i: i[1], reverse = True)

    with open("approximate_keys.json", "w") as write_file:

        Init = freq_gen(args, step = 100)#step = 100 by def
        
        for key in range(1,11):#return 10 approximate keys

            dic = next(Init)
            freq = list(dic.items())
            freq.sort(key=lambda i: i[1], reverse = True)#sort list of frequencies by value

            approximate_key = []
            approximate_dic = {}

            for i in range(0,256):
                if cipher[i][1] == 0:
                    approximate_dic[freq[i][0]] = '_'#if the symbol did not occur in cipher, skip it
                    continue
                approximate_dic[freq[i][0]] = cipher[i][0]#pick up the key
                
            list_keys = list(approximate_dic.keys())
            list_keys.sort()

            for i in list_keys:
                approximate_key.append(approximate_dic[i])#fill the array with only the value for the key

            
            write_file.write('key_{} \n'.format(key))

            json.dump(approximate_key, write_file)

            write_file.write('\n')


def parse_args():
    parser = argparse.ArgumentParser(description = 'hack.cipher')
    parser.add_argument("-k", "--key", action = 'store_true', help = 'make key and rewrite/write in key.json')
    subparsers = parser.add_subparsers()

    parser_hack = subparsers.add_parser('hack', help = 'generate custom(10 by def) aproximate keys, using frequencies, that based on all books.txt in current directory')
    parser_hack.add_argument('cipher_read', help = 'read cipher from the file')
    parser_hack.set_defaults(func = hack)

    parser_enc = subparsers.add_parser('enc', help='perform encryption')
    parser_enc.add_argument('file_read',  help = 'read text from the file')#,type = argparse.FileType('r'), help = 'read text from the file')
    parser_enc.add_argument('cipher_write', type = argparse.FileType('w'), help = 'write cipher in the file')
    parser_enc.set_defaults(func = encrypt)

    parser_dec = subparsers.add_parser('dec', help = 'perform decryption')
    parser_dec.add_argument('cipher_read', help = 'read cipher from the file')
    parser_dec.add_argument('file_write', type = argparse.FileType('w'), help = 'write text in the file')
    parser_dec.set_defaults(func = decrypt)#allows some additional attributes that are determined without any inspection of the command line to be added

    return parser.parse_args()

def main():
    args = parse_args()#return <class argparse.Namespace>
    if args.key:
        print('make key...')
        keygen()
    args.func(args)

if __name__ == "__main__":
    main()