import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json


def lambda_handler(event, context):
    try:
        requestBody = json.load(event)
    except:
        requestBody = event

    action = requestBody["action"]
    actionName = action["actionName"]
    parameters = action["parameters"]

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
        if actionName == "answer_predict":
            company = parameters["company"]
            dir = db.reference('예측정보').child(company["value"])
            updown = dir.get()
            up = updown['up']
            down = updown['down']
            message = "상승" if up >= down else "하락"
            return callback_response_basic({"updown": message})
        elif actionName == "answer_totalprofit":
            dir = db.reference('총수익률')
            totalprofit = dir.get()
            return callback_response_basic({"totalprofit": totalprofit['총수익률']})
        elif actionName == "answer_show":
            dir = db.reference('계좌정보')
            json_list = dir.get()
            message = ""
            for stock in json_list:
                item = json_list[stock]
                message += item['종목명']
                message += ", "
            return callback_response_basic({"stock_list": message})
        elif actionName == "answer_eachprofit":
            dir = db.reference('계좌정보')
            json_list = dir.get()
            message = ""
            for stock in json_list:
                item = json_list[stock]
                message += item['종목명']
                message += "의 수익률은 "
                message += item['수익률(%)']
                message += "퍼센트, "
            return callback_response_basic({"message": message})






def callback_response_basic(message):
    return {
        "version": "2.0",
        "resultCode": "OK",
        "output": message,
        "directives": []
    }
