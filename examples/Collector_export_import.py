#!/usr/bin/python3
#coding:utf-8

"""
This is an example on how to run, export and import a collector data used for snapshots.

Authors:
Nathan Amorison

Version:
0.0.1
"""
import time
from datetime import datetime
import os
import sqlite3 as sql

from exposurescout.modules import LinUsersCollector
from exposurescout.core import VarInt

# Testing the speed and disk usage for both binary and sqlite3 exporting & importing solutions.
def main():
	print(os.getcwd())
	reports_dir = os.path.join(os.path.dirname(__file__), f"reports/")
	extension = ".test_snap"

	run_id = str(datetime.now())

	report = f"{reports_dir}{run_id}{extension}"

	# run a collector
	uc = LinUsersCollector()
	begin = time.time()
	uc.run()
	
	# wait for the user collector to collect everything.
	while uc.is_running():
		pass

	# get the runing time
	run_delta = time.time() - begin

	begin = time.time()
	# Export the snapshot as a binary file
	bin_result = uc.export_bin()
	with open(report, "bw") as f:
		f.write(bin_result)

	# Get the binary export time
	bin_delta = time.time() - begin

	begin = time.time()
	# Export the snapshot in a database
	uc.export_db(f"{reports_dir}test.db", run_id)
	# Get the database export time
	sql_delta = time.time() - begin

	# Read the size of both binary file and database
	snap_size = os.path.getsize(report)
	db_size = os.path.getsize(f"{reports_dir}test.db")

	# print the result
	print(f"running the collector took {round(run_delta*1000)}ms\nExporting the analysis to a binary file took {round(bin_delta*1000)}ms\nExporting the analysis to a sqlite db took {round(sql_delta*1000)}ms")
	print(f"The binary file weights {snap_size} o.\nThe db file weights {db_size} o.")


	# prepare the import
	uc = LinUsersCollector()

	# Read the report content
	with open(report, "rb") as f:
		data = f.read()
	
	# Parse the data to recover the content
	rest = data
	while rest:
		first_byte = rest[0:1]
		encoded_data_len_size = VarInt.get_len(rest[1:2])
		encoded_data_len = VarInt.from_bytes(rest[1:1+encoded_data_len_size])
		rest = rest[1+encoded_data_len_size:]
		if first_byte == LinUsersCollector.snapshot_elemnt_id:
			rest = uc.import_bin(rest)

	# recover the same content from the database
	uc2 = LinUsersCollector()
	conn = sql.connect(reports_dir + "test.db")
	cursor = conn.cursor()
	uc2.import_db(cursor, run_id)
	conn.close()

	print("is it the same when importing?", uc == uc2)


if __name__ == '__main__':
	main()