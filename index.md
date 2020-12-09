# Stock-Forecasting-Program

## Members:
- San Gu, Dept. of Information System 2014005305, Hanyang University, goosan126@gmail.com
- YeonJu Nam, Dept. of Information System 2018007510, HanyangnUniversity, skaduswn0515@naver.com
- Yeol Yang, Dept. of Information System 2018057701, Hanyang University, yeolyang77@gmail.com
- CheongRok Yoon, Dept. of Information System 2011004556, Hanyang University,  dbscjdfhr@gmail.com
- Jaemin Lee, Dept. of Information System 2018007656, Hanyang University, jm4984@naver.com

## I. Introduction
### - Motivation: 
Recently, low interest rates and soaring housing prices have created a craze for investment among young people. As a result, there is a growing need for programs to help investment for generations unfamiliar with stocks. 

### - What do you want to see at the end?
This program provides easy access to the desired stock and stock market information. It is a program that predicts whether the stock will go up or down based on the information of the stock you have. Besides that, it also soothes and comforts investors' moods that change when stock price fluctuates. This program will be a reliable guide for you in the difficult stock world and allow you to check your account information by voice at any time.

## II. Datasets
### (1) Selecting the target data set
![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure1.png?raw=true)

        Figure 1 (Samsung data set example)


We went through the stock selection process for deep learning as follows. First, among the 200 stocks that represent Kospi200, the top 10 stocks in market capitalization were selected. And to predict whether each stock will rise or fall tomorrow, we collected daily data from the listing date to the present day. Daily data consist of open price, high price, low price, close price, and trading volume for each day. In addition, the adjusted stock price was selected to obtain accurate stock prices excluding factors that affect stock prices such as dividends, capital decrease, and capital increase. The stock data we selected were obtained through Kiwoom API +

### (2) Data processing for deep learning
Our goal is to show the probability of stocks rising or falling tomorrow. The LSTM will be used as a deep learning model. LSTM is good at learning series data. It also serves to hand over important information of past learning to the preceding nodes. In addition, the Binary_crossentropy will be used as a loss function, with only two cases of classes predicting whether the result will rise or fall. It Computes the cross-entropy loss between true labels and predicted labels when there are only two label classes (assumed to be 0 and 1). 

First, we extracted a series of datasets to configure the data to suit LSTM as follows:

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure2.png?raw=true)

                                                        Figure 2
 
As you can see in Figure 2, we have extracted five column data of open price, close price, high price, low price, and trading volume of M days (blue bar) from the start date (t) and close data of M+1 day (yellow bar), which we intend to predict. It then extracted data from M days that lasted one day (t+1) from the start date and extracted close data from M+1 day. The above process was repeated over and over the entire dataset.

Second, we applied one-hot encoding to the M+1 (yellow bar) data that we wanted to predict to use the binary_crosentropy loss function.

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure3.png?raw=true)

                              Figure 3

If the close price (t=M+1) rose the following day from the previous day's (t=M) close price, the M+1 data would be replaced with 1 instead of 0 otherwise. In other words, M+1 data was composed of two classes: 1 when rising and 0 when falling.

Lastly, we divided the training set and test set into 80:20 ratio. 

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure4.png?raw=true)

                                                           Figure 4
                                                     
With fewer data to be learned than expected, the ratio of training sets to test sets was estimated to be an appropriate ratio(80:20).

## III. Methodology
### 1. Structure

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure5.png?raw=true)

                                                           Figure 5
                                             
#### (1). User
Calls to play ‘Nugustock’ by asking someone to start playing ‘Nugustock’. In addition, if you ask for your account information, total return, return per stock item, and whether the stock price of tomorrow will rise or fall, you can hear the answer from any speaker.

#### (2). NUGU Play
After executing ‘Nugustock’ Play, if the user's intent is recognized correctly, the appropriate action is called to answer the user. At this time, the name of the action is attached to the server address of the connected backend, and the backend requests information that matches the user's command.

#### (3). AWS Lambda
Receives an API Request and retrieves data from DB. Then, it executes the Python code stored in the lambda, processes the data to be sent in json format, and sends it to NUGU Play as an API response.

#### (4). Firebase Realtime Database
It delivers data tailored to the request from the backend.

### 2. Development – Backend Proxy
#### (1). Build a server through AWS Lambda and add an API

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure6.png?raw=true)

                                                            Figure 6
                                                            
