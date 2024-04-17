from flask import Flask, request, jsonify, render_template
import google.generativeai as genai


app = Flask(__name__)

# Set your API key
genai.configure(api_key="AIzaSyAtCY_9Guak894u4O_3vXksvG_-IuUDNjc")


@app.route('/')
def home():
    return render_template('page2.html')


@app.route('/upload')
def page3():
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

        # Extract the summary text from the response
        summary_text = response.text

        # Return the summary
        return jsonify({'summary': summary_text}), 200

    except Exception as e:
        # Print the exception for debugging
        print("Error:", e)
        # Handle other unexpected errors
        return jsonify({'error': 'Unexpected error occurred: {}'.format(str(e))}), 500


if __name__ == '__main__':
    app.run(debug=True)
