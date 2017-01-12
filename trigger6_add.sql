-- Trigger for Constraint #15. 
-- Block Addition of Bids when Bidding Time is not equal to the System Time in CurrentTime Table.

PRAGMA foreign_keys = ON;

drop trigger if exists block_bad_ctime;
create trigger block_bad_ctime
before insert ON Bids
for each row
when exists(
    select *
    from CurrentTime
    where new.Time <> CTime
)
begin
	select raise(rollback, 'Bidding Time has to match System Time');
end;
