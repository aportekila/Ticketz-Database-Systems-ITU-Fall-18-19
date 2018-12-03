from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import views
from base64 import b64encode
from dao.user_dao import UserDao
from DBOP.tables.image_table import Image
from DBOP.tables.hotel_table import Hotel
from DBOP.tables.expedition_table import Expedition
from DBOP.hotel_db import hotel_database
from DBOP.image_db import image_database
from DBOP.expedition_db import expedition_database
from DBOP.vehicles_db import vehicle_database

db_hotel = hotel_database()
db_image = image_database()
db_expedition = expedition_database()
db_vehicle = vehicle_database()

hotel_db = db_hotel.hotel
image_db = db_image.image
expedition_db = db_expedition.expedition
vehicle_db = db_vehicle.vehicle
userop = UserDao()

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    return app

app = create_app()

app.secret_key = b'_5#y2L"F4Q8z_^?4c]/'


@app.route('/admin_home_page', methods=['GET', 'POST'])
def admin_home_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.admin_home_page()
    else:
        return unAuth403()

@app.route('/search_hotel/<string:text>', methods=['GET', 'POST'])
def search_hotel(text):
    return views.search_hotel_page(text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return views.login_page(request)

@app.route('/admin/add_hotel', methods=['GET', 'POST'])
def add_hotel_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        if request.method == "GET":
            return views.add_hotel_page()
        else:
            hotel_name = request.form["hotel_name"]
            email = request.form["e_mail"]
            description = request.form["description"]
            city = request.form["city"]
            address = request.form["address"]
            phone = request.form["phone"]
            website = request.form["website"]
            if "logo" in request.files:
                logo = request.files["logo"]
                hotel_db.add_hotel_with_logo(Hotel(hotel_name, email, description, city, address, phone, website, logo.read()))
            else:
                hotel_db.add_hotel(Hotel(hotel_name, email, description, city, address, phone, website, None))

            s = request.form["s"]

            (temp_id, ) = hotel_db.get_hotel_id(Hotel(hotel_name, email, description, city, address, phone, website, None))

            uploaded_files = request.form.getlist("file[]")
            for i in range(int(s) + 1):
                temp = "image" + str(i)
                if temp in request.files:
                    file = request.files[temp]
                    image_db.add_image(Image(temp_id, file.read()))

            return redirect(url_for('admin_home_page'))
    else:
        return unAuth403()

@app.route('/admin/edit_hotel/<int:id>', methods=['GET', 'POST'])
def edit_hotel_page(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    print(user)
    if user and user[-1]:
        if request.method == "GET":
            return views.edit_hotel_page(id)
        else:
            hotel_name = request.form["hotel_name"]
            email = request.form["e_mail"]
            description = request.form["description"]
            city = request.form["city"]
            address = request.form["address"]
            phone = request.form["phone"]
            website = request.form["website"]
            if "logo" in request.files:
                logo = request.files["logo"]
                hotel_db.update_hotel_with_logo(id, Hotel(hotel_name, email, description, city, address, phone, website, logo.read()))
            else:
                hotel_db.update_hotel(id, Hotel(hotel_name, email, description, city, address, phone, website, None))
            s = request.form["s"]
            uploaded_files = request.form.getlist("file[]")
            for i in range(int(s) + 1):
                temp = "image" + str(i)
                if temp in request.files:
                    file = request.files[temp]
                    image_db.add_image(Image(id, file.read()))

            return redirect(url_for('admin_home_page'))
    else:
        return unAuth403()



@app.route('/admin/edit_hotels', methods=['GET', 'POST'])
def edit_hotels_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.edit_hotels_page()
    else:
        return unAuth403()

@app.route('/admin/delete_hotel/<int:id>')
def delete_hotel(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        hotel_db.delete_hotel(id)
        return redirect(url_for('edit_hotels_page'))
    else:
        return unAuth403()



@app.route('/admin/delete_image/<int:hotel_id>/<int:image_id>')
def delete_image(hotel_id, image_id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        image_db.delete_image(hotel_id, image_id)
        return redirect(url_for('edit_hotel_page', id=hotel_id))
    else:
        return unAuth403()


@app.route('/admin/delete_logo/<int:hotel_id>')
def delete_hotel_logo(hotel_id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        hotel_db.delete_hotel_logo(hotel_id)
        return redirect(url_for('edit_hotel_page', id=hotel_id))
    else:
        return unAuth403()



@app.route('/hotels/<int:id>', methods=['GET', 'POST'])
def hotel_page(id):
    return views.hotel_page(id)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return views.home_page()

@app.route('/firm/<int:id>', methods=['GET', 'POST'])
def firms_page(id):
    return views.firms_page(id)

@app.route('/firm/login', methods=['GET', 'POST'])
def firms_login():
    return views.firm_login(request)

@app.route('/firm/driver_list/<int:id>', methods=['GET', 'POST'])
def driver_list_page(id):
    return views.driver_list_page(id)

@app.route('/firm/driver_profile/<int:id>', methods=['GET', 'POST'])
def driver_profile_page(id):
    return views.driver_profile_page(id)

@app.route('/firm/driver_edit/<int:id>', methods=['GET', 'POST'])
def driver_edit_page(id):
    return views.driver_edit_page(id)

@app.route('/firm/add_expedition', methods=['GET', 'POST'])
def add_expedition():
    firm_id = session.get("firm_id")
    if firm_id != None:
        if request.method == "GET":
            return views.add_expedition()
        else:
            from_ = request.form["from"]
            from_ter = request.form["from_ter"]
            to = request.form["to"]
            to_ter = request.form["to_ter"]
            dep_time = request.form["dep_time"]
            arr_time = request.form["arr_time"]
            date = request.form["date"]
            price = request.form["price"]
            plane = request.form["selected_plane"]
            vehicle = vehicle_db.get_vehicle(plane)
            total_cap = vehicle.capacity
            driver_id  = request.form["driver"]
            if "document" in request.files:
                document = request.files["document"]
                expedition_db.add_expedition_with_document(Expedition(from_, from_ter, to, to_ter, dep_time, arr_time, date, price, plane, driver_id, firm_id, total_cap, 0, document.read()))

            else:
                expedition_db.add_expedition(Expedition(from_, from_ter, to, to_ter, dep_time, arr_time, date, price, plane, driver_id, firm_id, total_cap, 0,  None ))

            return redirect(url_for('firms_page', id=firm_id))
    else:
        return unAuth403()



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return views.signup_page()


@app.route('/403')
def unAuth403():
    return "un authorized"


if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
