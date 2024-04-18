from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import google.generativeai as genai
from server import authenticate_user, create_user_account
import os
from dotenv import load_dotenv
from datetime import timedelta
import PIL.Image


load_dotenv()
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=3)
app.secret_key = os.getenv("secret_key")  # Set a secret key for sessions


# Set your API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('useremail')
        password = request.form.get('password')

        print(f"Received form data: username={username}, email={email}, password={password}")

        create_user = create_user_account(username, email, password)
        print(f"User creation result: {create_user}")

        if create_user:

            # Store data in the session
            session['username'] = username

            flash('Welcome to DUSH', 'info')
            return redirect(url_for('get_started'))
        else:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('home'))


@app.route('/submit_login_details', methods=['POST'])
def submit_login_details():
    username = request.form.get('username')
    password = request.form.get('password')

    # call the authenticate function and use it
    auth_result = authenticate_user(username, password)

    if "Login Successful" in auth_result:
        # Store data in the session
        session['username'] = username
        return redirect(url_for('get_started'))

    elif "Login Failed: Incorrect Password" in auth_result:
        return redirect(url_for("login_failed_incorrect_password"))
    else:
        return redirect(url_for('login_failed_user_not_found'))


@app.route('/Login_Failed_Incorrect_Password')
def login_failed_incorrect_password():
    session.pop("username", None)
    flash('Login Failed: Incorrect_Password', 'danger')
    return redirect(url_for("Home"))


@app.route('/login_failed_user_not_found')
def login_failed_user_not_found():
    session.pop("username", None)
    flash('Login Failed: User not found', 'danger')
    return redirect(url_for("Home"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash('you have logged out', 'info')
    return redirect(url_for("Home", _rnd=request.args.get("_rnd", None)))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-started')
def get_started():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('page3.html')


@app.route('/TTS')
def page4():
    return render_template('page4.html')


@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        # Get the text to summarize from the request
        data = request.json
        print("Received data:", data)  # Debugging statement
        text = data['text']
        print("Received text:", text)  # Debugging statement

        model = genai.GenerativeModel('gemini-pro')
        prompt = f"summarize this text{text}"
        response = model.generate_content(prompt)

        # print response feedback
        print(response.prompt_feedback)

        # Extract the summary text from the response
        summary_text = response.text

        # Return the summary
        return jsonify({'summary': summary_text}), 200

    except Exception as e:
        # Print the exception for debugging
        print("Error:", e)

        # Handle other unexpected errors
        return jsonify({'error': 'Unexpected error occurred: {}'.format(str(e))}), 500


@app.route('/uploadIMG', methods=['POST'])
def uploadIMG():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part'})

    img_data = request.files['image']
    img = PIL.Image.open(img_data)

    # process image genai
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    response_img = response.text

    # print response feedback
    print(response.prompt_feedback)

    return jsonify({'message': f'{response_img}'})


@app.route('/')
def root():
    return redirect(url_for('Home'))


# Add a catch-all route for handling URL not found errors
@app.errorhandler(404)
def page_not_found(e):
    return "Page not found. Please check the URL.", 404


if __name__ == '__main__':
    app.run(debug=True)
