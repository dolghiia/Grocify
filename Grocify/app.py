from flask import Flask, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '6907baee897e17fe27788b5215e8c2bf'

FILE_NAME = os.path.abspath('./static/grocery_list.txt')
grocery_items = []


# -------------Form Classes----------------------- #


class CreateForm(FlaskForm):
    """
    Collects and verifies user input to add to grocery list data.

    ===Parameters===
    item_name: Represents field that stores info about the name of the item
    item_price: Represents field that stores info about the price of the item
    item_quantity: Represents field that stores info about the quantity of the item
    add_item: Field that confirms whether item will be added into the list
    """
    item_name = StringField('', validators=[DataRequired(), Length(max=28)])
    item_price = DecimalField('', validators=[DataRequired(),
                                              NumberRange(min=0)], places=2)
    item_quantity = IntegerField('', validators=[DataRequired(),
                                                 NumberRange(min=1)])
    add_item = SubmitField('Add')


class ResetForm(FlaskForm):
    """
    Form which allows user to reset the current grocery list.

    ===Parameters===
    reset_list: Field that confirms if the current grocery list should be reset
    """
    reset_list = SubmitField('Reset')


# -------------Grocery List Functions------------- #


def read_list() -> None:
    """
    On startup, this is called to restore past grocery list data. Reads
    'grocery_list.txt' to determine items that were already added to the list
    and updates list accordingly.

    ===Parameters===
    None
    """
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
    del(lines[:5])
    for line in lines:
        if line.count('-') == 64:
            break
        name, quantity, price = line[1:30], line[32:47], line[49:65]
        name, quantity, price = name.strip(' '), quantity.strip(' '), \
                                price.strip(' ')
        price = float(price)
        if float(price) - int(price) == 0:
            price = int(price)
        grocery_items.append({'Name': name, 'Price': price,
                              'Quantity': int(quantity)})


def write_list(items: dict, t_pri: int, t_quant: int) -> None:
    """
    Writes/updates current grocery list according to data stored in items.

    ===Parameters===
    items: List of dicts containing info on each item in grocery list
    t_pri: int representing total price of all items in grocery list
    t_quant: int representing total quantity of all items in grocery list
    """
    with open(FILE_NAME, 'r') as f:
        lines = f.readlines()
    with open(FILE_NAME, 'w') as f:
        new_lines = lines[:5]
        for item in items:
            curr_line = '| ' + item['Name'] + (' ' * (27 - len(item['Name']))) +\
                        ' | ' + str(item['Quantity']) + \
                        (' ' * (14 - len(str(item['Quantity'])))) + ' | ' + \
                        str(item['Price']) + (' ' * (15 - len(str(item['Price'])))) + ' |\n'
            new_lines.append(curr_line)
        lines[-2] = '|' + (' ' * 29) + '| Total: ' + str(t_quant) +\
                    (' ' * (7 - len(str(t_quant)))) + ' | Total: ' + str(t_pri) +\
                    (' ' * (8 - len(str(t_pri)))) + ' |\n'
        new_lines.extend([lines[-3], lines[-2], lines[-1]])
        f.writelines(new_lines)


def update_items(items: list, new_item: list) -> None:
    """
    Updates items to reflect changes to grocery list.

    ===Parameters===
    items: List of dicts containing info on each item in grocery list
    new_item: List of data that represents new addition to grocery list
    """
    match = False
    new_item[1] = float(new_item[1])
    if float(new_item[1]) - int(new_item[1]) == 0:
        new_item[1] = int(new_item[1])
    total_price, total_quantity = new_item[1], new_item[2]
    for item in items:
        total_price, total_quantity = total_price + item['Price'], \
                                      total_quantity + item['Quantity']
        if item['Name'] == new_item[0]:
            item['Price'] += new_item[1]
            item['Quantity'] += new_item[2]
            match = True
    if not match:
        items.append({'Name': new_item[0], 'Price': new_item[1],
                      'Quantity': new_item[2]})
        print(items)
    write_list(items, total_price, total_quantity)


# -------------Web Page Routes-------------------- #


@app.route('/')
@app.route('/home')
def home() -> None:
    """
    Displays the 'home' page of the website.
    """
    return render_template('home.html')


@app.route('/create', methods=["GET", "POST"])
def create() -> None:
    """
    Displays the 'create' page of the website. Allows user to add new items to
    their grocery list. The user can also view, save, or reset their grocery
    list from this page.
    """
    form = CreateForm()
    reset_form = ResetForm()
    if form.validate_on_submit() and form.add_item.data:
        flash(f'{form.item_name.data} has been added to your grocery list!',
              'success')
        price = round(form.item_price.data, 2)
        curr_item = [form.item_name.data, price, form.item_quantity.data]
        update_items(grocery_items, curr_item)
    elif reset_form.validate_on_submit() and reset_form.reset_list.data:
        flash('Your grocery list was reset!', 'success')
        del(grocery_items[:])
        write_list({}, 0, 0)
    return render_template('create.html', form=form, reset_form=reset_form)


@app.route('/view')
def view() -> None:
    """
    Displays the 'view' page of the website. This page allows the user to view
    their grocery list, updating when they add a new item to the list.
    """
    t_price, t_quantity = 0, 0
    for item in grocery_items:
        t_price, t_quantity = t_price + item['Price'], \
                              t_quantity + item['Quantity']
    t_price, t_quantity = str(t_price), str(t_quantity)
    return render_template('view.html', grocery_items=grocery_items,
                           t_price=t_price, t_quantity=t_quantity)


# -------------Main Program----------------------- #


read_list()

if __name__ == '__main__':
    app.run()
