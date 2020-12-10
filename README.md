# Stock-Forecasting-Program

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/stock.jpg?raw=true)

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
Users can call NUGU stock play by requesting to start NUGU stock play. And if users request their account information, total profit rate, each profit rate, and tomorrow’s stock price up/down, they can listen the answer to NUGU Speaker.
#### (2). NUGU Speaker(NUGU Play)
If the user’s request (Intent) is correctly recognized after executing ‘NUGU stocker’, NUGU Speaker call the action and answer to the user. To perform this, it needs to construct backend the informations to user’s command by adding action name to connected backend proxy server address.

#### (3). AWS Lambda
If AWS Lambda received API request from NUGU Play, then it gets corresponding data from Firebase Realtime Database. Then, it execute python code that is saved in lambda, process from DB data to json format, and send API response to NUGU Play.

#### (4). Firebase Realtime Database
Firebase Realtime Database send the data corresponding the request of the backend.

### 2. Development – Backend Proxy
#### (1). Server Build with AWS Lambda and API Add

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure6.png?raw=true)

                                                        Figure 6
                                                            
#### (2). AWS Lambda URL setting in NUGU Play Builder

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure7.png?raw=true)

                                                        Figure 7
                                                            
#### (3). Write and Explain Python code loaded in lambda
```  
import firebase_admin  
from firebase_admin import credentials  
from firebase_admin import db  
import json  
```  

To get the data at Firebase Realtime Database, it imports firebase_admin library. Also, to get NUGU Play request delivered from AWS Lambda, it imports json library.

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
    
In order to let AWS Lambda recognize the code, the method name is set to ‘lambda_handler’. Also, it extract action name and parameters by reading json format data that contain the information like action name, parameters.

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
    
To read Firebase Realtime Database, it first checks whether the code has the information about the database. If it has, the code deletes and initialize it for reading real-time stock data.  
 
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

If the database information is saved, it gets the data corresponding action, manufacture to json format data, and send to AWS Lambda. First, if the action name is ‘answer_predict’, the code gets the company name from the json data of NUGU Stock Play. Then, it gets ‘예측정보’ datas from database and search the price up and down rate with the company name. Finally, it sends the higher rate to NUGU Stock with json data. 

```
elif actionName == "answer_totalprofit":  
    dir = db.reference('총수익률')  
    totalprofit = dir.get()  
    return callback_response_basic({"totalprofit": totalprofit['총수익률']})  
```

If the action name is ‘answer_totalprofit’, the code gets total profit information at database,and sends it to NUGU Stock with json data.

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

If the action name is ‘answer_show, the code gets ‘계좌정보’ data at database, extract names of stocks in the account, and sends it to NUGU Stock with json data.

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

If the action name is ‘answer_eachprofit, the code gets ‘계좌정보’ data at database, and sends profit rate of each stock to NUGU Stock with json data.

```
def callback_response_basic(message):
    return {
        "version": "2.0",
        "resultCode": "OK",
        "output": message,
        "directives": []
    }
```

It sends API Response Code to NUGU Stock Play. The output is the response about the request (total profit rate, the name of stock in the account, etc.), and the parameter’s type is json format.

## IV. Evaluation & Analysis
### Predict Model

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure8.png?raw=true)

                                                        Figure 8
                                                        
We uses the tensorflow library to learn, receiving processed data, learning, and storing values of parameters. They also work to calculate the predicted probability values. In learning data, we used LSTM optimized for continuous data. LSTM serves to hand over important information of past learning to the preceding nodes.  The form of NN is Many - to - one. Because we receive as much learning data as M days and print only one output of probability whether it will rise or fall on M+1. In addition, the Binary_crossentropy will be used as a loss function, with only two cases of classes predicting whether the result will rise or fall. It Computes the cross-entropy loss between true labels and predicted labels when there are only two label classes (assumed to be 0 and 1). Finally, we selected the last activation function as sigmoid function to indicate output as probability.

### Network
Kiwoom OPEN API serves to communicate with securities firms. it adopted the ocx method. Therefore, we used the PyQt5 library to construct the overall system. Logging in to securities firms is essential and is designed to get stock event information and personal stock account information. We get the information in real time from the securities company and upload it to firebase.

## V. Related Work
### NUGU 스피커와 AWS Lambda 사용하기
[https://velog.io/@jeffyoun/NUGU-%EC%8A%A4%ED%94%BC%EC%BB%A4%EC%99%80-AWS-Lambda-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0](https://velog.io/@jeffyoun/NUGU-%EC%8A%A4%ED%94%BC%EC%BB%A4%EC%99%80-AWS-Lambda-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0)   
For implementing the function of NUGU Stocker Play, it is inevitable to call backend proxy server. So I explored the solution, and found this post that develop NUGU Play by combining AWS Lambda and NUGU Play Builder.

### Kiwoom Open API Develop Guide(ver 1.1)
[https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.1.pdf](https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.1.pdf)   
referring to the development guide of Kiwoom Securities firm.    

### Used Deep Learning(LSTM) to predict the stock price of Samsung Electronics.
[https://teddylee777.github.io/tensorflow/LSTM%EC%9C%BC%EB%A1%9C-%EC%98%88%EC%B8%A1%ED%95%B4%EB%B3%B4%EB%8A%94-%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90-%EC%A3%BC%EA%B0%80](https://teddylee777.github.io/tensorflow/LSTM%EC%9C%BC%EB%A1%9C-%EC%98%88%EC%B8%A1%ED%95%B4%EB%B3%B4%EB%8A%94-%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90-%EC%A3%BC%EA%B0%80)  
the reference for stock prediction.   

## VI. Conclusion: Discussion
Likewise, based on the data of Kiwoom API, NUGU Play which inform the stock information is developed. Users can watch their stocks, total profit rate, each stock rate, or prediction of tomorrow’s stock price change by calling NUGU Stocker.   
But there are some problems to harm the accuracy of NUGU Stocker. We’ll be in agony to resolve those problems.  

### (1). Result
First, call NUGU Stocker play by speak ‘스토커 오픈’ or ‘스토커 시작’.


![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure9.png?raw=true)

                                                        Figure 9

If users request “내일 (Company name) 예측해줘” or “내일 (Company name) 어때”, NUGU Stocker predicts whether tomorrow’s stock price is increased or decreased.  

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure10.png?raw=true)

                                                        Figure 10
                                                        
If users request “종목별 수익률 알려줘”, NUGU Stocker inform users the profit rate of each stock. 

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure11.png?raw=true)

                                                        Figure 11
                                                        
If users request “총 수익률 알려줘”, NUGU Stocker inform users total profit rate of all stocks.

![image](https://github.com/Ediwna/Stock-Forecasting-Program/blob/gh-pages/figure12.png?raw=true)

                                                        Figure 12
                                                        
If users request “내가 가진 종목 불러줘”, NUGU Stocker informs the stock name in users’ account.

### (2). Direction of interference improvement.
#### There are 4 questions for improving our ‘NUGU Stocker’.  
1. By converting daily data into minute data, increase the data set and expect to learn well.  
2. Various variables affecting stock prices, such as interest rates and real estate indicators, are also included in the learning data.  
3. In predict function, NUGU Stocker could recognize only 15 stocks, so We’ll increase recognized stocks to 200 stocks.  
4. The accuracy rate of prediction is just 54 percent. Therefore, we’ll have priority to increase this accuracy.  
