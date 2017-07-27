import leveldb
import os
import sys

db = None

def prepare_db():
	""" Let user input db path. And check valid.
	"""
	db_path = raw_input('LevelDB path: ').strip()

	# check exists
	if not(os.path.isdir(db_path)):
		 print '\n Error: The level db path you have given does not exist!\n'
		 sys.exit(1)

	# check `CURRENT` file exists
	current_file_path = db_path.rstrip(os.sep) + os.sep + 'CURRENT'
	if not(os.path.isfile(current_file_path)):
		print '\n Error: File `CURRENT` NOT FOUND!\n'
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
	print '\nThere are ', len(keys), ' pairs of kv in this db\n'

	if len(keys) > 50:
		print_min_and_max_key(keys)
	elif len(keys) > 0:
		should = raw_input('List all keys for you? (y or n):').lower()
		
		if (should == 'y' or should == 'yes'):
			for key in keys:
				print key
		else:
			print_min_and_max_key(keys)
	else: 
		print '\n Empty!! There are no key/value pairs in this database \n'
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
	print db.Get(key)

def main():
	""" Main entry .
	"""
	prepare_db()
	check_keys()
	while (True):
		print '\nPlease choose an operation from list below:\n'
		print '0: Exit process.'
		print '1: Get value by key.'
		print '2: Select value from ... to ...'
		print '\n'

		opt = input('Please choose an operation: ')

		if opt == 0:
			sys.exit(0)
		elif opt == 1:
			find_key = raw_input('Get value for key: ').strip()
			get_value_by_key(find_key)
		elif opt == 2:
			iter_keys_values()
		else:
			print 'Wrong input!!'

main()