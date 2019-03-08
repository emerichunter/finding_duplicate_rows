#/usr/bin/python2.7
#
#

import psycopg2

# Try to connect

try:
    conn=psycopg2.connect("dbname='postgres' user='postgres'")
except:
    print "I am unable to connect to the database."

cur = conn.cursor()
try:
    cur.execute("""WITH pks AS (
SELECT tc.table_schema, tc.table_name, kc.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kc ON kc.table_name = tc.table_name
AND kc.table_schema = tc.table_schema AND kc.constraint_name = tc.constraint_name
WHERE (tc.constraint_type = 'PRIMARY KEY'
   OR tc.constraint_type = 'UNIQUE')
  AND kc.ordinal_position IS NOT NULL
ORDER BY tc.table_schema, tc.table_name, kc.position_in_unique_constraint
),
col AS (
SELECT c.table_schema, c.table_name, array_to_string(array_agg(c.column_name::text), ', ') as str_col, array_agg(c.column_name::text) as arr_col
FROM information_schema.columns c
LEFT JOIN information_schema.key_column_usage kc
ON kc.table_schema= c.table_schema
AND kc.table_name= c.table_name
AND kc.ordinal_position= c.ordinal_position
AND kc.column_name = c.column_name
LEFT JOIN information_schema.table_constraints tc
ON tc.table_schema=c.table_schema
AND tc.table_name=c.table_name
AND tc.constraint_name=kc.constraint_name
WHERE kc.constraint_name IS NULL
GROUP BY c.table_schema, c.table_name
ORDER BY c.table_schema, c.table_name
)
SELECT FORMAT ('SELECT %I, count(%I) as n_duplicate_rows, array_agg(%I) as pks_uks FROM %I.%I GROUP BY %I HAVING count(%I) >1;',
col.str_col, col.arr_col[1], pks.column_name, col.table_schema, col.table_name, col.str_col, col.arr_col[1]) as sql_statement,
col.table_schema || '.' || col.table_name as schema_table
FROM pks
JOIN col
  ON pks.table_schema= col.table_schema
 AND pks.table_name=col.table_name
;""")
except:
    print "Could not collect data"

rows = cur.fetchall()
#print "Query to be played: \n"
for row in rows:
    print "\n"
    print "Relation name: %s " %  (row[1])
    row=row[0].replace("\"", " ")
    #print row


    cur2 = conn.cursor()
    try:
        cur2.execute(row)

    except:
        print "Could not replay queries"

    results = cur2.fetchall()
    print "Duplicate content | number or duplicates(L) | Values of keys"
    for result in results:
        print result

