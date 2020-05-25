import json
from flask import Flask, request
from config import *


app = Flask("Shesterochka")


def read_json(json_name):
    with open(json_name, "r") as reading_file:
        return json.load(reading_file)


def write_json(json_name, new_items):
    with open(json_name, "w") as writing_file:
        json.dump(new_items, writing_file, indent=2)


def parse_food(food, process):
    splitted = food.split(', ')
    order = {splitted[0]: {}}
    order[splitted[0]].update({name_process: process})
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
    with open("password.txt", "r") as file_name:
        password = file_name.read()
    return str(test) == password


@app.route('/')
def start_page():
    return startpage


@app.route(offers_page, methods=['POST', 'GET'])
def get_offer():
    text = list()
    data = read_json("data_file.json")
    for i in data:
        text.extend(["<p>", str(i), str(data[i]), "$", "</p>"])
    text.append(
        unique_form(False, offer_form, order, current_tag, " ", ""))
    if request.method == 'POST':
        tag = request.form[current_tag]
        current_order = parse_food(tag, in_process)
        orders = read_json("offers.json")
        orders.update(current_order)
        write_json("offers.json", orders)
    text.append(go_back)
    return " ".join(tuple(text))


@app.route(check_page, methods=['POST', 'GET'])
def checking():
    text = list()
    text.append(unique_form(False, check_form, check, current_tag, " ", " "))
    if request.method == 'POST':
        tag = request.form[current_tag]
        orders = read_json("offers.json")
        if tag in orders:
            status = orders[tag][name_process]
        else:
            status = no_order
        text.append(status)
    text.append(go_back)
    return " ".join(tuple(text))


@app.route(add_page, methods=['POST', 'GET'])
def add():
    text = list()
    text.append(unique_form(True, Password, add, Password, add_form, food_update))
    if request.method == 'POST':
        password = request.form.get(Password)
        if not login(password):
            text.append(no_access)
        else:
            food = request.form.get('new_food')
            new_food = parse_new_food(food)
            orders = read_json("data_file.json")
            orders.update(new_food)
            write_json("data_file.json", orders)
            text.append(changed)
    text.append(go_back)
    return " ".join(tuple(text))


@app.route(show_page, methods=['POST', 'GET'])
def show_orders():
    text = list()
    text.append(unique_form(False, Password, check, current_tag, " ", " "))
    if request.method == 'POST':
        password = request.form[current_tag]
        if not login(password):
            text.append(no_access)
        else:
            data = read_json("offers.json")
            for i in data:
                text.extend(["<p>", str(i), ":"])
                for j in data[i]:
                    if j == name_process:
                        text.extend([str(j), "-", str(data[i][j])])
                    else:
                        text.extend([",", str(j), str(data[i][j]), pieces])
                text.append("</p>")
    text.append(go_back)
    return " ".join(tuple(text))


@app.route(change_order_page, methods=['POST', 'GET'])
def change_status():
    text = list()
    text.append(
        unique_form(True, Password, change, Password, changes_form, change))
    if request.method == 'POST':
        password = request.form.get(Password)
        if not login(password):
            text.append(no_access)
        else:
            input = request.form.get(change)
            splitted = input.split(', ')
            orders = read_json("offers.json")
            if splitted[0] in orders:
                order = orders[splitted[0]]
                order[name_process] = splitted[1]
                orders[splitted[0]].update(order)
                write_json("offers.json", orders)
                text.append(changed)
            else:
                text.append(not_found)
    text.append(go_back)
    return " ".join(tuple(text))


@app.route(change_password_page, methods=['POST', 'GET'])
def change_password():
    text = list()
    text.append(unique_form(True, old_pass, change, Password, new_password, new_password))
    if request.method == 'POST':
        password = request.form.get(Password)
        if not login(password):
            text.append(no_access)
        else:
            password2 = request.form.get(new_password)
            with open("password.txt", "w") as writing_lines:
                writing_lines.write(password2)
            text.append(changed)
    text.append(go_back)
    return " ".join(tuple(text))


if __name__ == '__main__':
    app.run(adress, port=port, debug=True)
