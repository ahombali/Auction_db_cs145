-- Trigger for Constraint #16. 
-- Block Updating system time in CurrenTime Table if new time is less than old/existing system time.

PRAGMA foreign_keys = ON;

drop trigger if exists block_bad_ctime_update;
create trigger block_bad_ctime_update
before update ON CurrentTime
for each row
when exists(
    select *
    from CurrentTime
    where new.CTime < old.CTime
)
begin
	select raise(rollback, 'System Time cannot go backward');
end;
