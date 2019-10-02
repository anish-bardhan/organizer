import collections
import numpy as np

#order class to store all information about each order
class Order():
    def __init__ (self, items = None, price = None, id = None, delivery_type= None, order_time = None):
        self.items = items
        self.price = price
        self.id = id
        self.delivery_type = delivery_type
        self.order_time = order_time

#item class to store information about each particular item
class Item():
    def __init__ (self, type = None, size = None, price = None, color = None, time = None):
        self.type = type
        self.size = size
        self.price = price
        self.color = color
        self.time = time

#order the orders based on importance (note: importance != time)
def order_orders(orders):
    order_importance= {}
    #iterate over every order
    for order in orders:
        #handle express vs regular orders
        if order.delivery_type == "express":
            importance = 200
        else:
            importance = 0
        #iterate over every item in order
        for item in order.items:
            if item.type == "hoodie":
                importance += 100
            elif item.type == "sweatshirt":
                importance += 70
            elif item.type == "t-shirt":
                importance += 50
        order_importance[order] = importance
    #put orders in ordered dictionary
    order_importance = collections.OrderedDict(order_importance)
    #return jus the orders but in order of their importand
    return list(order_importance.keys())

def total_day_cost (day):
    sum = 0
    for order in day:
        if order == None:
            continue
        for item in order.items:
            sum += item.time
    return sum

#assign the time to complete each order
def assign_time (ordered_orders, max_hours_per_day):
    #initialized work week schedule
    work_week = [[None],[None],[None],[None],[None]]
    #iterate over every order
    for order in ordered_orders:
        order_time = 0
        #iterate over every orders items
        for item in order.items:
            #assign time based on each item
            if item.type == "hoodie":
                order_time += 100
                item.time = 100
            elif item.type == "sweatshirt":
                order_time += 70
                item.time = 70
            elif item.type == "t-shirt":
                order_time += 50
                item.time = 50
        #if the order will take too long
        if order_time > 500:
            print ("we cannot handle order " + str(order.id) + " because it is too large")
            continue
        #if there are orders
        while order_time != 0:
            #iterate over each day in the work week
            for i in range (len(work_week)):
                day = work_week[i]
                #make sure the day is not full
                if day[-1] != True:
                    #calculate the work current day already has
                    t_d_c =  total_day_cost(day)
                    #check to see if current order can be added to current day
                    if order_time + t_d_c < max_hours_per_day:
                        #update time accordingly
                        order.order_time = order_time
                        day.append(order)
                        order_time = 0
                        break
                    #check to see if current order can be added to current day
                    elif order_time + t_d_c == max_hours_per_day:
                        #add order and mark day as full
                        order.order_time = order_time
                        day.append(order)
                        day.append(True)
                        order_time = 0
                        break
                    #if the order is too big
                    else:
                        #split the order up into multiple orders across multiple days
                        new_order = Order()
                        new_order.items = order.items
                        new_order.price = order.price
                        new_order.id = order.id
                        new_order.delivery_type = order.delivery_type
                        new_order.order_time = order_time - (order_time - (max_hours_per_day - t_d_c))

                        day.append(new_order)
                        day.append(True)
                        order_time = order_time - (max_hours_per_day - t_d_c)
                        #work_week[i+1] = (max_hours_per_day - order) * -1
                        break
                else:
                    continue
    return work_week

def pretty_print_w(work_week):
    #iterate over every day in the week
    for i in range (len(work_week)):
        day = work_week[i]
        #iterate over every order
        for order in day:
            if order == None or type(order) == bool:
                continue
            #print order attributes
            print ("Day: " + str(i+1))
            print("Order id: " + str(order.id))
            print("Order time for day: " + str(np.abs(order.order_time)) + " minutes")
            print ("Order items: ")
            for item in order.items:
                print (item.type)
            print ("\n")

def output_table(work_week):
    #iterate over every day in the week
    output = []
    itemers = []
    for i in range (len(work_week)):
        day = work_week[i]
        #iterate over every order
        for order in day:
            if order == None or type(order) == bool:
                continue
            #print order attributes
            output.append(str(i+1))
            output.append(str(order.id))
            output.append(str(np.abs(order.order_time)) + " minutes")
            for item in order.items:
                itemers.append(item.type)
            s = ','
            output.append(str(s.join(itemers)))
    return output

#create an order
order1 = Order()
order1.id = "1"
#add items to order
item1_1 = Item()
item1_1.type = "hoodie"
item1_2 = Item()
item1_2.type = "t-shirt"
order1.items = [item1_1, item1_2]

order2 = Order()
order2.id = "2"
item2_1 = Item()
item2_1.type = "t-shirt"
order2.items = [item2_1]

order3 = Order()
order3.id = "3"
item3_1 = Item()
item3_1.type = "sweatshirt"
item3_2 = Item()
item3_2.type = "sweatshirt"
order3.items = [item3_1]

orders = [order1,order2, order3]
#get orders in order of their importance
ordered_orders = order_orders(orders)
#assign the orders to each day of the work week
work_week = assign_time (ordered_orders, 100)
#print out new schedule
pretty_print_w(work_week)