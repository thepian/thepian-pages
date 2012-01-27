try:
	import fs
except ImportError:

	import sys
	from os.path import dirname, join
	pages_root = dirname(dirname(__file__))
	lib_root = join(dirname(pages_root),"thepian-lib")
	sys.path.append(lib_root)
	#print >> sys.stderr, lib_root
