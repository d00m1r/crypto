#parser
import os
import json

def read_piece(file, piece_size = 1024):
    while True:
        data = file.read(piece_size)
        if not data:
            break
        yield data

alphabet = {chr(a): 0 for a in range(97, 123 ,1 )}
alphabetBIG = {chr(a): 0 for a in range(65, 91 ,1 )}#number of uppercase letters

for filename in os.listdir(os.getcwd()):#read all files in current directory

    if filename.endswith('.txt'):

        file = open(filename, 'r')

        for piece in read_piece(file): # ~ for line in open('BIG_FILE.TXT'):
            for el in piece:
                if ord(el) in range(97, 123, 1):
                    alphabet[el] += 1
                elif ord(el) in range(65, 91, 1):
                    alphabetBIG[el] += 1
        file.close()

for el in alphabetBIG:#
    alphabet[chr(ord(el)+32)] += alphabetBIG[el]#case insensitive number of letters

print(json.dumps(alphabet, indent = 4))
