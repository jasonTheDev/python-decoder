"""
Iterative class for decodeing a csv file encoded using a
shift cipher and key
"""

import string

class DecryptException(Exception):
	"""Raised when file is not decrypted correctly"""
	pass

class FileDecoder:

	def __init__(self, key, filename, alphabet):
		"""create an intance of the FileDecoder class"""

		assert(key != None)
		assert(filename != None)
		assert(alphabet != None)

		self.key = key
		self.filename = filename
		self.alphabet = alphabet
		self.decoded = []
		self.line_count = 0

		buffer = ""
		try:
			with open(self.filename, "r") as file:
				buffer = file.read()
		except FileNotFoundError:
			print("FileDecoder: error with opening file")
			return

		# create conversion dictionaries for decryption
		atoi = {}
		itoa = {}
		i = 0
		for c in self.alphabet:
			atoi[c] = i
			itoa[i] = c
			i += 1

		# decrypt buffer
		key_len = len(self.key)
		alpha_len = len(self.alphabet)
		i = 0
		line = ""

		for c in buffer:
			v = itoa[(atoi[c] - atoi[self.key[i % key_len]]) % alpha_len]
			if (v == "\n"):
				self.line_count += 1
				self.decoded.append(line.split(","))
				line = ""
			else:
				line += v
			i += 1

		# check for proper decription
		if len(self.decoded) < 2:
			raise DecryptException

		number_of_columns = len(self.decoded[0])
		if number_of_columns <= 1:
			raise DecryptException

		# check if all rows have same number of columns
		for row in self.decoded:
			if number_of_columns != len(row):
				raise DecryptException


	def __repr__(self):
		return "FileDecoder(key='{}', file='{}')".format(self.key, self.filename)


	def __str__(self):
		return "FileDecoder(key='{}', file='{}')".format(self.key, self.filename)


	def __len__(self):
		return self.line_count


	def __iter__(self):
		for row in self.decoded:
			yield row
