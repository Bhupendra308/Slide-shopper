from flask import Flask, render_template, request, jsonify
from db_handler import store_booking, store_contact

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/head')
def head():
    return render_template('head.html')

@app.route('/book', methods=['POST'])
def book():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    ppt_id = data.get('pptId')
    
    # Input validation (example)
    if not name or not email or not ppt_id:
        return jsonify(success=False, message='All fields are required.')

    try:
        # Store the booking information
        store_booking(name, email, ppt_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify(success=False, message='Error storing booking.')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    # Input validation (example)
    if not name or not email or not message:
        return jsonify(success=False, message='All fields are required.')

    try:
        store_contact(name, email, message)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message='Error storing contact.')

if __name__ == '__main__':
    app.run(debug=True)
