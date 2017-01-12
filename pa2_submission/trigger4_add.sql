-- Trigger for Constraint #13. 
-- Update Number of Bids in Items Table when new a new bid is inserted for that ItemID

PRAGMA foreign_keys = ON;

drop trigger if exists update_num_bids;
create trigger update_num_bids
after insert ON Bids
for each row
begin
	update Item 
    set Number_of_Bids = Number_of_Bids + 1
    where ItemID = new.ItemID;
end;


