select count(distinct(Item.SellerID))
from Item, Bids
where Item.SellerID=Bids.BidderID;
