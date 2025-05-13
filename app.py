from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Home route to render the page
@app.route('/')
def home():
    return render_template('chatbot.html')

# Route for handling appeal submission
@app.route('/submit_appeal', methods=['POST'])
def submit_appeal():
    # Get data from the form
    application_id = request.form.get('applicationId')
    appeal_reason = request.form.get('appealReason')
    
    if application_id and appeal_reason:
        # Process the appeal (For now, we'll simulate it)
        response = {"status": "success", "message": "Appeal submitted successfully!"}
    else:
        response = {"status": "error", "message": "Please fill all fields!"}
    
    return jsonify(response)

# Route for chatbot response (Simulating chatbot's response)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    
    # Define responses based on the user's input
    if "renew" in user_input.lower():
        reply = "To renew your license, click 'Renew Now'."
    elif "appeal" in user_input.lower():
        reply = "You can appeal by filling the form below."
    elif "status" in user_input.lower():
        reply = "Check your application status in the dashboard."
    else:
        reply = "I'm sorry, I don't understand. Please contact support for further assistance."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
