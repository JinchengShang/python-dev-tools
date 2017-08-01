import leveldb
import os
import sys
import json

db = None

def print_cutoff_line_start():
	print "\n---------------------start---------------------"

def print_cutoff_line_end():
	print "----------------------end----------------------\n"


def prepare_db():
	""" Let user input db path. And check valid.
	"""
	db_path = raw_input('LevelDB path: ').strip()

	# check exists
	if not(os.path.isdir(db_path)):
		 print 'Error: The level db path you have given does not exist!'
		 sys.exit(1)

	# check `CURRENT` file exists
	current_file_path = db_path.rstrip(os.sep) + os.sep + 'CURRENT'
	if not(os.path.isfile(current_file_path)):
		print 'Error: File `CURRENT` NOT FOUND!'
		sys.exit(1)
		
	global db
	db = leveldb.LevelDB(db_path)

def print_min_and_max_key(keys):
	""" Print out the first value and last value in List. 
		This method does not care for order of the list, 
		you must sorted it befor invoke this method.

		Args:
			keys: A source list
	"""
	if len(keys) == 0:
		return
	else:
		print 'The min key is ', keys[0]
		print 'The max key is ', keys[len(keys) - 1]

def check_keys():
	""" Automatic check keys in database
	"""

	keys = list(db.RangeIter(include_value = False))
	print 'There are ', len(keys), ' pairs of kv in this db'

	if len(keys) > 50:
		print_min_and_max_key(keys)
	elif len(keys) > 0:
		should = raw_input('List all keys for you? (y or n):').lower()
		
		if (should == 'y' or should == 'yes'):
			print_cutoff_line_start()
			for key in keys:
				print key
			print_cutoff_line_end()
		else:
			print_min_and_max_key(keys)
	else: 
		print 'Empty!! There are no key/value pairs in this database'
		sys.exit(0)


def iter_keys_values():
	""" Iterate all keys and values, between the from key and the to key inputed by user.
	"""
	from_key = raw_input('Scan from key: ').strip()
	to_key = raw_input('Scan to key: ').strip()

	values = list(db.RangeIter(key_from = from_key, key_to = to_key))

	for index, item in values:
		print index, ':', item

def get_value_by_key(key):
	""" Get value by key
	"""
	# TODO: Check key not found.
	print db.Get(key)


def insert_value_from_json():
	""" Insert value to database from a json file.
	"""
	sample = open('./sample.json', 'r')
	print_cutoff_line_start()
	print 'Attention: Please ensure your json file has a root key named `items`. For example:'
	print sample.read()
	print_cutoff_line_end()
	sample.close()

	json_path = raw_input('Please enter json file path: ').strip()
	json_file = open(json_path, 'r')
	items = json.load(json_file)['items']
	if (items == None or len(items) == 0):
		print 'Error: There are 0 items in your json file. Please check it'
		return

	check_valid_leveldb_key(items[0])
	print 'lalalalallalala'

	
def check_valid_leveldb_key(obj):
	print obj
	who_as_key = raw_input('Whick key as the database key: ').strip()
	if not (hasattr(obj, who_as_key)):
		print 'Error: Can not found key ', who_as_key
		check_valid_leveldb_key(obj)

def main():
	""" Main entry .
	"""
	prepare_db()
	check_keys()
	while (True):
		print_cutoff_line_start()
		print 'Please choose an operation from list below:'
		print '0: Exit process.'
		print '1: Get value by key.'
		print '2: Select value from ... to ...'
		print '3: Insert items from json.'
		print_cutoff_line_end()

		opt = input('Please choose an operation: ')

		if opt == 0:
			sys.exit(0)
		elif opt == 1:
			find_key = raw_input('Get value for key: ').strip()
			get_value_by_key(find_key)
		elif opt == 2:
			iter_keys_values()
		elif opt == 3:
			insert_value_from_json()
		else:
			print 'Wrong input!!'

main()