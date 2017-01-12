-- Trigger for Constraint #11. 
-- Block Addition of Bids when Bidding Time is outside the range of Start Time or End Time for that particular ItemID

PRAGMA foreign_keys = ON;

drop trigger if exists block_outiside_time_range;
create trigger block_outiside_time_range
before insert ON Bids
for each row
when exists(
    select *
    from Item
    where ItemID = new.ItemID and (new.Time < Started OR new.Time > Ends)
)
begin
	select raise(rollback, 'Bidding Time has to be in between Start Time and End Time for that ItemID');
end;

