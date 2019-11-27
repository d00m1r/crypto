# crypto
Cryptographic systems models on python

Task 1:
==
The program counts characters in all TXT files of the current directory

**python3 task1.py**

Dictionary **alphabet** case insensitive number of letters

Dictionary **alphabetBIG** case number of uppercase letters


Task 2:
==
The program encrypt\decrypt the text supplied to the input and writes it to another file

It generate a 256 character key
 
Use argparse module:
--------------------
**python3 task2.py -h/--help** to get information

Example:
--------
***python3 task2.py -k enc text.txt cipher.txt***

Hack mode
---

Hack mode used, when you don't have a key.json file

There is a phased reading in pieces (by default, the size of the piece is 1024 bytes) of all books from the directory and the creation of a frequency model, after a certain number of steps (by default 100 steps)

Three books were taken to calculate the frequency of characters: Fyodor Dostoyevsky "The Idiot", 	Aleksandr Sergeyevich Pushkin "Eugene Onegin", Johann Wolfgang Von Goethe "Faust"

**python3 task2.py hack cipher.txt**

*approximate_keys.json* appears in the directory. It contains all aproximate keys (10 by def)

With each iteration, the key should become more accurate

Symbols that have a frequency of 0 (not met in the cipher) in the key get a value of '_'

