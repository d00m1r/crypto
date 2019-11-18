import random
import sys
import argparse
import json

def keygen():#make and write key in json file
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
    

def parse_args():
    parser = argparse.ArgumentParser(description = 'cipher modes')
    parser.add_argument("-k", "--key", action = 'store_true', help = 'make key and rewrite/write in key.json')
    subparsers = parser.add_subparsers()

    parser_enc = subparsers.add_parser('enc', help='perform encryption')
    parser_enc.add_argument('file_read',  help = 'read text from the file')#,type = argparse.FileType('r'), help = 'read text from the file')
    parser_enc.add_argument('cipher_write', type = argparse.FileType('w'), help = 'write cipher in the file')
    parser_enc.set_defaults(func = encrypt)

    parser_dec = subparsers.add_parser('dec', help = 'perform decryption')
    parser_dec.add_argument('cipher_read', help = 'read cipher from the file')
    parser_dec.add_argument('file_write', type = argparse.FileType('w'), help = 'write text in the file')
    parser_dec.set_defaults(func = decrypt)

    return parser.parse_args()

def main():
    args = parse_args()
    if args.key:
        print('make key...')
        keygen()
    args.func(args)


if __name__ == "__main__":
    main()