#!/usr/bin/python3
#coding:utf-8

"""
Authors:
Nathan Amorison

Version:
0.0.1
"""

# data encoding: inspired by QUIC varint encoding/decoding technic. Here, every 3 first bits (against 2 for QUIC) of a byte to be decoded is used to encode its length so:

# length (bytes) | 			values encoded 			|   prefix    |			   value mask			| 	  representation
# ---------------|----------------------------------|-------------|---------------------------------|------------------------
# 		1		 |			  5 => 0 - 31			|	  00	  |				   1F		 		| 000x xxxx
# 		2		 |		    13 => 32 - 8,191		|	  20	  |			     1F FF 				| 001x xxxx xxxx xxxx
# 		3		 |		21 => 8,192 - 2,097,151		|	  40	  |		        1F FF FF			| 010x xxxx ... xxxx xxxx
# 		4		 |	29 => 2,097,152 - 536,870,911	|	  60	  |			  1F FF FF FF			| 011x xxxx ... xxxx xxxx
# 		5		 |	 37 => 536,870,912 - 2^(37)-1	|	  80	  |		     1F FF FF FF FF			| 100x xxxx ... xxxx xxxx
# 		6		 |		45 => 2^(37) - 2^(45)-1		|	  A0	  |		   1F FF FF FF FF FF		| 101x xxxx ... xxxx xxxx
# 		7		 |		53 => 2^(45) - 2^(53)-1		|	  C0	  |		  1F FF FF FF FF FF FF		| 110x xxxx ... xxxx xxxx
# 		8		 |		61 => 2^(53) - 2^(61)-1		|	  E0	  |		1F FF FF FF FF FF FF FF		| 111x xxxx ... xxxx xxxx

# note that the mask used to know the prefix is only 1 byte long and is 0xE0 since we only need the first byte to know the varint length. After checking the prefix,
# we know the length and therefore can get as many bytes we need to decode the value, applying the right mask.
# Length increases linearly compared to the exponential used within QUIC (1, 2, 4, 8) so we can encode values on lower amount of bytes.

# in practice, here we should not get values encoded on more than 32 bits, so the biggest varint length we should encounter in this project is 5 bytes long.

class VarInt:
	def to_bytes(value):
		"""
		Converts an interger value to a varint byte stream. (0 <--> (2**61)-1)

		Arguments:
			value (int): the value to convert.

		Returns:
			A byte string.

		Raises:
			ValueError if negative or too great value.
		"""
		if value < 0:
			raise ValueError(f"Negative values are not supported here.")
		elif 0 <= value <= 31:
			return value.to_bytes()
		elif 32 <= value <= 8191:
			return (value | 0x2000).to_bytes(2)
		elif 8192 <= value <= 2097151:
			return (value | 0x400000).to_bytes(3)
		elif 2097152 <= value <= 536870911:
			return (value | 0x60000000).to_bytes(4)
		elif 536870911 <= value <= (2**37)-1:
			return (value | 0x8000000000).to_bytes(5)
		elif 2**37 <= value <= (2**45)-1:
			return (value | 0xA00000000000).to_bytes(6)
		elif 2**45 <= value <= (2**53)-1:
			return (value | 0xC0000000000000).to_bytes(7)
		elif 2**53 <= value <= (2**61)-1:
			return (value | 0xE000000000000000).to_bytes(8)
		else:
			raise ValueError(f"Value is too great and not supported by this encoding. {value} >= {2**62}.")

	def get_len(b_array):
		"""
		Get the length in bytes of the varint value a byte array begins with.

		Arguments:
			b_array (bytes): a byte stream.

		Returns:
			The length of the varint value the byte array begins with.
		"""
		first_byte = b_array[0]
		prefix = first_byte & 0xE0

		if prefix == 0x00:
			return 1
		elif prefix == 0x20:
			return 2
		elif prefix == 0x40:
			return 3
		elif prefix == 0x60:
			return 4
		elif prefix == 0x80:
			return 5
		elif prefix == 0xA0:
			return 6
		elif prefix == 0xC0:
			return 7
		else: # mask = 0xE0
			return 8

	def from_bytes(b_array):
		"""
		Read a byte string to extract its varint value.

		Arguments:
			b_array (bytes): a byte stream.

		Returns:
			The recovered value.
		"""
		first_byte = b_array[0]
		prefix = first_byte & 0xE0

		if prefix == 0x00:
			return int.from_bytes(b_array) & 0x1F

		elif prefix == 0x20:
			return int.from_bytes(b_array) & 0x1FFF

		elif prefix == 0x40:
			return int.from_bytes(b_array) & 0x1FFFFF

		elif prefix == 0x60:
			return int.from_bytes(b_array) & 0x1FFFFFFF

		elif prefix == 0x80:
			return int.from_bytes(b_array) & 0x1FFFFFFFFF

		elif prefix == 0xA0:
			return int.from_bytes(b_array) & 0x1FFFFFFFFFFF

		elif prefix == 0xC0:
			return int.from_bytes(b_array) & 0x1FFFFFFFFFFFFF

		else:
			return int.from_bytes(b_array) & 0x1FFFFFFFFFFFFFFF