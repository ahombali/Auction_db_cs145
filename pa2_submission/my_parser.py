
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"
newLine = "\n"


# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file, item_dat, user_dat, category_dat, bids_dat):
	
    #Create file handles for all the dat files



    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            add_item_tuple(item_dat, item);
            add_user_tuple(user_dat, item);
            add_category_tuple(category_dat, item);
            add_bids_tuple(bids_dat, item);
    
def convert_to_sql_compatible_string(strng):
    return '"' + strng.replace('"','""') + '"';

def add_item_tuple(item_dat, item):
    item_id = item['ItemID'];
    name = convert_to_sql_compatible_string(item['Name']);
    currently = transformDollar(item['Currently']);
    if "Buy_Price" in item:
        buy_price = transformDollar(item["Buy_Price"]);
    else:
        buy_price = "NULL"
    first_bid = transformDollar(item["First_Bid"]);
    number_of_bids = item["Number_of_Bids"];
    started = transformDttm(item["Started"])
    ends = transformDttm(item["Ends"])
    seller_id = convert_to_sql_compatible_string((item["Seller"])["UserID"]);
    # Some descriptions are Null
    if "Description" in item and item["Description"] != None:
        description = convert_to_sql_compatible_string(item["Description"]);
    else:
        description = "NULL";
    
    # Create Row tuple and write to DAT file
    row_tuple = item_id+columnSeparator+name+columnSeparator+currently+columnSeparator+buy_price+columnSeparator+first_bid+columnSeparator+number_of_bids+columnSeparator+started+columnSeparator+ends+columnSeparator+seller_id+columnSeparator+description+newLine;
    item_dat.write(row_tuple);

    #Debug
    #if (item_id == '1043397459'):
    #if (item_id == '1043374545'):
    #    print "Curr Item id";
    #    print item_id;
    #    print name;
    #    print currently;
    #    print row_tuple;

def add_user_tuple(user_dat, item):
    # First add seller user to the table
    user_id = convert_to_sql_compatible_string((item["Seller"])["UserID"])
    location = convert_to_sql_compatible_string(item["Location"])
    country = convert_to_sql_compatible_string(item["Country"])
    rating = (item["Seller"])["Rating"]

    row_tuple = user_id+columnSeparator+location+columnSeparator+country+columnSeparator+rating+newLine;
    user_dat.write(row_tuple)

    #Next add Bidder user info
    if "Bids" in item:
        bids = (item["Bids"]);
        if (bids != None):
            for i in range(0,len(bids)):
                bidder = (bids[i]["Bid"])["Bidder"];
                user_id = convert_to_sql_compatible_string(bidder["UserID"]);
                #location
                if "Location" in bidder:
                    location = convert_to_sql_compatible_string(bidder["Location"]);
                else:
                    location = "NULL"
                #country
                if "Country" in bidder:
                    country = convert_to_sql_compatible_string(bidder["Country"]);
                else:
                    country = "NULL"
                #rating
                rating = bidder["Rating"];
                row_tuple = user_id+columnSeparator+location+columnSeparator+country+columnSeparator+rating+newLine;
                user_dat.write(row_tuple)


def add_category_tuple(category_dat, item):
    
    item_id = item['ItemID'];
    item_categories = item['Category'];
    
    #Null check needed? TODO

    for i in range(0,len(item_categories)):
        category = item_categories[i];
        category = convert_to_sql_compatible_string(category);
        # Create Row tuple and write to DAT file
        row_tuple = item_id + columnSeparator + category + newLine;
        category_dat.write(row_tuple);

    #Debug
    #if (item_id == '1043397459'):
    #    print "Got Item id";
    #    print item_categories; 


def add_bids_tuple(bids_dat, item):
    
    item_id = item['ItemID'];
    if "Bids" in item:
        bids = (item["Bids"]);
        if (bids != None):
            for i in range(0,len(bids)):
                bid = bids[i]["Bid"];
                user_id = convert_to_sql_compatible_string((bid["Bidder"])["UserID"]);
                amount = transformDollar(bid["Amount"]);
                time = transformDttm(bid["Time"])
                # Create Row tuple and write to DAT file
                row_tuple = item_id+columnSeparator+user_id+columnSeparator+amount+columnSeparator+time+newLine;
                bids_dat.write(row_tuple);
                
                #Debug
                #if (item_id == "1043495702"):
                #    print row_tuple;


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    
    # Open all DAT files to be written.
    item_dat = open('item.dat', 'w');
    user_dat = open('user.dat', 'w');
    category_dat = open('category.dat', 'w');
    bids_dat = open('bids.dat', 'w');

    for f in argv[1:]:
        if isJson(f):
            parseJson(f, item_dat, user_dat, category_dat, bids_dat)
            print "Success parsing " + f

    #Close all opened files
    item_dat.close();
    user_dat.close();
    category_dat.close();
    bids_dat.close();  

if __name__ == '__main__':
    main(sys.argv)
