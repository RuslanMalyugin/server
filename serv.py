import json

from flask import Flask, request

app = Flask("Shesterochka")

adress = "localhost"
port = 5000


def parse_food(food, process):
    splitted = food.split(', ')
    order = {splitted[0]: {}}
    order[splitted[0]].update({"process": process})
    for i in range(len(splitted) // 2):
        order[splitted[0]].update({splitted[2 * i + 1]: int(splitted[2 * i + 2])})
    return order


def single_form(upper_text, button, tag):
    return f"""<form method="POST">
            {upper_text}<br>
            <input type="text" name={tag}><br>
            <input type="submit" value={button}>
            </form>"""


def double_form(first_text, button, first_tag, second_text, second_tag):
    return f"""<form method="post">
        <p>
	    <label for="first_label">{first_text}</label> <br>
	    <input type="first" name={first_tag}> 
	 </p>
	    <label for="second_label">{second_text}</label> <br>
	    <input type="second" name={second_tag}> <br>
	     <input type="submit" value={button}>
    </form>"""


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
    text1 = f"""<p> Shop! </p>
    <p> Commands: </p>
    <p> 1. <a   href="http://{adress}:{port}/offers" > /offers </a> - show food and offers   </p>
    <p> 2. <a  href="http://{adress}:{port}/check" > /check </a> - check your order </p>
    <p> 3. <a  href="http://{adress}:{port}/add" > /add </a> - add food to shop (admin only) </p>
    <p> 4. <a  href="http://{adress}:{port}/show_orders" >/show_orders </a> - show all orders (admin only) </p>
    <p> 5. <a  href="http://{adress}:{port}/change_status" >/change_status </a> - change status order's id (admin only) </p>
    <p> 6. <a  href="http://{adress}:{port}/change_password" >/change_password </a> - change password (admin only) </p>
    """
    return str(text1)


@app.route('/offers/', methods=['GET', 'POST'])
def get_offer():
    with open("data_file.json", "r") as read_file:
        data = json.load(read_file)
        text = ""
        for i in data:
            text = " ".join([text, "<p>", str(i), str(data[i]), "$", "</p>"])
        text = " ".join(
            [text, single_form("Your order in format (Name, food, amount, food2, amount...) :", "order", "tag")])
        if request.method == 'POST':
            tag = request.form['tag']
            current_order = parse_food(tag, "In process")
            with open("offers.json", "r") as reading_file:
                orders = json.load(reading_file)
                orders.update(current_order)
            with open("offers.json", "w") as writing_file:
                json.dump(orders, writing_file, indent=2)
    text = " ".join([text, f'<p> <a   href= "http://{adress}:{port}" > Go back </a> </p> '])
    return text


@app.route('/check/', methods=['GET', 'POST'])
def checking():
    text = single_form("Your name :", "check", "tag")
    if request.method == 'POST':
        tag = request.form['tag']
        with open("offers.json", "r") as reading_file:
            orders = json.load(reading_file)
        if tag in orders:
            status = orders[tag]["process"]
        else:
            status = "No orders!"
        text = " ".join([text, status])
    text = " ".join([text, f'<p> <a   href= "http://{adress}:{port}" > Go back </a> </p> '])
    return text


@app.route('/add/', methods=['GET', 'POST'])
def add():
    text = double_form("Password", "add", "password", "New food in format(Food1, cost1, ..) ", "new_food")
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
    text = " ".join([text, f'<p> <a   href= "http://{adress}:{port}" > Go back </a> </p> '])
    return text


@app.route('/show_orders/', methods=['GET', 'POST'])
def show_orders():
    text = single_form("Password", "check", "tag")
    if request.method == 'POST':
        password = request.form["tag"]
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
    text = " ".join([text, f'<p> <a   href= "http://{adress}:{port}" > Go back </a> </p> '])
    return text


@app.route('/change_status/', methods=['GET', 'POST'])
def change_status():
    text = double_form("Password", "change", "password", "Changes in format(Name1, change1, ..) ", "changes")
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
    text = " ".join([text, f'<p> <a   href= "http://{adress}:{port}" > Go back </a> </p> '])
    return text


@app.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    text = double_form("Old password", "change", "password", "New password", "password2")
    if request.method == 'POST':
        password = request.form.get("password")
        if not login(password):
            text = " ".join([text, '<p> Access denied! </p>'])
        else:
            password2 = request.form.get("password2")
            with open("password.txt", "w") as writing_lines:
                writing_lines.write(password2)
            text = " ".join([text, '<p> Changed! </p>'])
    text = " ".join([text, f'<p> <a   href= "http://{adress}:{port}" > Go back </a> </p> '])
    return text


if __name__ == '__main__':
    app.run(adress, port=port, debug=True)
