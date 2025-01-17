import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import telegram
from telegram.ext import Updater, CommandHandler

def command_buy_sell(*args):
    server_url = args[0]
    access_key = args[1]
    secret_key = args[2]
    buy_sell = args[3]
    ord_type = args[4]
    coin = args[5][0]
    price = args[5][1]

    query = {
        'market': 'KRW-' + coin,
        'side': buy_sell,
        'price': price,
        'ord_type': ord_type,
    }

    if ord_type == "market":
        query.pop('price')
        query.update(volume=price)

    query_string = urlencode(query).encode()
    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }
    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)

    return res
