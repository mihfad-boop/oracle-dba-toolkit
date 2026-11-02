select s1.sid
       || ','
       || s1.serial# blocker,
       s2.sid
       || ','
       || s2.serial# blocked
  from v$lock l1
  join v$session s1
on l1.sid = s1.sid
  join v$lock l2
on l1.id1 = l2.id1
  join v$session s2
on l2.sid = s2.sid
 where l1.block = 1
   and l2.request > 0;
