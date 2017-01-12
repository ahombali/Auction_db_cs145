select count(*)
from (
    select ItemID
    from Category as C
    group by C.ItemID
    having count(C.Category)=4
);
