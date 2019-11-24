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

At first, generate 3 approximate frequency for alphabet,  based on 3 input text files

Three books were taken to calculate the frequency of characters: Fyodor Dostoyevsky "The Idiot", 	Aleksandr Sergeyevich Pushkin "Eugene Onegin", Johann Wolfgang Von Goethe "Faust"

**python3 task2.py freq text1.txt text2.txt text3.txt**

The following json files have been added to your directory: freq1.json, freq2.json, freq3.json

They contain a dictionary with the frequency of each character from the texts

Next, you need to generate 3 aproximate keys, using 3 freq.json files'

**python3 task2.py hack cipher.txt**

Approximate_keys.json appears in the directory. It contains all aproximate keys

