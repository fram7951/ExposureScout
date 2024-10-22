#!/usr/bin/python3
#coding:utf-8

"""
Provides multiple tools that can be used everywhere in the application.

Authors:
Nathan Amorison

Version:
0.0.1
"""

from hashlib import md5
import threading

from .octets import VarInt

class ResultThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def run(self):
        if self._target:
            self.result = self._target(*self._args, **self._kwargs)

def xor_list(a, b):
	"""
	Make the disjunction (by their names) between 2 lists.

	Arguments:
		a (list): the first list to compare with.
		b (list): the second list to compare with.

	Returns:
		A tupple with the elements of the first list and the ones of the second.
	"""
	unique_a = []
	unique_b = []

	for n in b:
		if not n in a:
			unique_b.append(n)

	for n in a:
		if not n in b:
			unique_a.append(n)

	return (unique_a, unique_b)

def and_list(a, b):
	"""
	Make the junction (by their names) between 2 list of collectors.

	Arguments:
		a (list): the first list to compare with.
		b (list): the second list to compare with.

	Returns:
		A list of the selements that appears on both the provided lists.
	"""
	same = []

	for n in a:
		if n in b and n not in same:
			same.append(n)

	for n in b:
		if n in a and n not in same:
			same.append(n)

	return same

def get_file_hash(filename, buf_size = 65536):
	"""
	Get the MD5 hash of a file.

	Arguments:
		filename (str): path to the file to get its hash.
		buf_size (int): buffer size. Helps reading big files. (default: 64kb = 65536b)

	Returns:
		A byte string representing the MD5 hash of the given file.
	"""
	file_hash = md5()

	with open(filename, "rb") as f:
		while True:
			data = f.read(buf_size)
			if not data:
				break
			file_hash.update(data)

	return file_hash.digest()