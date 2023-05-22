import flask
from flask import send_from_directory, request


app = flask.Flask(__name__)

@app.route('/hello/<name>')
@app.route('/')
def hello_name():
    return 'Hello World!'

from helperfunction.waSendMessage import sendMessage

@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    print(request.get_data())
    message = request.form['Body']
    senderId = request.form['From'].split('+')[1]
    print(f'Message --> {message}')
    print(f'Sender id --> {senderId}')
    res = sendMessage(senderId=senderId, message=message)
    print(f'This is the response --> {res}')
    return '200'

if __name__ == '__main__':
    app.run(port=8050)
