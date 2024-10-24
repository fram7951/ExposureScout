# core
This is where the core functionalities of the application are implemented.

You can extend or modify it but keep in mind that any modification in those files may corrupt the application if not handled carefully.

---------------------------------------------------
## Index
* [core](#core)
	---------------------------------------------------
	- [Index](#index)
	---------------------------------------------------
	- [analysis_manager](#analysis_manager)
	    - [AnalysisManager](#analysismanager)
	        - [is_running](#is_running)
	        - [get_running_snapshot](#get_running_snapshot)
	        - [save](#saverun_id-method--bin-db--none-buf_size--64)
	        - [load](#loadrun_id-method--bin-db--none-buf_size--64)
	        - [dump](#dumprun_id)
	        - [dump_report](#dump_reportreport_id)
	        - [pause_running](#pause_running)
	        - [resume_running](#resume_running)
	        - [quit_running](#quit_running)
	        - [show_running_status](#show_running_status)
	        - [run_snapshot](#run_snapshotrun_id-collectors)
	        - [make_diff](#make_difffirst_run-second_run-report_id--none)
	        - [export_report](#export_reportreport_id-method--bin-db--none-buf_size--64)
	        - [import_report](#import_reportreport_id-method--bin-db--none-buf_size--64)
	---------------------------------------------------
	- [report](#report)
	    - [parse_snap_header](#parse_snap_headerdata)
	    - [parse_rpt_header](#parse_rpt_headerdata)
	    ---------------------------------------------------
	    - [AlreadyExistsException](#alreadyexistsexception)
	    - [UnknownValueException](#unknownvalueexception)
	    ---------------------------------------------------
	    - [DiffElement](#diffelementrun_id-element-type)
	        - [get_collectible_name](#get_collectible_name)
	        - [to_bytes](#to_bytesrun_id_bytes)
	        - [from_bytes](#from_bytesrun_ids-element_class)
	        - [export_db](#export_dbreport_id-db_cursor)

	    - [DiffReport](#diffreportfirst_run_id-second_run_id)
	        - [get_collectors_names](#get_collectors_names)
	        - [add_diff_element](#add_diff_elementelement-collector_name)
	        - [add_no_diff_element](#add_no_diff_elementcollector_name-type)
	        - [add_no_diff_collector](#add_no_diff_collectorcollector_name)
	        - [to_bytes](#to_bytes)
	        - [read_collector_from_bytes](#read_collector_from_bytesdata-run_ids-collector)
	        - [export_db](#export_dbreport_id-db)
	---------------------------------------------------
	- [tools](#tools)
	    - [xor_list](#xor_lista-b)
	    - [and_list](#and_lista-b)
	    - [get_file_hash](#get_file_hashfilename-buf_size--65536)
	    ---------------------------------------------------
	    - [ResultThread](#resultthreadargs-kwargs)
	---------------------------------------------------
	- [octets](#octets)
	    - [VarInt](#varint)
	        - [to_bytes](#to_bytesvalue)
	        - [get_len](#get_lenb_array)
	        - [from_bytes](#from_bytesb_array)
---------------------------------------------------

## analysis_manager
This is the heart of the application. It manages all the collectors, the snapshots ran or loaded and the reports of diff. You can use it as a "Memory Manager" of the application and you should use it to perform all commands since it implements all the application features.

### AnalysisManager()
Core module used to manage all the different runs and make analysis between them.\
It can also manage the memory used by the different runs (you can dump runs to free memory, otherwize every run is kept in memory either they have been saved ot not so it is faster if you want to make analysis between those runs).

*Attributes*:
- runs (dict{str:[CollectorList](./MODULES.md#collectorlist)}): the different runs in memory that are ready to use (to be analyzed or to be stored). Every run is identified by its run id as a string and its collectors.
- running_snapshot (str): used to know what snapshot is running, using its run_id.
- running_snapshot_threads (list[threading.Thread]): list of all the threads running for the running snapshot.
- snapshot_paused (bool): flag used to know if the running snapshot has been paused or not.
- diff_reports (dict{str : DiffReport}): list of reports of differences between two snapshots that have been performed.

#### is_running()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the running status.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if a snapshot is beeing run.

#### get_running_snapshot()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the collectors of the running snapshot.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The list of collectors being run, None if no snapshot is running.

#### save(_**run_id, method = BIN, db = None, buf_size = 64**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Export a snapshot.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): the run identifier.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_method_ (int): the method used to export the data (binary: 0, sqlite3 db: 1). (default = BIN = 0)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_ (str): path to the database. (MUST be used ONLY if method is set to 1 (DB), default = None)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_buf_size_ (int): buffer size in kB used while writing a snap file. (default = 64)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the export succeeded, False otherwize.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: unknown method provided.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: method is set to 1 (DB) but no path to the database provided.

#### load(_**run_id, method = BIN, db = None, buf_size = 64**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Import a snapshot.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): the run identifier.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_method_ (int): the method used to export the data (binary: 0, sqlite3 db: 1). (default = BIN = 0)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_ (str): path to the database. (MUST be used ONLY if method is set to 1 (DB), default = None)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_buf_size_ (int): buffer size in kB used while reading a snap file. (default = 64)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the loading was successful, False if it has already been loaded.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: unknown method provided.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: method is set to 1 (DB) but no path to the database provided.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_IOError_: corrupted file (header and content do not match together).\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_IOError_: impossible to parse the file content.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_FileNotFoundError_: incorrect path to the file (based on the run_id).

#### dump(_**run_id**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Free the memory by dumping a run/snapshot.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): the run identifier.

#### dump_report(_**report_id**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Free the memory by dumping a report.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): the report identifier.

#### pause_running()
_WIP_

#### resume_running()
_WIP_

#### quit_running()
_WIP_

#### show_running_status()
_WIP_

#### run_snapshot(_**run_id, collectors**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Runs collectors for a snapshot.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): identifier of the snapshot.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_collectors_ (list\[str\]): list of collectors' name used for the analysis.

#### make_diff(_**first_run, second_run, report_id = None**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Analyze the difference between two snapshots.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_first_run_ (str): run_id of the first run to compare.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_second_run_ (str): run_id of the second run to compare.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): identifies the report. (default: None; if None, then combines the first and second snapshot id's)

#### export_report(_**report_id, method = BIN, db = None, buf_size = 64**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Export a report.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): identifier of the report.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_method_ (int): the method used to export the data (binary: 0, sqlite3 db: 1). (default = BIN = 0)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_ (str): path to the database. (MUST be used ONLY if method is set to 1 (DB), default = None)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_buf_size_ (int): buffer size in kB used while writing a rpt file.. (default = 64)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the export succeeded, False otherwize.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: unknown method provided.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: method is set to 1 (DB) but no path to the database provided.

#### import_report(_**report_id, method = BIN, db = None, buf_size = 64**_):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;import a report.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): identifier of the report.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_method_ (int): the method used to export the data (binary: 0, sqlite3 db: 1). (default = BIN = 0)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_ (str): path to the database. (MUST be used ONLY if method is set to 1 (DB), default = None)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_buf_size_ (int): buffer size in kB used while reading a rpt file. (default = 64)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the loading was successful, False if it has already been loaded.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: unknown method provided.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: method is set to 1 (DB) but no path to the database provided.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_FileNotFoundError_: incorrect path to the file (based on the run_id).\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_IOError_: unexpected bytes at the end of the file.

---------------------------------------------------
## report
In this file, you can find the definition of a report and all the objects related to it. Basically, a report is represented as a python dictionnary containing a list of elements that was different from the two snapshots being compared for every collector they used.

*Data*:
- CREATED
- DELETED
- MODIFIED

### parse_snap_header(_**data**_):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parse the header of a snapshot binary file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): header as bytes to parse.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of tupple containing the type of containers and their position in the file.

### parse_rpt_header(_**data**_):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parse the header of a report binary file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): header as bytes to parse.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A tupple containing:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. an ordered list of the snapshot id's of the compared snapshots in the report;\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. a list of tupple containing the type of containers and their position in the file.

### AlreadyExistsException()
Inherits from python built-in _Exception_.

### UnknownValueException()
Inherits from python built-in _Exception_.

### DiffElement(_**run_id, element, type**_)
Representation of an element that differs during a comparison.\
It can either be a new element or an element that has changed between two snapshots.

*Arguments*:
- _run_id_ (str): identifier of the snapshot the element is associated to.
- _element_ (Object): the objects used by a collector to store what they collect. (e.g. [User](./MODULES.md#useruid-name-groups) in [UsersCollector](./MODULES.md#userscollector) to store users)
- _type_ (str): type of the element. (e.g. [User](./MODULES.md#useruid-name-groups) in [UsersCollector](./MODULES.md#userscollector) has the "user" type)

*Attributes*:
- _run_id_ (str): identifier of the snapshot the element is associated to.
- _element_ (Object): the objects used by a collector to store what they collect. (e.g. [User](./MODULES.md#useruid-name-groups) in [UsersCollector](./MODULES.md#userscollector) to store users)
- _type_ (str): type of the element. (e.g. [User](./MODULES.md#useruid-name-groups) in [UsersCollector](./MODULES.md#userscollector) has the "user" type)

#### get_collectible_name()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the name of the collectible being stored.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The element_name of the stored collectible.

#### to_bytes(_**run_id_bytes**_):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Encode an element of the tree of differences.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_bytes_ (dict{str:bytes}): python dictionary mapping the run_id's used in the report to their respective byte identifier.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A bytes stream represdenting the element.

#### from_bytes(_**run_ids, element_class**_):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_STATIC_** Decode an element of the tree of differences.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): a bytes stream representing a DiffElement.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_ids_ (list\[str\]): the snapshot id's used for the report.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_element_class_ ([Collectible](./MODULES.md#acollectible)): reference to the class of the element.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A tupple containing:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. a bytes stream represdenting the element;\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. the rest of the unread bytes that are not part of this DiffElement datastructure.

#### export_db(_**report_id, db_cursor**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Insert the element into the database.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): identifier of the report the element is linked to.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_cursor_ ([Cursor](doc.python.org/3/library/sqlite3.html#sqlite3.Cursor)): cursor pointing to the sqlite3 database.

### DiffReport(_**first_run_id, second_run_id**_)
Report of the differences between two snapshots.

*Arguments*:
- _first_run_id_ (str): identifier of the first snapshot to compare with.
- _second_run_id_ (str): identifier of the second snapshot to compare with.

*Attributes*:
- _first_run_id_ (str): identifier of the first snapshot to compare with.
- _second_run_id_ (str): identifier of the second snapshot to compare with.
- _diff_elements_ \(dict\{str : dict\{str : list\[[DiffElement](#diffelementrun_id-element-type)\]\}\}\): tree of differences.

#### get_collectors_names()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get a list of all the collectors' names in the tree of differences.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of collector's names.

#### add_diff_element(_**element, collector_name**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Add an element to the tree of differences.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_element_ ([DiffElement](#diffelementrun_id-element-type)): the element to add in the tree.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_collector_name_ (str): the name of the collector that is compared.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_[UnknownValueException](#unknownvalueexception)_: run id does not match between the snapshots beeing compared and the snapshot from which the element comes from.

#### add_no_diff_element(_**collector_name, type**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Add the name of an element type of a collector for which there were no changes between the two snapshots.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(e.g. for [LinUsersCollector](./MODULES.md#linuserscollector), there could be a new user without new group or sudoer)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_collector_name_ (str): the name of the collector that is compared.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_type_ (str): the name of the element type of the collector that is compared.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_[AlreadyExistsException](#alreadyexistsexception)_: the element type already is in the report for the given collector name.

#### add_no_diff_collector(_**collector_name**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Add the name of a collector that has not changed between the two snapshots.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_collector_name_ (str): the name of the collector that is compared.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_[AlreadyExistsException](#alreadyexistsexception)_: the collecton name already is in the report.

#### to_bytes()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Encode the tree of differences.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A bytes stream representing\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. the header with preliminar informations over the collectors in the tree;\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. the tree of differences.

#### read_collector_from_bytes(_**data, run_ids, collector**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Decode a bytes stream into a DiffReport for a single collector.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): the bytes stream that represent the DiffReport.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_ids_ (list\[str\]): ordered list of the snapshot id's compared in the report. (order is the same as in the report file)\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_collectors_ (list\[Class\]): ordered list of references to collectors classes used in the report. (order is the same as in the report file)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the decoding was successful.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: collectors do not match

#### export_db(_**report_id, db**_):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Export the report in the specified database.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): identifer of the report.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_ (str): path to the database.

---------------------------------------------------
## tools
It provides useful tools such as computing the md5 hash of a file or implements functions to use logical _xor_ and _and_ on python lists.

### xor_list(_**a, b**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Make the disjunction (by their names) between 2 lists.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_a_ (list): the first list to compare with.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_b_ (list): the second list to compare with.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A tupple with the elements of the first list and the ones of the second.

### and_list(_**a, b**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Make the junction (by their names) between 2 list of collectors.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_a_ (list): the first list to compare with.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_b_ (list): the second list to compare with.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of the selements that appears on both the provided lists.

### get_file_hash(_**filename, buf_size = 65536**_)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the MD5 hash of a file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_filename_ (str): path to the file to get its hash.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_buf_size_ (int): buffer size. Helps reading big files. (default: 64kb = 65536b)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A byte string representing the MD5 hash of the given file.

### ResultThread(*__\*args, \*\*kwargs__*)
Inherits from [threading.Thread](https://docs.python.org/3/library/threading.html#threading.Thread) class and only features the result handling of the target function it ran via the _result_ attribute.

---------------------------------------------------
## octets
It provides dynamic compression mecanism for Integer values thanks to VarInt. The mecanism is itself based on the one used by the _QUIC_ protocol.

**length (bytes)**|**values encoded**|**prefix**|**value mask**|**binary representation**
:---:|:---:|:---:|---|---
1|5 => 0 - 31|00|1F|000x xxxx
2|13 => 32 - 8,191|20|1F FF|001x xxxx xxxx xxxx
3|21 => 8,192 - 2,097,151|40|1F FF FF|010x xxxx ... xxxx xxxx
4|29 => 2,097,152 - 536,870,911|60|1F FF FF FF|011x xxxx ... xxxx xxxx
5|37 => 536,870,912 - 2^(37)-1|80|1F FF FF FF FF|100x xxxx ... xxxx xxxx
6|45 => 2^(37) - 2^(45)-1|A0|1F FF FF FF FF FF|101x xxxx ... xxxx xxxx
7|53 => 2^(45) - 2^(53)-1|C0|1F FF FF FF FF FF FF|110x xxxx ... xxxx xxxx
8|61 => 2^(53) - 2^(61)-1|E0|1F FF FF FF FF FF FF FF|111x xxxx ... xxxx xxxx

Note that the mask used to know the prefix is only 1 byte long and is _0xE0_ since we only need the first byte to know the varint length. After checking the prefix,
we know the length and therefore can get as many bytes we need to decode the value, applying the right mask.
Length increases linearly compared to the exponential used within QUIC (1, 2, 4, 8) so we can encode values on lower amount of bytes.

In practice, here we should not get values encoded on more than 32 bits, so the biggest varint length we should encounter in this project is 5 bytes long. We can accept this little increasing of one byte compared to the regular encoding for integer values since the majority of the covered integer values here are at worst encoded on 4 bytes as well.

### VarInt
#### to_bytes(*__value__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_STATIC_** Converts an interger value to a varint byte stream. (0 <--> (2\*\*61)-1)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_value_ (int): the value to convert.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A byte string.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Raises*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_ValueError_: if negative or too great value has been provided.

#### get_len(*__b_array__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_STATIC_** Get the length in bytes of the varint value a byte array begins with.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_b_array_ (bytes): a byte stream.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The length of the varint value the byte array begins with.

#### from_bytes(*__b_array__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_STATIC_** Read a byte string to extract its varint value.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_b_array_ (bytes): a byte stream.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The recovered value.