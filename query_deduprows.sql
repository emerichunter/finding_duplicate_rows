WITH pks AS (
select tc.table_schema, tc.table_name, kc.column_name 
from information_schema.table_constraints tc 
join information_schema.key_column_usage kc on kc.table_name = tc.table_name 
and kc.table_schema = tc.table_schema and kc.constraint_name = tc.constraint_name 
where tc.constraint_type = 'PRIMARY KEY'
 and kc.ordinal_position is not null 
order by tc.table_schema, tc.table_name, kc.position_in_unique_constraint
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
--WHERE c.table_schema='public'
WHERE kc.constraint_name IS NULL
GROUP BY c.table_schema, c.table_name
ORDER BY c.table_schema, c.table_name
)
SELECT FORMAT ('SELECT  %I , count(%I)   as n_duplicate_rows, array_agg(%I) as pks 
FROM %I.%I 
GROUP BY %I
HAVING count(%I) >1;', col.str_col, col.arr_col[1], pks.column_name, col.table_schema, col.table_name, col.str_col, col.arr_col[1]) as sql_statement
FROM pks 
JOIN col 
  ON pks.table_schema= col.table_schema
AND pks.table_name=col.table_name 
;
