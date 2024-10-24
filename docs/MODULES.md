# modules
This is where the features of the application as well as the collectors are implemented.

The package itself provides a few important data such as a list of which collectors are available.

*Data*:
- _AVAILABLE_COLLECTORS_ ([CollectorList](#))

## CollectorList(*__collectors = \[\]__*)
List object that must contain only collectors so we can easily perform operations with those collectors. It is subscriptible so you can use it as if it was a Python list.

*Arguments*:
- _collectors_ (list\[[Collector](#collector)\]): list of collectors.

*Attributes*:
- _collectors_ (list\[[Collector](#collector)\]): list of collectors.
- _names_ (list\[str\]): list of the names of the collectors list.
- _types_ (list\[bytes\]): list of the types of the collectors list.

### append(*__collector__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Append a collector to the list.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_collector_ ([Collector](#acollector)): the collector to append in the list.

### get_collector_by_name(*__name__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the collector by its name.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_name_ (str): name of the collector.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Collector.

### get_collector_by_type(*__type__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the collector by its type.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_type_ (bytes): type of the collector.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Collector.

### XOR(*__a, b__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_STATIC_** Make the disjunction (by their names) between 2 list of collectors.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_a_ ([CollectorList](#collectorlistcollectors)): the first list to compare with.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_b_ ([CollectorList](#collectorlistcollectors)): the second list to compare with.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of the different collectors name.

### AND(*__a, b__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_STATIC_** Make the junction (by their names) between 2 list of collectors.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_a_ ([CollectorList](#collectorlistcollectors)): the first list to compare with.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_b_ ([CollectorList](#collectorlistcollectors)): the second list to compare with.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of the same collectors name.

---------------------------------------------------
## Index
* [modules](#modules)
	---------------------------------------------------
	- [CollectorList](#collectorlistcollectors)
	    - [append](#appendcollector)
	    - [get_collector_by_name](#get_collector_by_namename)
	    - [get_collector_by_type](#get_collector_by_typetype)
	    ---------------------------------------------------
	    - [XOR](#xora-b)
	    - [AND](#anda-b)
	---------------------------------------------------
	- [Index](#index)
	---------------------------------------------------
	- [Collector](#collector)
	    - [AbstractMethodException](#abstractmethodexception)
	    - [FormattingError](#formattingerror)
	    - [RunningError](#runningerror)
	    ---------------------------------------------------
	    - [ACollectible](#acollectible)
	        - [to_bytes](#to_bytes)
	        - [export_report_db](#export_report_dbreport_id-run_id-status-db_cursor)
	        ---------------------------------------------------
	        - [from_bytes](#from_bytesdata)
	    - [ACollector](#acollector)
	        - [is_running](#is_running)
	        - [help](#help)
	        - [\_format](#_format)
	        - [\_export](#_export)
	        - [export_bin](#export_bin)
	        - [\_export_sql](#_export_sqldb-run_id)
	        - [export_db](#export_dbdb-run_id)
	        - [import_bin](#import_bindata)
	        - [import_db](#import_dbdb_cursor-run_id)
	        - [start_running](#start_running)
	        - [stop_running](#stop_running)
	        - [run](#run)
	        ---------------------------------------------------
	        - [make_diff](#make_diffa-b-report)
	        - [import_diff_from_report](#import_diff_from_reportdata-run_ids-report)
	        - [import_diff_from_report_db](#import_diff_from_report_dbdb_cursor-run_ids-report)
	        - [get_report_tree_structure](#get_report_tree_structure)
	        - [create_report_tables](#create_report_tablesdb_cursor)
	---------------------------------------------------
	- [UsersCollector](#userscollector)
		- [parse_user_line](#parse_user_lineline)
		- [parse_group_line](#parse_group_lineline)
		---------------------------------------------------
		- [User](#useruid-name-groups)
		- [Group](#groupgid-name)
		- [Sudoer](#sudoeruid)
		- [LinUsersCollector](#linuserscollector)
		    - [get_users](#get_users)
		    - [get_groups](#get_groups)
		    - [get_sudoers](#get_sudoers)
		    - [get_hashes](#get_hashes)
		    - [collect_users](#collect_users)
		    - [collect_groups](#collect_groups)
		    - [collect_sudoers](#collect_sudoers)
		    - [collect_passwd_hash](#collect_passwd_hash)
		    - [collect_group_hash](#collect_group_hash)
	        ---------------------------------------------------
		    - [make_diff](#make_diffrun_id_a-run_id_b-a-b-report)
		    - [import_diff_from_report](#import_diff_from_reportdata-run_ids-report)
	        - [import_diff_from_report_db](#import_diff_from_report_dbdb_cursor-run_ids-report)
	        - [get_report_tree_structure](#get_report_tree_structure)
	        - [create_report_tables](#create_report_tablesdb_cursor)
---------------------------------------------------

## Collector
This file contains the Abstract classes from which any Collector or Collectible implemented in _Exposure Scout_ inherits.

### AbstractMethodException()
Inherits from python built-in _Exception_.

### FormattingError()
Inherits from python built-in _Exception_.

### RunningError()
Inherits from python built-in _Exception_.

### ACollectible()
Abstract class from which every collectible element of a Collector should derive.\
_You should see it like a mix between an abstract class and an interface in Java._

*Attributes*:
- _element_name_ (str): name of the collectible.

#### to_bytes()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Converts the collectible to a byte string used to store it. **MUST** always been rewritten for every new module.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If it has not been implemented, raises [AbstractMethodException](#abstractmethodexception).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A bytes stream.

#### export_report_db(*__report_id, run_id, status, db_cursor__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Export a collectible data structure that is part of a diff report into the specified database.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): identifer of the report the element is linked to.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): identifier of the snapshot run the element comes from.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_status_ (int): value of the element's status in the diff report (created, deleted, modified, ...).\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_cursor_ ([Cursor](doc.python.org/3/library/sqlite3.html#sqlite3.Cursor)): sqlite3 cursor that points to the database.

#### from_bytes(*__data__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_STATIC_** Convert bytes into a Collectible. **MUST** always been rewritten for every new module.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): a bytes stream begining with the encoded data of the collectible.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A tupple containing:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. the collectible data structure recovered from the bytes stream;\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. the rest of the unread bytes that are not part of this collectible data structure.

### ACollector()
Abstract class from which every analysis/collector module should derive.\
_You should see it like a mix between an abstract class and an interface in Java._

*Attributes*:
- _name_ (str): name of the Collector module.
- _descr_ (str): description of what the module does and what it was created for.
- _snapshot_elemnt_id_ (byte): byte used to identify the collector in the binary file.

- _result_ (bytes): formated data collected by the collector so it can be exported. (default: None)
- _raw_result_ (dict{str : ACollectible}): data collected by the collector before to be formated for export. (default: None)
- _running_ (bool): flag repesenting whether the module is running or not. (default: None)

#### is_running()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Allows to check if the module is runing or not.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the module is running, False otherwize.

#### help()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the description of the module.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The description of the module.

#### \_format()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Private** method to format raw collected data of a run to exportable data. **MUST** always been rewritten for every new module.

#### \_export()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Private** method to export the result after running the module. **SHOULD** not be rewritten for every new module.

#### export_bin()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Public** method to export the result after running the module. It is mainly used by the [AnalysisManager](./CORE.md#analysismanager) of the [core](./CORE.md#core) python project module.

#### \_export_sql(*__db, run_id__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Private** method to export the result in a db after running the module. **MUST** be rewritten for every new module.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_ (str): path to the db.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): run identifier being exported.

#### export_db(*__db, run_id__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Public** method to export the result in a db after running the module. It is mainly used by the CollectorManager of the "core" python project module.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_ (str): path to the db.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): run identifier being exported.

#### import_bin(*__data__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Import method to recover data of a previous run. Those data can then be previewed.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): raw data with the first bytes representing this collector.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The rest of raw bytes unrelated to this collector.

#### import_db(*__db, run_id__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Import method to recover data of a previous run stored in DB. Those data can then be previewed.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note: must already been connected to the database.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_cursor_ ([Cursor](doc.python.org/3/library/sqlite3.html#sqlite3.Cursor)): pointer to the database.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_ (str): id used to store the collected data in the db of a specific run.

#### \_start_running()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Private** method used when starting the collector. **SHOULD** not be rewritten for every new module.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It can be rewritten to perform some task before the execution of the collector(e.g. setting a timer).

#### \_stop_running()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Private** method used when collector finished running. **SHOULD** not be rewritten for every new module.

#### \_run()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Private** Private method used to run the collector. **MUST** be rewritten for every new module since every module/collector works differently.

#### make_diff(*__a, b, report__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_Static_** method used to get the difference between two collectors of the same type. **MUST** be rewritten for every new module since every module/collecor works differently.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_a_ (str): run_id of the first collector.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_id_b_ (str): run_id of the second collector.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_a_ ([Collector](#acollector)): one of the collectors.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_b_ ([Collector](#acollector)): the other collector.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_ ([DiffReport](./CORE.md#diffreportfirst_run_id-second_run_id)): the report where to add the differences.

#### import_diff_from_report(*__data, run_ids, report__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_Static_** method used to import the values of report that are related to a given collector. **MUST** be rewritten for every new module since every module/collecor works differently.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): A bytes stream containing the data to import.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_ids_ (list[str]): the ordered list of the snapshot ids from which come the report elements.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_ ([DiffReport](./CORE.md#diffreportfirst_run_id-second_run_id)): datastructure in which to store the recovered data.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the [DiffElements](./CORE.md#diffelementrun_id-element-type) associated to the collector data have been successfully imported.

#### import_diff_from_report_db(*__db_cursor, run_ids, report__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_Static_** method used to import the values of report that are related to a given collector from a database. **MUST** be rewritten for every new module since every module/collecor works differently.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_cursor_ ([Cursor](doc.python.org/3/library/sqlite3.html#sqlite3.Cursor)): pointer to the database.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_ids_ (list[str]): the ordered list of the snapshot ids from which come the report elements.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_ ([DiffReport](./CORE.md#diffreportfirst_run_id-second_run_id)): datastructure in which to store the recovered data.

#### get_report_tree_structure()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_Static_** method used to get the structure of the Collector used for the report. **MUST** be rewritten for every new module since every module/collecor works differently.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A python dict representing the data structure to use in the [DiffReport](./CORE.md#diffreportfirst_run_id-second_run_id)

#### create_report_tables(*__db_cursor__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**_Static_** method used to create the different tables used by this collector for report structure in the specified database.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note: modifications are not committed here. MUST be rewritten for every new module since every module/collecor works differently.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_cursor_ ([Cursor](doc.python.org/3/library/sqlite3.html#sqlite3.Cursor)): sqlite3 cursor pointing to the database in which the tables must be created.

---------------------------------------------------
## UsersCollector
Implementation of the users collector to gather users, groups and sudoers on the machine. This collector inherits from the abstract Collector class. It also contains the data structures used for the different collectibles which inherit from the abstract Collectible class.

For every object, it describes how it can be exported or loaded and how it is being run.

### parse_user_line(*__line__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parse a line representing a user after running the collector bash script to extract data so it is easier to fill in the User data structure.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_line_ (str): the string line to parse.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A tupple with the uid, the user name, and the groups id it's in.

### parse_group_line(*__line__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parse a line representing a group after running the collector bash script to extract data so it is easier to fill in the Group data structure.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_line_ (str): the string line to parse.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A tupple with the gid, the group name.

### User(*__uid, name, groups__*)
Datastructure used to represent a Linux/Unix User.\
Implements method inherited from [ACollectible](#acollectible). Please refer to it for its methods description.

*Arguments*:
- _uid_ (int): user id.
- _name_ (str): user's name.
- _groups_ (list[int]): list of groups' gid the user is in.

*Attributes*:

	element_name = "User"

- _element_name_ (str): name used to identify this collectible.

- _uid_ (int): user id.
- _name_ (str): user's name.
- _groups_ (list[int]): list of groups' gid the user is in.

### Group(*__gid, name__*)
Datastructure used to represent a Linux/Unix Group.\
Implements method inherited from [ACollectible](#acollectible). Please refer to it for its methods description.

*Arguments*:
- _gid_ (int): group id.
- _name_ (str): group's name.

*Attributes*:

	element_name = "Group"

- _element_name_ (str): name used to identify this collectible.

- _gid_ (int): group id.
- _name_ (str): group's name.

### Sudoer(*__uid__*)
Datastructure used to represent the sudoers.\
Implements method inherited from [ACollectible](#acollectible). Please refer to it for its methods description.

*Arguments*:
- _uid_ (int): sudoer's user id.

*Attributes*:

	element_name = "Sudoer"

- _element_name_ (str): name used to identify this collectible.

- _uid_ (int): sudoer's user id.

### LinUsersCollector()
Users, Groups and Sudoers collector.\
Implements method inherited from [ACollector](#acollector). Please refer to it for more methods.

*Attributes*: Inherits from [ACollector](#acollector).

	name = "Users Collector"
	descr = """
			For Linux/Unix platforms only.
			This module collects all the users and groups as well as sudoers available on this machine.
			"""
	snapshot_elemnt_id = b"\x00"

#### get_users()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the list of collected users.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of [Users](#useruid-name-groups). (None if collector has not run yet)

#### get_groups()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the list of collected groups.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of [Groups](#groupgid-name). (None if collector has not run yet)

#### get_sudoers()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the list of collected sudoers.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A list of [Sudoers](#sudoeruid). (None if collector has not run yet)

#### get_hashes()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Get the two collected hashes (passwd, group).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A tupple with both hashes.

#### collect_users()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Executes the bash script that will collect all the users.

#### collect_groups()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Executes the bash script that will collect all the groups.

#### collect_sudoers()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Executes the bash script that will collect the list of sudoers.

#### collect_passwd_hash()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Computes the /etc/passwd file md5 hash.

#### collect_group_hash()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Computes the /etc/group file md5 hash.

#### make_diff(*__run_id_a, run_id_b, a, b, report__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Static**_ method used to get the difference between two "Linux/Unix users" collectors. **SHOULD** be used only if the two hashes have been checked and are different between both the collectors.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*: Inherits from [ACollector](#acollector).

#### import_diff_from_report(*__data, run_ids, report__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Static**_: Extract LinUsersCollector's elements from a report file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_data_ (bytes): a bytes stream representing the elements associated to this collector in the report.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_ids_ (list[str]): the ordered list of the snapshot ids from which come the report elements.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_ ([DiffReport](./CORE.md#diffreportfirst_run_id-second_run_id)): datastructure in which to store the recovered data.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;True if the [DiffElements](./CORE.md#diffelementrun_id-element-type) associated to LinUsersCollector data have been successfully imported.

#### import_diff_from_report_db(*__db_cursor, report_id, run_ids, report__*)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Static**_: Extract LinUsersCollector's diff elements from a database.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_cursor_ ([Cursor](doc.python.org/3/library/sqlite3.html#sqlite3.Cursor)): pointer to the database.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_id_ (str): identifier of the report being imported.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_run_ids_ (list[str]): the ordered list of the snapshot ids from which come the report elements.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_report_ ([DiffReport](./CORE.md#diffreportfirst_run_id-second_run_id)): datastructure in which to store the recovered data.

#### get_report_tree_structure()
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Static**_: Get the structure of the Collector used for the report.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Returns*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A python dict with an empty list of users, an empty list of groups, and an empty list of sudoers.

#### create_report_tables(*__db_cursor__*):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_**Static**_ method used to create the different tables used by this collector for report structure in the specified database.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note: modifications are not committed here.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*Arguments*:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_db_cursor_ ([Cursor](doc.python.org/3/library/sqlite3.html#sqlite3.Cursor)): sqlite3 cursor pointing to the database in which the tables must be created.