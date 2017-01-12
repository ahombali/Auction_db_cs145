select count(distinct(sellerID))
from Item
where sellerID in (select UserID
                    from AuctionUser
                    where Rating > 1000);
