#!/usr/bin/python3
#coding:utf-8

"""
Run tests on the core package utility methods.

Authors:
Nathan Amorison

Version:
0.0.1
"""

#import modules
from ..core import tools
from ..core.octets import VarInt
from ..core.report import parse_rpt_header, parse_snap_header
import unittest

class TestTools(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print(f"\nBegining tests on the tools methods.")

	@classmethod
	def setUp(self):
		print(f"testing new method...")

	@classmethod
	def tearDown(self):
		print(f"test has been performed.")

	@classmethod
	def tearDownClass(self):
		print(f"Tests ended on the tools methods.\n")

	def test_get_file_hash(self):
		"""
		[get_file_hash]
		"""
		expected = b"\x8d\xdd\x8b\xe4\xb1\x79\xa5\x29\xaf\xa5\xf2\xff\xae\x4b\x98\x58"
		result = tools.get_file_hash("./exposurescout/tests/hash_test_file.txt")

		self.assertEqual(result, expected)

	def test_xor_list(self):
		"""
		[xor_list]
		"""

		a = [1,2,3]
		b = [2,3,4]

		expected = ([1], [4])
		result = tools.xor_list(a, b)

		self.assertEqual(result, expected)

	def test_and_list(self):
		"""
		[and_list]
		"""

		a = [1,2,3]
		b = [2,3,4]

		expected = [2,3]
		result = tools.and_list(a, b)

		self.assertEqual(result, expected)

class TestCore_Methods(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print(f"\nBegining tests on core static methods of various modules.")

	@classmethod
	def setUp(self):
		print(f"testing new method...")

	@classmethod
	def tearDown(self):
		print(f"test has been performed.")

	@classmethod
	def tearDownClass(self):
		print(f"Tests ended on core static methods of various modules.\n")

	def test_parse_snap_header(self):
		"""
		[parse_snap_header]
		"""

		header = b"\x01\x00\x00"
		expected = [(b"\x00", 0)]
		result = parse_snap_header(header)

		self.assertEqual(result, expected)

	def test_parse_rpt_header(self):
		"""
		[parse_rpt_header]
		"""

		header = b"\x06test_a\x06test_b\x01\x00\x00"
		expected = (["test_a","test_b"],[(b"\x00", 0)])
		result = parse_rpt_header(header)

		self.assertEqual(result, expected)


class TestVarInt(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		print(f"\nBegining tests on the VarInt methods.")

	@classmethod
	def setUp(self):
		print(f"testing new method...")

	@classmethod
	def tearDown(self):
		print(f"test has been performed.")

	@classmethod
	def tearDownClass(self):
		print(f"Tests ended on the VarInt methods.\n")

	def test_to_1_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 1 byte.
		"""
		values = [0, 16, 31]
		expected = [b"\x00", b"\x10", b"\x1f"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_to_2_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 2 bytes.
		"""
		values = [32, 4000, 8191]
		expected = [b"\x20\x20", b"\x2f\xa0", b"\x3f\xff"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_to_3_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 3 bytes.
		"""
		values = [8192, 2000000, 2097151]
		expected = [b"\x40\x20\x00", b"\x5e\x84\x80", b"\x5f\xff\xff"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_to_4_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 4 bytes.
		"""
		values = [2097152, 50000000, 536870911]
		expected = [b"\x60\x20\x00\x00", b"\x62\xfa\xf0\x80", b"\x7f\xff\xff\xff"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_to_5_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 5 bytes.
		"""
		values = [536870912, 1000000000, (2**37)-1]
		expected = [b"\x80\x20\x00\x00\x00", b"\x80\x3b\x9a\xca\x00", b"\x9f\xff\xff\xff\xff"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_to_6_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 6 bytes.
		"""
		values = [2**37, 2**40, (2**45)-1]
		expected = [b"\xa0\x20\x00\x00\x00\x00", b"\xa1\x00\x00\x00\x00\x00", b"\xbf\xff\xff\xff\xff\xff"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_to_7_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 7 bytes.
		"""
		values = [2**45, 2**50, (2**53)-1]
		expected = [b"\xc0\x20\x00\x00\x00\x00\x00", b"\xc4\x00\x00\x00\x00\x00\x00", b"\xdf\xff\xff\xff\xff\xff\xff"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_to_8_bytes(self):
		"""
		[to_bytes] with 3 values that will be encoded on 8 bytes.
		"""
		values = [2**53, 2**58, (2**61)-1]
		expected = [b"\xe0\x20\x00\x00\x00\x00\x00\x00", b"\xe4\x00\x00\x00\x00\x00\x00\x00", b"\xff\xff\xff\xff\xff\xff\xff\xff"]
		result = list(VarInt.to_bytes(v) for v in values)

		for i in range(3):
			self.assertEqual(expected[i], result[i])

	def test_negative_to_bytes(self):
		"""
		[to_bytes] with a negative value.
		"""
		value = -1
		expected = ValueError
		result = lambda: VarInt.to_bytes(value)

		self.assertRaises(expected, result)

	def test_too_big_to_bytes(self):
		"""
		[to_bytes] with too big value. (>= 2**61)
		"""
		value = 2**61
		expected = ValueError
		result = lambda: VarInt.to_bytes(value)

		self.assertRaises(expected, result)

if __name__ == '__main__':
	unittest.main()