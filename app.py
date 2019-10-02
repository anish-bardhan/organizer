# importing necessary modules & functions from workload.py
from flask import Flask
from flask import render_template, request
import workload
from workload import Order, Item, pretty_print_w, assign_time, order_orders, output_table
import collections
import numpy as np

# inits flask app w debugger on
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    out = ['', '', '', '', '']
    return render_template('base.html', out=out)

@app.route('/', methods=['POST'])
def order_now():
    order1 = Order()
    item1_1 = Item()
    order1.id = request.form['order_id']
    item1_1.type = request.form['order_item']
    #day = request.form['day']
    order1.items = [item1_1]

    orders = [order1]
    #get orders in order of their importance
    ordered_orders = order_orders(orders)
    #assign the orders to each day of the work week
    work_week = assign_time(ordered_orders, 100)
    #print out new schedule
    out = output_table(work_week)

    return render_template('base.html', out=out)

    
if __name__ == '__main__':
    app.run()