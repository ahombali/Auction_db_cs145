import web

db = web.database(dbn='sqlite',
        db='AuctionBase.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select CTime from CurrentTime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].CTime # TODO: update this as well to match the
                                  # column name


# setting time
def setTime(new_time):
    query_string = 'update CurrentTime set CTime = $new_time'
    txn = transaction()
    try:
        db.query(query_string, {'new_time': new_time})
    except Exception as e:
        txn.rollback()
        #print "exception"
        #print e;
        #print str(e);
        return (str(e))
    else:
        txn.commit()
        msg_string = "Time updated to " + str(new_time)
        #print msg_string
        return (msg_string)

#add bid
def add_bid(item_id, user_id, price):
    if item_id == "" or user_id == "" or price == "":
        return ("Inputs cannot be empty, enter all values", False)

    txn = transaction();
    try:
        time = getTime();
        query_string = "insert into bids values ($ItemID, $UserID, $Amount, $bid_time)"
        db.query(query_string, {"ItemID" : item_id, "UserID": user_id, "Amount": price, "bid_time":time})
    except Exception as e:
        txn.rollback();
        return(str(e), False)
    else:
        txn.commit();
        return("Successfully added bid ",True)


#search
def browse_auction(item_id, category, description, minPrice, maxPrice, status):
    #fields = ["item_id", "category", "description", "minPrice", "maxPrice", "status"]
    at_least_one_clause_added = 0;
    db_dict = {};
    #TODO: Check what all is needed in search results.
    query_string = "select distinct(Item.ItemID), Name, Currently, Buy_Price, First_Bid, Number_of_Bids, Started, Ends, SellerID, Description from Item, Category where Item.ItemID = Category.ItemID"
    #query_string = "select * from Item, Category where Item.ItemID = Category.ItemID"
    at_least_one_clause_added = 1;
    if item_id != "":
        db_dict["item_id"] = item_id;
        if at_least_one_clause_added:
            query_string = query_string + " AND " + "Item.ItemID = $item_id";
        else:
            query_string = query_string + "Item.ItemID = $item_id";
            at_least_one_clause_added = 1; 

    
    if category != "":
        db_dict["category"] = category;
        if at_least_one_clause_added:
            query_string = query_string + " AND " + "Category = $category";
        else:
            query_string = query_string + "Category = $category";
            at_least_one_clause_added = 1; 

    if description != "":
        db_dict["description"] = "%" + description + "%";
        if at_least_one_clause_added:
            query_string = query_string + " AND " + "Description LIKE $description";
        else:
            query_string = query_string + "Description LIKE $description";
            at_least_one_clause_added = 1;

    if minPrice != "":
        db_dict["minPrice"] = minPrice;
        if at_least_one_clause_added:
            query_string = query_string + " AND " + "Currently >= $minPrice";
        else:
            query_string = query_string + "Currently >= $minPrice";
            at_least_one_clause_added = 1;

    if maxPrice != "":
        db_dict["maxPrice"] = maxPrice;
        if at_least_one_clause_added:
            query_string = query_string + " AND " + "Currently <= $maxPrice";
        else:
            query_string = query_string + "Currently <= $maxPrice";
            at_least_one_clause_added = 1; 

    #TODO: Figure out relation between Currently and Bug Price for Status = Open
    if status != "":
        time = getTime();
        db_dict["time"] = time;
        if at_least_one_clause_added:
            if status == "open":
                query_string = query_string + " AND " + "Started <= $time AND Ends > $time AND ((Currently < Buy_Price AND Buy_Price IS NOT NULL) OR Buy_Price is NULL)";
            elif status == "close":
                query_string = query_string + " AND " + "(Ends <= $time OR (Currently >= Buy_Price AND Buy_Price IS NOT NULL))";
            elif status == "notStarted":
                query_string = query_string + " AND " + "Started > $time"; 
        else:
            if status == "open":
                query_string = query_string + "Started <= $time AND Ends > $time";
            elif status == "close":
                query_string = query_string + "Ends <= $time";
            elif status == "notStarted":
                query_string = query_string + "Started > $time";  
            at_least_one_clause_added = 1;
            
            
             
    #print query_string;
    txn = transaction();
    try:
        data = db.query(query_string, db_dict);
    except Exception as e:
        txn.rollback();
        msg_string = "Error - Exception occured!. " + str(e);
        return (msg_string, None)
    else:
        txn.commit();
        return ("Following are the results of your search query", data);  




def get_item_info(item):
    txn = transaction()
    try:
        status = getItemStatus(item);
        bids = getItemBids(item);
        if status == "Closed" and len(bids) > 0:
            winner = bids[0]["BidderID"]
        else:
            winner = "None";
    except Exception as e:
        txn.rollback();
        status = "";
        bids = {};
        winner = "";
        msg_string = "Error - Exception occured!. " + str(e);
        return(msg_string, status, bids, winner);
    else:
        txn.commit();
        msg_string = "Following is the Auction Info for this Item";
        return(msg_string, status, bids, winner); 


def getItemBids(item):
    query_string = "select * from Bids where ItemID = $itemID ORDER BY Amount DESC"
    return query(query_string,{"itemID": item["ItemID"]})

#TODO: Figure out relation between Currently and Bug Price for Status = Open
#TODO
def getItemStatus(item):
    time = getTime()
    if item["Started"] > time:
        return "Not Started"
    if item["Ends"] <= time:
        return "Closed"
    if item["Buy_Price"] and item["Currently"] >= item["Buy_Price"]:
        return "Closed"
    return "Open"

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    txn = transaction();
    query_string = 'select * from Item where ItemID = $item_id'
    try:
        result = query(query_string, {'item_id': item_id})
    except Exception as e:
        txn.rollback()
        msg_string = "Error - Exception occured!. " + str(e);
        return (msg_string, None)
    else:
        txn.commit();
        if len(result) > 0:
            return ("Success", result[0])
        else:
            return ("Check Input! Item doesn't exist.", None)

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time
