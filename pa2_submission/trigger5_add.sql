-- Trigger for Constraint #14. 
-- Block Addition of Bids when Bid Amount is not higher than any of the bid amounts for that ItemID.

PRAGMA foreign_keys = ON;

drop trigger if exists block_bad_bid_amnt;
create trigger block_bad_bid_amnt
before insert ON Bids
for each row
when exists(
    select *
    from Bids
    where ItemID = new.ItemID and new.Amount <= Amount
)
begin
	select raise(rollback, 'Bid Amount has to be higher than any of the previous Bids for that Item');
end;
