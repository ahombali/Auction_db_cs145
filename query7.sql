select count(distinct(C.Category))
from Bids as B, Category as C
where ((C.ItemID = B.ItemID) and (B.Amount > 100));
