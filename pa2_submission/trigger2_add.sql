-- Trigger for Constraint #9. 
-- Block Addition of Bids where BidderID is same as SellerID for a particular ItemID

PRAGMA foreign_keys = ON;

drop trigger if exists block_same_bid_sid;
create trigger block_same_bid_sid
before insert ON Bids
for each row
when exists(
    select *
    from Item
    where SellerID = new.BidderID and ItemID = new.ItemID
)
begin
	select raise(rollback, 'Seller cannot bid on his own item');
end;
