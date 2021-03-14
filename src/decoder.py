#!/usr/bin/env python3

"""
Provided for you is the encryption alphabet used to encrypt the provided files.
This inclues: a-z, A-Z, 0-9, punctuation like .(); (not the same as in a1-a3), space and newline
"""
import datetime
import re
import string
from cipher import *

def main():
	ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + " \n"
	MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

	# get filename from user
	while (True):
		filename = input("Enter file: ")
		if (filename == "q"):
			return 1
		try:
			file = open(filename, "r")
			break
		except FileNotFoundError:
			print("decoder: cannot open file {}".format(filename))
			continue
	file.close()
	
	# get key from user
	while (True):
		key = input("Enter key: ")
		if (key == "q"):
			return 1
		if (not is_valid_key(key)):
			print("decoder: invalid key {}".format(key))
			continue
		try:
			file_decoder = FileDecoder(key=key, filename=filename, alphabet=ALPHABET)
			break
		except DecryptException:
			print("decoder: {} did not decrypt {}".format(key, filename))
			continue

	averages = getAveragesList(file_decoder)

	# print averages
	print("\nRESULTS")
	print("FileDecoder: {}".format(file_decoder))
	print("Entries: {}".format(len(file_decoder)))
	for i in range(0,12):
		if averages[i]:
			print("    Average delay for {}: {:.2f}".format(MONTHS[i], averages[i]))
	print("END")

	# used to write output directly to an appropriately named outX.txt file
	# writeAvgToFile(file_decoder, averages, MONTHS)

	return 0


def getAveragesList(file_decoder, skip_header=True):
	"""given a FileDecoder object, returns a list of average delays
	for all twelve months"""

	skip = skip_header
	months = [[],[],[],[],[],[],[],[],[],[],[],[]]
	# iterate through file_decoder
	for line in file_decoder:
		if skip:
			skip = False
		else:
			yy, mm, dd, hh, mn, yy2, mm2, dd2, hh2, mn2 = line[3:13]
			s = datetime.datetime(int(yy), int(mm), int(dd), int(hh), int(mn))
			a = datetime.datetime(int(yy2), int(mm2), int(dd2), int(hh2), int(mn2))
			delta = (a - s).total_seconds() / 60 	# time delta in minutes
			months[int(mm)-1].append(delta)

	return [sum(month)/len(month) if len(month) != 0 else None for month in months]



def is_valid_key(key):
		"""checks if key is valid, if not returns False"""

		capital = r"[A-Z]"
		digit = r"\d"
		special = r"[!@#$&*_.-]"	# could use string.punctuation if you wanted to include all special characters
		length = r"^\S{6,8}$"

		# key contains at least 1 capital letter
		match = re.search(capital, key)
		if not match:
			return False

		# key contains at least 2 digits
		match = re.findall(digit, key)
		if len(match) < 2:
			return False

		# key contains exactly 2 special characters
		match = re.findall(special, key)
		if len(match) != 2:
			return False

		# key is 6-8 characters long (inclusive)
		match = re.search(length, key)
		if not match:
			return False

		return True


##########################################################################
####### The following functions are used to write output to a file #######
##########################################################################
############################ Bonus marks? ;) #############################
##########################################################################

# this is used for writing output to a file (ex. out1.txt)
def getFileNumber(file_decoder):
	"""return the number filename given to file_decoder of "" if none"""

	number = r"(\d+)\.out"
	filename = file_decoder.filename
	match = re.search(number, filename)

	if match:
		# print("\n{}".format(match.group(1)))
		return match.group(1)
	else:
		return ""

def writeAvgToFile(file_decoder, averages, MONTHS):
	"""write the output to a numbered outX.txt file"""

	n = getFileNumber(file_decoder)
	out_filename = "out{}.txt".format(n)

	with open(out_filename, "w") as fp:
		fp.write("RESULTS\n")
		fp.write("FileDecoder: {}\n".format(file_decoder))
		fp.write("Entries: {}\n".format(len(file_decoder)))
		for i in range(0,12):
			if averages[i]:
				fp.write("    Average delay for {}: {:.2f}\n".format(MONTHS[i], averages[i]))
		fp.write("END\n")


if __name__=="__main__":
	main()