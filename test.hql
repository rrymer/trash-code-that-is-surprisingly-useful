--author=Richard Rymer
insert into table a73270.why_is_hive_stupid
select cast(from_unixtime(unix_timestamp(substring("${TODAY}",0,10),'yyyy-MM-dd'),'u') as string)
from  a73270.why_is_hive_stupid