from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import json
import re


app = Flask(__name__)
sslify = SSLify(app)

# token = 'private'
URL = 'https://api.telegram.org/bot' + token + '/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def send_message(chat_id, text='Hello.'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id,
              'text': text}
    response = requests.post(url, json=answer)
    return response.json()


def parce_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]


def get_percent_change_one_hour(crypto):
    url = 'https://api.coinmarketcap.com/v1/ticker/{}'.format(crypto)
    response = requests.get(url).json()
    percent_change_1h = response[-1]['percent_change_1h']
    percent_change_1h = format(float(response[-1]['percent_change_1h']), '.2f')
    return str(percent_change_1h) + '%'


def get_percent_change_24_hours(crypto):
    url = 'https://api.coinmarketcap.com/v1/ticker/{}'.format(crypto)
    response = requests.get(url).json()
    percent_change_24h = response[-1]['percent_change_24h']
    percent_change_24h = format(
        float(response[-1]['percent_change_24h']), '.2f')
    return str(percent_change_24h) + '%'


def get_percent_change_7_days(crypto):
    url = 'https://api.coinmarketcap.com/v1/ticker/{}'.format(crypto)
    response = requests.get(url).json()
    percent_change_7d = response[-1]['percent_change_7d']
    percent_change_7d = format(float(response[-1]['percent_change_7d']), '.2f')
    return str(percent_change_7d) + '%'


def get_price(crypto):
    url = 'https://api.coinmarketcap.com/v1/ticker/{}'.format(crypto)
    response = requests.get(url).json()
    price = response[-1]['price_usd']
    # write_json(response, filename='price.json')
    price = format(float(response[-1]['price_usd']), '.2f')
    return str(price) + ' usd'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.get_json()
        chat_id = response['message']['chat']['id']
        message = response['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
            price = get_price(parce_text(message))
            one_hour = get_percent_change_one_hour(parce_text(message))
            one_day = get_percent_change_24_hours(parce_text(message))
            one_week = get_percent_change_7_days(parce_text(message))
            f_price = f"Current price of {parce_text(message).upper()} is: {price}\n\n"
            f_hour = f"Percent change in 1H:  {one_hour}\n\n"
            f_day = f"Percent change in 24H:  {one_day}\n\n"
            f_week = f"Percent change in 7 days:  {one_week}"
            send_message(chat_id, text=f_price + f_hour + f_day + f_week)
        else:
            invalid_msg = 'Have you already read how to search interested token?\nExample: /bitcoin'
            send_message(chat_id, text=invalid_msg)
        # write_json(response)
        return jsonify(response)
    return '<h1>Bot welcomes you.</h1>'


# https://api.telegram.org/botprivate/setWebhook?url=https://ostegura88.pythonanywhere.com/


# def main():
#     # response = requests.get(URL + 'getMe')
#     # write_json(response.json())
#     # response = get_updates()
#     # get_updates()
#     # chat_id = response['result'][-1]['message']['chat']['id']
#     # send_message(chat_id)
#     pass


if __name__ == '__main__':
    app.run()
    # main()
