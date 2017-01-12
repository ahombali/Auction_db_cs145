-- Trigger for Constraint #8. 
-- Update Currently of Items Table when new bid is inserted

PRAGMA foreign_keys = ON;

drop trigger if exists update_currently;
create trigger update_currently
after insert ON Bids
for each row
begin
	update Item 
    set Currently = new.Amount 
    where ItemID = new.ItemID;
end;

