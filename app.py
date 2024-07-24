from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bot_token = request.form['bot_token']
        return redirect(url_for('get_chat_id', bot_token=bot_token))
    return render_template('index.html')

@app.route('/get_chat_id/<bot_token>', methods=['GET'])
def get_chat_id(bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json()
        if 'result' in updates and len(updates['result']) > 0:
            chat_id = updates['result'][0]['message']['chat']['id']
            return render_template('result.html', chat_id=chat_id, updates=updates)
        else:
            return "No updates found or the bot hasn't received any messages yet."
    else:
        return "Invalid Bot Token or Network Error."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
