adress = "localhost"

port = 5000

start_reference = f"http://{adress}:{port}"

go_back = f'<p> <a   href= "{start_reference}" > Go back </a> </p> '

startpage = f"""<p> <strong> Shop! </strong> </p>
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

offer_form = "Your order in format (Name, food, amount, food2, amount...) :"

check_form = "Your name :"

in_process = "In process"

add_form = "New food in format(Food1, cost1, ..) "

name_process = "process"


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


offers_page = '/offers/'

order = "order"

current_tag = "tag"

check = "check"

no_order = "No orders!"

check_page = '/check/'

change = "change"

add_page = '/add/'

Password = "Password"

add = "add"

check = "check"

no_access = '<p> Access denied! </p>'

pieces = "pieces"

show_page = '/show_orders/'

change_order_page = '/change_status/'

change_password_page = '/change_password/'

changes_form = "Changes in format(Name1, change1, ..) "

not_found = '<p>  Not found! </p>'

changed = '<p>  Changed! </p>'

new_password = "New password"

old_pass = "Old password"

food_update = "new_food"
