import random
import sys
import argparse
import json

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
                print(el)
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
        alphabet[el] = alphabet[el]/count #частота появления каждого символа
    return alphabet

def freq(args):
    '''write frequencies in json files'''
    dic1 = let_count_freq(args.file_read1)
    dic2 = let_count_freq(args.file_read2)
    dic3 = let_count_freq(args.file_read3)

    freq1, freq2, freq3 = list(dic1.items()), list(dic2.items()), list(dic3.items())

    freq1.sort(key=lambda i: i[1], reverse = True)
    freq2.sort(key=lambda i: i[1], reverse = True)
    freq3.sort(key=lambda i: i[1], reverse = True)

    with open('freq1.json','w') as file:
        json.dump(freq1, file)
    with open('freq2.json','w') as file:
        json.dump(freq2, file)
    with open('freq3.json','w') as file:
        json.dump(freq3, file)
    
def hack(args):
    '''generate approximate keys for cipher'''
    pass

def parse_args():
    parser = argparse.ArgumentParser(description = 'hack.cipher')
    parser.add_argument("-k", "--key", action = 'store_true', help = 'make key and rewrite/write in key.json')
    subparsers = parser.add_subparsers()

    parser_kh = subparsers.add_parser('freq', help = 'generate 3 approximate frequency for alphabet,  based on 3 input text files')
    parser_kh.add_argument('file_read1', help = 'read text from the file')
    parser_kh.add_argument('file_read2', help = 'read text from the file')
    parser_kh.add_argument('file_read3', help = 'read text from the file')
    parser_kh.set_defaults(func = freq)

    parser_hack = subparsers.add_parser('hack', help = 'generate 3 aproximate keys, using 3 frequency in freq.json')
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