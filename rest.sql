PRAGMA foreign_keys = ON;

--insert into AuctionUser values ("007cowboy","Michigan","USA",1590);
--insert into Item values (198888888888888,"blah",30.00,NULL,30.00,0,"2001-12-20 00:00:01","2001-12-20 00:00:02","ahombali","brand");
--insert into Bids values (1043402767,"goldcoastvide",6.00,"2001-12-20 00:00:01");
--select * from Item where SellerID="ahombali";
--select * from AuctionUser where UserID="ahombali";
--insert into Category values (1000, "blah");

update Item set Started="2001-12-23 18:44:54",Ends="2001-12-23 18:44:59" where ItemID= 1043402767; 
--update Item set Ends="2001-12-23 18:44:59" where ItemID= 1043402767;
update CurrentTime set CTime = "2001-12-23 18:44:57";
--insert into Bids values (1043402767,"nobody138",10.00,"2001-12-03 18:44:54");
--select * from CurrentTime;
insert into Bids values (1043402767,"daba",12.07,"2001-12-23 18:44:57");
