import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate(
    "./stock-b69a2-firebase-adminsdk-t55a0-66534d7508.json")
try:
    firebase_apps = firebase_admin.get_app()
    if (firebase_apps):
        firebase_admin.delete_app(firebase_apps)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://stock-b69a2.firebaseio.com'
        })
except:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://stock-b69a2.firebaseio.com'
    })
finally:
    dir = db.reference('계좌정보')
    json_list = dir.get()
    message = ""
    for stock in json_list:
        item = json_list[stock]
        message += item['종목명']
        message += "의 수익률은 "
        message += item['수익률(%)']
        message += "퍼센트, "
    print(message)
