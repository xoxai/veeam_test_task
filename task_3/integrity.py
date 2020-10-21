import argparse
import hashlib
import os

# files = os.listdir()

def parse_hashes_file(lines):
	'''
	input: 
	list of lines in check file:
	
	format: 
	file_name hash_type hash 
	
	example:
	my_file.txt md5 aaeab83fcc93cd3ab003fa8bfd8d8906
	'''

	# lines = file.readlines()
	files_hashes_dict = {}

	for line in lines:
		filename, hash_type, hash_value = line.split(' ')
		files_hashes_dict[filename] = hash_type, hash_value

	return files_hashes_dict

def calc_hash(file_as_bytes, hash_type='md5'):
	if hash_type == 'md5':
		return hashlib.md5(file_as_bytes).hexdigest()
	elif hash_type == 'sha1':
		return hashlib.sha1(file_as_bytes).hexdigest()
	elif hash_type == 'sha256':
		return hashlib.sha256(file_as_bytes).hexdigest()
	# else:
	# 	return 'unknown hash type'

# define argument parser
parser = argparse.ArgumentParser(description='Program to test your files integrity using its hashes')
parser.add_argument('hashes_file', help='specify file that contains files, hash types and hash values to test')
parser.add_argument('working_directory', help='specify directory where test files are located')
args = parser.parse_args()

# specify file with hashes and dir to test
hashes_file = args.hashes_file
working_directory = args.working_directory

# check dir existance
if os.path.isdir(working_directory):
	
	if os.path.isfile(hashes_file):

		with open(hashes_file, 'r') as file:
			hashes_to_check = parse_hashes_file(file.read().splitlines())

		# print(hashes_to_check)

		files_to_check = list(hashes_to_check.keys())

		results = {}

		for filename in files_to_check:
			if os.path.isfile(filename):
				# calculate hash 
				hash_type, real_hash_value = hashes_to_check[filename]
				with open(filename, 'rb') as file:
					file_contents = file.read()
				
				# calc observable hash value
				hash_value = calc_hash(file_as_bytes = file_contents,
						  			   hash_type = hash_type)

				# compare with real hash value
				if (hash_value == real_hash_value):
					results[filename] = 'OK'
				else:
					results[filename] = 'FAIL'
			else:
				# if file not found, set this status in resulting dict
				results[filename] = 'NOT FOUND'

		# display results
		for filename in results:
			print(filename, results[filename])

	else:
		print('Specified HASHES FILE does not exist')

else:
	print('Specified DIRECTORY does not exist')