from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YOUR GMAIL@gmail.com'
app.config['MAIL_PASSWORD'] = 'YOUR APP PASSWORD' 
app.config['MAIL_DEFAULT_SENDER'] = 'YOUR GMAIL@gmail.com'

mail = Mail(app)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        return render_template('payment.html')
    
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        msg = Message("Registration Payment Successful", recipients=[email])
        msg.body = "Dear User,\n\nYour business registration payment was successful.\n\nThank you!"
        mail.send(msg)

        return jsonify({'message': 'Payment successful and email sent.'}), 200
    except Exception as e:
        print("Email Error:", e)
        return jsonify({'error': 'Failed to send email.'}), 500


@app.route('/thankyou')
def thank_you():
    return "<h2>Thank you! Your payment was successful.</h2>"

if __name__ == '__main__':
    app.run(debug=True)
