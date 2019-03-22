# README.md 

## finding_duplicate_rows

[WIP] simple view to find all duplicate rows from PK
python script to give more readable results 

Much like maintenance_schema, this view allows to find exactly how many occurences and which tuples are duplicates. This only takes into account primary keys as entry. Need to expand to UNIQUE constraints as well. 

This is how to use it.
~~~~
postgres@dv400bd04g7018:~$ psql -t -d postgres -c "select * from rpt_duplicate_rows" | sed 's/"\|+//g' | psql -d postgres
 duplicate_rows | count |  pks
----------------+-------+-------
 toto           |     2 | {1,2}
(1 row)

 duplicate_rows | count | pks
----------------+-------+-----
(0 rows)

 content | duplicate_rows | count |  pks
---------+----------------+-------+-------
 toto2   |             12 |     2 | {2,5}
(1 row)

postgres@dv400bd04g7018:~$ psql
psql (9.6.11)
Type "help" for help.

postgres=# select * from dummy;
 id | content
----+---------
  1 | toto
  2 | toto
  3 | toto2
(3 rows)

postgres=# select * from dummy2;
 id | content
----+---------
(0 rows)

postgres=# select * from dummy3;
 id | content | num
----+---------+-----
  1 | toto    |  12
  2 | toto2   |  12
  3 | toto    |  14
  4 | toto2   |  14
  5 | toto2   |  12
(5 rows)

~~~~

Better now, use pg_deduplicator.py 

~~~~
postgres@dv400bd04g7018:~$ python pg_deduplicator.py

Relation name: public.dummy
Duplicate content | number or duplicates(L) | Name of keys
('toto', 2L, [1, 2])


Relation name: public.dummy2
Duplicate content | number or duplicates(L) | Name of keys


Relation name: public.dummy3
Duplicate content | number or duplicates(L) | Name of keys
('toto2', 12, 2L, [2, 5])


Relation name: public.dummy4
Duplicate content | number or duplicates(L) | Name of keys
(14, 'toto', 2L, [3, 4])


Relation name: public.dummy5
Duplicate content | number or duplicates(L) | Name of keys
~~~~


## TODO
- Add multiple PKs and unique Keys
