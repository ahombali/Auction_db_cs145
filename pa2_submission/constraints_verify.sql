-- Foreign Key BidderID
select * 
from Bids 
where BidderID not in (select UserID from AuctionUser);

-- Foreign Key SellerID
select * 
from Item 
where SellerID not in (select UserID from AuctionUser);

-- Foreign Key ItemID in Bids table
select * 
from Bids 
where ItemID not in (select Itm.ItemID from Item as Itm);

-- Foreign key ItemID in Category Table
select * 
from Category 
where ItemID not in (select Itm.ItemID from Item as Itm);
