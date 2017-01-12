drop table if exists Item;
drop table if exists AuctionUser;
drop table if exists Bids;
drop table if exists Category;

create table Item(
	ItemID INTEGER PRIMARY KEY,
	Name TEXT,
	Currently REAL,
	Buy_Price REAL,
	First_Bid REAL,
	Number_of_Bids INTEGER,
	Started DATETIME,
	Ends DATETIME,
    SellerID TEXT,
	Description TEXT,
	FOREIGN KEY(SellerID) REFERENCES AuctionUser(UserID),
    CHECK(Ends > Started)
);

create table AuctionUser(
    UserID TEXT PRIMARY KEY,
    Location TEXT,
    Country TEXT,
    Rating INTEGER
);

create table Bids(
    ItemID INTEGER,
    BidderID TEXT,
    Amount REAL,
    Time DATETIME,
    UNIQUE(ItemID,Time),
    UNIQUE(ItemID,BidderID,Amount),
    FOREIGN KEY(BidderID) REFERENCES AuctionUser(UserID),
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID)
);

create table Category(
    ItemID INTEGER,
	Category TEXT,
	UNIQUE(ItemID,Category),
    FOREIGN KEY(ItemID) REFERENCES Item(ItemID)
);


DROP TABLE if exists CurrentTime;
CREATE TABLE CurrentTime(
	CTime DATETIME
);
INSERT into CurrentTime values ("2001-12-20 00:00:01");
SELECT * from CurrentTime;