#### (2). Setting AWS Lambda Server Address in NUGU Play Builder

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure7.png?raw=true)

                                                            Figure 7
                                                            
#### (3). Write and describe Python code loaded into Lambda
```  
import firebase_admin  
from firebase_admin import credentials  
from firebase_admin import db  
import json  
```  

Import the firebase_admin library to import data from Firebase Realtime DB. In addition, json library is also imported to receive Nugu Play requests from AWS Lambda.

```
def lambda_handler(event, context):  
    try:  
        requestBody = json.load(event)  
    except:  
        requestBody = event  
    action = requestBody["action"]  
    actionName = action["actionName"]  
    parameters = action["parameters"]  
```
    
When processing code in a lambda following the guide, I set the name of the method to lambda_handler to recognize which method to handle. Also, actionName and parameter were extracted by reading json-type data loaded with information such as action name and parameter.

```
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
```
    
To read the Firebase DB, first check whether there is any information about the database. If there is, it was re-initialized after removing the information from the database to read the stock data that fluctuates in real time.

```
finally:  
    if actionName == "answer_predict":  
        company = parameters["company"]  
        dir = db.reference('예측정보').child(company["value"])  
        updown = dir.get()  
        up = updown['up']  
        down = updown['down']  
        message = "상승" if up >= down else "하락"  
        return callback_response_basic({"updown": message})  
```

When the database information is saved, the appropriate information is retrieved from the db according to the called action name, processed into json format data, and sent to Lambda. First, if the action name is answer_predict, the company name is fetched from json data from Whose Stock. Then, the forecast information is fetched from the database and the up/down probability of the stock matching the company name is obtained. Finally, the result is sent to Whostock through json data according to the higher probability.

```
elif actionName == "answer_totalprofit":  
    dir = db.reference('총수익률')  
    totalprofit = dir.get()  
    return callback_response_basic({"totalprofit": totalprofit['총수익률']})  
```

If the action name is answer_totalprofit, the total return information is fetched from the database and sent to Nounstock through json data.

```
elif actionName == "answer_show":  
    dir = db.reference('계좌정보')  
    json_list = dir.get()  
    message = ""  
    for stock in json_list:  
        item = json_list[stock]  
        message += item['종목명']  
        message += ", "  
    return callback_response_basic({"stock_list": message})  
```

If the action name is answer_show, the account information is fetched from the database, the names of the items in the account are extracted and sent to Whostock through json data.

```
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
```

If the action name is answer_eachprofit, account information is fetched from the database, and the rate of return for each item in the account is sent to Nounstock through json data.

```
def callback_response_basic(message):
    return {
        "version": "2.0",
        "resultCode": "OK",
        "output": message,
        "directives": []
    }
```

Send API Response code to Who Stock Play. At this time, the output is the response value to the request (total rate of return, the name of the item in the account, etc.), and the type is json format.

## IV. Evaluation & Analysis
### Predict Model

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure8.png?raw=true)

                                                            Figure 8
                                                        
We uses the tensorflow library to learn, receiving processed data, learning, and storing values of parameters. They also work to calculate the predicted probability values. In learning data, we used LSTM optimized for continuous data. LSTM serves to hand over important information of past learning to the preceding nodes.  The form of NN is Many - to - one. Because we receive as much learning data as M days and print only one output of probability whether it will rise or fall on M+1. In addition, the Binary_crossentropy will be used as a loss function, with only two cases of classes predicting whether the result will rise or fall. It Computes the cross-entropy loss between true labels and predicted labels when there are only two label classes (assumed to be 0 and 1). Finally, we selected the last activation function as sigmoid function to indicate output as probability.

### Network
Kiwoom OPEN API serves to communicate with securities firms. it adopted the ocx method. Therefore, we used the PyQt5 library to construct the overall system. Logging in to securities firms is essential and is designed to get stock event information and personal stock account information. We get the information in real time from the securities company and upload it to firebase.

## V. Related Work
In order to implement the functions of Nougat Stock Play, it was inevitable to call the Backend proxy in Nugu Play, and while looking for a method, I found an article that developed Nugu Play by connecting AWS Lambda and NUGU speakers.(https://velog.io/@jeffyoun/NUGU-%EC%8A%A4%ED%94%BC%EC%BB%A4%EC%99%80-AWS-Lambda-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)   
AWS Lambda is a module that allows you to run code for backend services on AWS servers without having to build and manage servers, and it was a very good article for me with little knowledge of backend development.
