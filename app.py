from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mani@1911',  # Update this with your MySQL password
        database='food_ordering'
    )
    return connection

# Home route displaying the menu
@app.route('/menu')
def menu():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, description, price, image_url FROM menu_items")
    menu_items = cursor.fetchall()  # Retrieve all the rows with image URL
    cursor.close()
    connection.close()
    return render_template('index.html', menu_items=menu_items)  # Pass the items with image URLs

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT id, name, description, price, image_url FROM menu_items')
    menu_items = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', menu_items=menu_items)

# Add menu item route
@app.route('/add', methods=['GET', 'POST'])
def add_menu_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image_url = request.form['image_url']  # Get the image URL from the form (assuming image URL input)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO menu_items (name, description, price, image_url) VALUES (%s, %s, %s, %s)',
                       (name, description, price, image_url))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    
    return render_template('add_menu_item.html')

# Delete menu item route
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_menu_item(item_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM menu_items WHERE id = %s', (item_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
