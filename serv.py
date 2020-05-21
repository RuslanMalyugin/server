import json
from flask import Flask, request

app = Flask("Shesterochka")

adress = "localhost"

port = 5000

start_reference = f"http://{adress}:{port}"

go_back = f'<p> <a   href= "{start_reference}" > Go back </a> </p> '


def read_json(json_name):
    with open(json_name, "r") as reading_file:
        return json.load(reading_file)


def write_json(json_name, new_items):
    with open(json_name, "w") as writing_file:
        json.dump(new_items, writing_file, indent=2)


def parse_food(food, process):
    splitted = food.split(', ')
    order = {splitted[0]: {}}
    order[splitted[0]].update({"process": process})
    for i in range(len(splitted) // 2):
        order[splitted[0]].update({splitted[2 * i + 1]: int(splitted[2 * i + 2])})
    return order


def unique_form(is_double, first_text, button, first_tag, second_text, second_tag):
    form = list()
    form.append(f"""<form method="post">
    <p>
    <label for="first_label">{first_text}</label> <br>
    <input type="first" name={first_tag}>
    </p>""")
    if is_double:
        form.append(f""" <label for="second_label">{second_text}</label> <br>
    <input type="second" name={second_tag}> <br>""")
    form.append(f"""<input type="submit" value={button}>
    </form>""")
    return " ".join(tuple(form))


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
    text1 = f"""<p> <strong> Shop! </strong> </p>
    <p> <strong> Commands: </strong> </p>
    <ol>
    <li> <a  href="{start_reference}/offers" > /offers </a> - show food and offers   </li>
    <li> <a  href="{start_reference}/check/" > /check </a> - check your order </li>
    <li> <a  href="{start_reference}/add/" > /add </a> - add food to shop (admin only) </li>
    <li> <a  href="{start_reference}/show_orders/" >/show_orders </a> - show all orders (admin only) </li>
    <li> <a  href="{start_reference}/change_status/" >/change_status </a> 
                                                        - change status order's id (admin only) </pli>
    <li> <a  href="{start_reference}/change_password/" >/change_password </a> - change password (admin only) </li>
    </ol>
    """
    return text1


@app.route('/offers/', methods=['POST', 'GET'])
def get_offer():
    text = list()
    data = read_json("data_file.json")
    for i in data:
        text.extend(["<p>", str(i), str(data[i]), "$", "</p>"])
    text.append(
        unique_form(False, "Your order in format (Name, food, amount, food2, amount...) :", "order", "tag", " ", ""))
    if request.method == 'POST':
        tag = request.form['tag']
        current_order = parse_food(tag, "In process")
        orders = read_json("offers.json")
        orders.update(current_order)
        write_json("offers.json", orders)
    text.append(go_back)
    return " ".join(tuple(text))


@app.route('/check/', methods=['POST', 'GET'])
def checking():
    text = list()
    text.append(unique_form(False, "Your name :", "check", "tag", " ", " "))
    if request.method == 'POST':
        tag = request.form['tag']
        orders = read_json("offers.json")
        if tag in orders:
            status = orders[tag]["process"]
        else:
            status = "No orders!"
        text.append(status)
    text.append(go_back)
    return " ".join(tuple(text))


@app.route('/add/', methods=['POST', 'GET'])
def add():
    text = list()
    text.append(unique_form(True, "Password", "add", "password", "New food in format(Food1, cost1, ..) ", "new_food"))
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text.append('<p> Access denied! </p>')
        else:
            food = request.form.get('new_food')
            new_food = parse_new_food(food)
            orders = read_json("data_file.json")
            orders.update(new_food)
            write_json("data_file.json", orders)
            text.append('<p> Added! </p>')
    text.append(go_back)
    return " ".join(tuple(text))


@app.route('/show_orders/', methods=['POST', 'GET'])
def show_orders():
    text = list()
    text.append(unique_form(False, "Password", "check", "tag", " ", " "))
    if request.method == 'POST':
        password = request.form["tag"]
        if not login(password):
            text.append('<p> Access denied! </p>')
        else:
            data = read_json("offers.json")
            for i in data:
                text.extend(["<p>", str(i), ":"])
                for j in data[i]:
                    if j == "process":
                        text.extend([str(j), "-", str(data[i][j])])
                    else:
                        text.extend([",", str(j), str(data[i][j]), "pieces"])
                text.append("</p>")
    text.append(go_back)
    return " ".join(tuple(text))


@app.route('/change_status/', methods=['POST', 'GET'])
def change_status():
    text = list()
    text.append(
        unique_form(True, "Password", "change", "password", "Changes in format(Name1, change1, ..) ", "changes"))
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text.append('<p> Access denied! </p>')
        else:
            input = request.form.get("changes")
            splitted = input.split(', ')
            orders = read_json("offers.json")
            if splitted[0] in orders:
                order = orders[splitted[0]]
                order["process"] = splitted[1]
                orders[splitted[0]].update(order)
                write_json("offers.json", orders)
                text.append('<p>  Changed! </p>')
            else:
                text.append('<p>  Not found! </p>')
    text.append(go_back)
    return " ".join(tuple(text))


@app.route('/change_password/', methods=['POST', 'GET'])
def change_password():
    text = list()
    text.append(unique_form(True, "Old password", "change", "password", "New password", "password2"))
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text.append('<p> Access denied! </p>')
        else:
            password2 = request.form.get("password2")
            with open("password.txt", "w") as writing_lines:
                writing_lines.write(password2)
            text.append('<p> Changed! </p>')
    text.append(go_back)
    return " ".join(tuple(text))


if __name__ == '__main__':
    app.run(adress, port=port, debug=True)
