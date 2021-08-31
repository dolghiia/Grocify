#-----------------------------------Grocify------------------------------------#
Author: Alexander D.
Last Updated: June 2, 2021

About:
Grocify is designed to be a virtual grocery list, allowing one to access it
on one's local network. You can view your grocery list, save it as a .txt file,
or reset it anytime you want. Even if you close the application, your grocery
list will still be the same upon startup.

Installation Requirements:
-Python 3.8 or later
-Python Flask 1.1.2 or later
-Flask-WTF 0.15.1 or later

Features:
-Run on any device on the same network
    As long as the device is connected to the same network as the device the
    application is run on, you can run it! Example: Accessing Grocify on your
    phone while running the application on your laptop.
-Add items to your grocery list
    Just fill out the form with the correct information, and your item will be
    added to the list!
-View your grocery list
    You can view your all the items in your grocery list as well as the total
    price and how many items there are in all.
- Save your Grocery list
    When you've finished adding all your items to your list, your can save it
    as a text file! After that, you can reset the current list on Grocify so you
    are ready for next week.

How to run:
1. Ensure all requirements are met and that all files are in their corresponding
folders.
2. Run 'app.py'.
3. You can now access Grocify on 'localhost:5000'. Note: If you would like to
run it on other devices (your phone), you have to set the route to the ip
address of the device you are running it on (See Python Flask Documentation).
4. If successful, you can now access Grocify and create your own grocery lists!

Additional Files:
-add.png
-carticon.png
-grocery_list.txt
-save.png
-styles.css
-create.html
-home.html
-view.html
-layout.html
#------------------------------------------------------------------------------#
