import json
import string
import random

import flask
from flask import Flask, request

app = Flask(__name__)


def parse_food(food, process):
    splitted = food.split(', ')
    order = {splitted[0]: {}}
    order[splitted[0]].update({"process": process})
    for i in range(len(splitted) // 2):
        order[splitted[0]].update({splitted[2 * i + 1]: int(splitted[2 * i + 2])})
    return order


def parse_new_food(food):
    splitted = food.split(', ')
    order = {}
    for i in range(len(splitted) // 2):
        order.update({splitted[2 * i]: int(splitted[2 * i + 1])})
    return order


def login(test):
    password = ''
    with open("password.txt", "r") as file_name:
        for line in file_name:
            password = line
    if str(test) == password:
        return True
    else:
        return False


@app.route('/')
def start_page():
    text1 = """<p> Shop! </p>
    <p> Commands: </p>
    <p> 1. <a   href="http://127.0.0.1:5000/offers" > /offers </a> - show food and offers   </p>
    <p> 2. <a  href="http://127.0.0.1:5000/check" > /check </a> - check your order </p>
    <p> 3. <a  href="http://127.0.0.1:5000/add" > /add </a> - add food to shop (admin only) </p>
    <p> 4. <a  href="http://127.0.0.1:5000/show_orders" >/show_orders </a> - show all orders (admin only) </p>
    <p> 5. <a  href="http://127.0.0.1:5000/change_status" >/change_status </a> - change status order's id (admin only) </p>
    <p> 6. <a  href="http://127.0.0.1:5000/change_password" >/change_password </a> - change password (admin only) </p>
    """
    return str(text1)


@app.route('/offers/', methods=['GET', 'POST'])
def get_offer():
    with open("data_file.json", "r") as read_file:
        data = json.load(read_file)
        text = ""
        for i in data:
            text = " ".join([text, "<p>", str(i), str(data[i]), "$", "</p>"])
        text = " ".join([text, """<form method="POST">
        Your order in format (Name, food, amount, food2, amount...) :<br>
        <input type="text" name="tag"><br>
        <input type="submit" value="order">
        </form>"""])
        if request.method == 'POST':
            tag = request.form['tag']
            current_order = parse_food(tag, "In process")
            with open("offers.json", "r") as reading_file:
                orders = json.load(reading_file)
                orders.update(current_order)
            with open("offers.json", "w") as writing_file:
                json.dump(orders, writing_file, indent=2)
    text = " ".join([text, '<p> <a   href= "http://127.0.0.1:5000/" > Go back </a> </p> '])
    return text


@app.route('/check/', methods=['GET', 'POST'])
def checking():
    text = """<form method="POST">
            Your name :<br>
            <input type="text" name="tag"><br>
            <input type="submit" value="check">
            </form>"""
    if request.method == 'POST':
        tag = request.form['tag']
        with open("offers.json", "r") as reading_file:
            orders = json.load(reading_file)
        if tag in orders:
            status = orders[tag]["process"]
        else:
            status = "No orders!"
        text = " ".join([text, status])
    text = " ".join([text, '<p> <a   href= "http://127.0.0.1:5000/" > Go back </a> </p> '])
    return text


@app.route('/add/', methods=['GET', 'POST'])
def add():
    text = """<form method="post">
        <p>
	    <label for="password">Password</label> <br>
	    <input type="pswrd" name="password"> 
	 </p>
	    <label for="food">New food in format(Food1, cost1, ..) </label> <br>
	    <input type="food" name="new_food"> <br>
	     <input type="submit" value="add">
    </form>"""
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text = " ".join([text, '<p> Access denied! </p>'])
        else:
            food = request.form.get('new_food')
            new_food = parse_new_food(food)
            with open("data_file.json", "r") as reading_file:
                orders = json.load(reading_file)
                orders.update(new_food)
            with open("data_file.json", "w") as writing_file:
                json.dump(orders, writing_file, indent=2)
            text = " ".join([text, '<p> Added! </p>'])
    text = " ".join([text, '<p> <a   href= "http://127.0.0.1:5000/" > Go back </a> </p> '])
    return text


@app.route('/show_orders/', methods=['GET', 'POST'])
def show_orders():
    text = """<form method="post">
    	    <label for="password">Password</label> <br>
	    <input type="pswrd" name="password">  <br>
    	     <input type="submit" value="check">
        </form>"""
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text = " ".join([text, '<p> Access denied! </p>'])
        else:
            with open("offers.json", "r") as read_file:
                data = json.load(read_file)
                for i in data:
                    text = " ".join([text, "<p>", str(i), ":"])
                    for j in data[i]:
                        if j == "process":
                            text = " ".join([text, str(j), "-", str(data[i][j])])
                        else:
                            text = " ".join([text, ",", str(j), str(data[i][j]), "pieces"])
                    text = " ".join([text, "</p>"])
    text = " ".join([text, '<p> <a   href= "http://127.0.0.1:5000/" > Go back </a> </p> '])
    return text


@app.route('/change_status/', methods=['GET', 'POST'])
def change_status():
    text = """<form method="post">
            <p>
    	    <label for="password">Password</label> <br>
    	    <input type="pswrd" name="password"> 
    	 </p>
    	    <label for="change">Changes in format(Name1, change1, ..) </label> <br>
    	    <input type="change" name="changes"> <br>
    	     <input type="submit" value="change">
        </form>"""
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text = " ".join([text, '<p> Access denied! </p>'])
        else:
            input = request.form.get("changes")
            splitted = input.split(', ')
            with open("offers.json", "r") as reading_file:
                orders = json.load(reading_file)
            if splitted[0] in orders:
                order = orders[splitted[0]]
                order["process"] = splitted[1]
                orders[splitted[0]].update(order)
                with open("offers.json", "w") as writing_file:
                    json.dump(orders, writing_file, indent=2)
                text = " ".join([text, '<p>  Changed! </p>'])
            else:
                text = " ".join([text, '<p>  Not found! </p>'])
    text = " ".join([text, '<p> <a   href= "http://127.0.0.1:5000/" > Go back </a> </p> '])
    return text

@app.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    text = """<form method="post">
                <p>
        	    <label for="password">Old password</label> <br>
        	    <input type="pswrd" name="password"> 
        	 </p>
        	    <label for="change">New password </label> <br>
        	    <input type="change" name="password2"> <br>
        	     <input type="submit" value="change">
            </form>"""
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text = " ".join([text, '<p> Access denied! </p>'])
        else:
            password2 = request.form.get("password2")
            with open("password.txt", "w") as writing_lines:
                writing_lines.write(password2)
            text = " ".join([text, '<p> Changed! </p>'])
    text = " ".join([text, '<p> <a   href= "http://127.0.0.1:5000/" > Go back </a> </p> '])
    return text




if __name__ == '__main__':
    app.run(debug=True)
