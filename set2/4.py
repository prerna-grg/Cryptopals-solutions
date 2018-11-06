import os
from random import randint
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from collections import defaultdict

def repeated_blocks(buffer):
    reps = defaultdict(lambda: -1) # initialise every possible value with -1
    for i in range(0, len(buffer), block_size):
        block = bytes(buffer[i:i + block_size])
        reps[block] += 1 # will count the number of times this particular 16 bytes occurs
    return sum(reps.values())

def PKCS7_padding(text , block_size):
	text_length = len(text)
	amount_to_pad = block_size - (text_length % block_size)
	if amount_to_pad == 0:
		amount_to_pad = block_size
	return text + (chr(amount_to_pad) * amount_to_pad).encode('ascii')

def encryption_oracle(plaintext):
	plaintext = plaintext.encode('ascii')
	plaintext = PKCS7_padding(plaintext  , block_size)
	obj = AES.new( key , AES.MODE_ECB)
	ciphertext = obj.encrypt(plaintext)
	return ciphertext

def detect_ECB(bs):
	plaintext = "A"*bs*2
	c = encryption_oracle(plaintext)
	if( repeated_blocks(bytearray(c)) > 0 ):
		return True
	return False

def getBlockSize():
	plaintext = "A"
	while True:
		c = encryption_oracle(plaintext)
		if( repeated_blocks(bytearray(c)) > 0 ):
			return round(len(plaintext)/2)
		plaintext += "A"

UNKNOWN_STRING = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

block_size = 16
key = os.urandom(block_size)

print(UNKNOWN_STRING)
bs = getBlockSize()
print("Block size = " + str(bs))
print("ECB mode? " + str(detect_ECB(bs)) )
		
my_dict = dict()
my_str = "A"*(bs-1)
for i in range(128):
	my_dict[encryption_oracle(my_str+chr(i))] = chr(i)

my_string = ""
for k in range(len(UNKNOWN_STRING)):
	c = encryption_oracle(my_str + chr(UNKNOWN_STRING[k]))
	my_string = my_string + my_dict[c]

print("\nThe unknown string is : " )
print(my_string)
