#RunParser 

rm -rf *.dat;

#Local
python my_parser.py ../ebay_data/items-*.json
#Corn Machine
#python my_parser.py /usr/class/cs145/project/ebay_data/items-*.json

sort user.dat | uniq > user_table.dat
sort bids.dat | uniq > bids_table.dat
sort category.dat | uniq > category_table.dat
sort item.dat | uniq > item_table.dat



