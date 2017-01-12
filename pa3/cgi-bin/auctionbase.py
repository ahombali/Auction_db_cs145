#!/usr/bin/env python

import sys; sys.path.insert(0, 'lib') # this line is necessary for the rest
import os                             # of the imports to work!

import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
# current_time = string_to_time(sqlitedb.getTime())

def string_to_time(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=extensions,
            )
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)

    return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/currtime', 'curr_time',
        '/selecttime', 'select_time',
        # TODO: add additional URLs here
        # first parameter => URL, second parameter => class name
        '/add_bid','add_bid',
        '/search','search',
        '/auction_info','item_info',
        )


class item_info:
    def GET(self):
        get_params = web.input();
        #print get_params;
        item_id = get_params["itemID"];
        ret_status1 = sqlitedb.getItemById(item_id);
        if ret_status1[1] == None:
            message = ret_status1[0];
            status = "";
            winner = "";
            bids = {};
            return render_template('item_info.html', item_id = item_id, message = message, status = status, bids = bids, winner = winner)
        else:
            ret_status = sqlitedb.get_item_info(ret_status1[1]);
            message = ret_status[0];
            status = ret_status[1];
            bids = ret_status[2];
            winner = ret_status[3];
            return render_template('item_info.html', item_id = item_id, message = message, status = status, bids = bids, winner = winner)

   #def POST(self):
   #    post_params = web.input()
   #    item_id = post_params["itemID"]
   #    ret_status1 = sqlitedb.getItemById(item_id);
   #    if ret_status1[1] == None:
   #        message = ret_status1[0];
   #        return render_template('item_info.html', message = message)
   #    else:
   #        ret_status = sqlitedb.get_item_info(ret_status1[1]);
   #        message = ret_status[0];
   #        status = ret_status[1];
   #        bids = ret_status[2];
   #        winner = ret_status[3];
   #        return render_template('item_info.html', message = message, status = status, bids = bids, winner = winner)
         

class curr_time:
    # A simple GET request, to '/currtime'
    #
    # Notice that we pass in `current_time' to our `render_template' call
    # in order to have its value displayed on the web page
    def GET(self):
        current_time = sqlitedb.getTime()
        return render_template('curr_time.html', time = current_time)

class select_time:
    # Aanother GET request, this time to the URL '/selecttime'
    def GET(self):
        return render_template('select_time.html')

    # A POST request
    #
    # You can fetch the parameters passed to the URL
    # by calling `web.input()' for **both** POST requests
    # and GET requests
    def POST(self):
        post_params = web.input()
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss'];
        enter_name = post_params['entername']


        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        status = sqlitedb.setTime(selected_time);
        update_message = status;

        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)


class add_bid:
    def GET(self):
        return render_template('add_bid.html')

    def POST(self):
        post_params = web.input()
        item_id = post_params["itemID"]
        user_id = post_params["userID"]
        price = post_params["price"]
        status = sqlitedb.add_bid(item_id, user_id, price)
        return render_template('add_bid.html', message = status[0], add_result = status[1])
        

class search:
    def GET(self):
        return render_template('search.html')

    def POST(self):
        post_params = web.input()
        item_id = post_params["itemID"]
        category = post_params["category"]
        description = post_params["description"]
        minPrice = post_params["minPrice"]
        maxPrice = post_params["maxPrice"]
        auction_status = post_params["status"]
        ret_status = sqlitedb.browse_auction(item_id, category, description, minPrice, maxPrice, auction_status)
        return render_template('search.html', message = ret_status[0], search_result = ret_status[1])

###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
    app.run()
