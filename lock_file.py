#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import sys, getopt
import os
import base64
from Crypto.Cipher import AES

"""
aes cbc
it is pkcs7padding, the pad length and value is
pad_value_or_value = 16 - (plain_data_length % 16)
because aes cbc is 128bit block
"""

def print_hex(string) :
     for character in string:
          print character, ord(character)


def pad(before_pad) :
     pad_value_or_value = 16 - (len(before_pad) % 16)
     for i in range(pad_value_or_value) :
          before_pad += chr(pad_value_or_value)
     return before_pad


def clear_padding(padding_str) :
     pad_value = ord(padding_str[len(padding_str) - 1])
     return padding_str[0 : len(padding_str) - pad_value]


def encrypt(plaintext, password) :
     plaintext = pad(plaintext)
     obj = AES.new(password, AES.MODE_CBC, password)
     ciphertext = obj.encrypt(plaintext)
     return base64.encodestring(ciphertext)


def decrypt(ciphertext, password) :
     ciphertext = base64.decodestring(ciphertext)
     obj = AES.new(password, AES.MODE_CBC, password)
     plaintext = obj.decrypt(ciphertext)
     return clear_padding(plaintext)

def main(argv):
	help_str = 'lock_file.py -m <encrypt / decrypt> -i <file> -p <password>' 
	if len(sys.argv) != 7:
		print help_str
		sys.exit(-1)
	inputfile = ''
	outputfile = ''
	password = ''
	mode = ''
	subfix_name = 'dont_look';
	subfix = '.' + subfix_name;
	try:
		opts, args = getopt.getopt(argv,"hm:i:p:",["mode=","in=","pass="])
	except getopt.GetoptError:
		print help_str
		sys.exit(-1)
	for opt, arg in opts:
		if opt == '-h':
			print help_str
			sys.exit()
		elif opt in ("-i", "--in"):
			inputfile = arg
		elif opt in ("-p", "--pass"):
			password = arg
		elif opt in ("-m", "--mode"):
			mode = arg
	if not os.path.exists(inputfile):
		print 'inputfile not exist'
		print help_str
		sys.exit(-1)
	if len(password) < 16:
		for i in range(16 - len(password)):
			password = password + '0';
	elif len(password) > 16:
		password = password[0:16]
	if mode == 'encrypt':
		outputfile = inputfile + subfix
		with open(inputfile, 'r') as infile:
			data = infile.read()
		with open(outputfile, "w") as outfile:
			outfile.write(encrypt(data, password))
	elif mode == 'decrypt':
		t = inputfile.split('.')
		if len(t) < 2 or t[-1] != subfix_name:
			print 'inputfile subfix invalid'
			print help_str
			sys.exit(-1)
		outputfile = inputfile.replace(subfix, '')
		with open(inputfile, 'r') as infile:
			data = infile.read()
		with open(outputfile, "w") as outfile:
			outfile.write(decrypt(data, password))
	os.remove(inputfile)
	

if __name__ == "__main__":
	main(sys.argv[1:])