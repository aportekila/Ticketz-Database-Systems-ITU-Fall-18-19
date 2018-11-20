from flask import render_template, current_app, redirect, url_for, request


from tables import Hotel
from dboperations import Database

db = Database()

hotel_db = db.hotel


def home_page():
    hotels = hotel_db.get_hotels()
    return render_template("admin_home_page.html", hotels = reversed(hotels))

def admin_home_page():
    hotels = hotel_db.get_hotels()
    #print(hotels)
    return render_template("admin_home_page.html", hotels = reversed(hotels))

def add_hotel_page():
    return render_template("add_hotel.html")

def login_page(request):
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin_home_page'))
    return render_template('login.html')

def hotel_page(id):
    temp_hotel = hotel_db.get_hotel(id)
    if temp_hotel is None:
        return render_template("404_not_found.html")
    else:
        return render_template("hotels.html", hotel = temp_hotel)

def driver_list_page(id):
    return render_template("driver/driver_list.html")

def driver_profile_page(id):
    return render_template("driver/driver_profile.html")

def driver_edit_page(id):
    return render_template("driver/driver_edit.html")

def firms_page(id):
    return render_template("firms.html")