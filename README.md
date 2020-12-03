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
(image_figure1)
Figure 1 (Samsung data set example)

We went through the stock selection process for deep learning as follows. First, among the 200 stocks that represent Kospi200, the top 10 stocks in market capitalization were selected. And to predict whether each stock will rise or fall tomorrow, we collected daily data from the listing date to the present day. Daily data consist of open price, high price, low price, close price, and trading volume for each day. In addition, the adjusted stock price was selected to obtain accurate stock prices excluding factors that affect stock prices such as dividends, capital decrease, and capital increase. The stock data we selected were obtained through Kiwoom API +

### (2) Data processing for deep learning
Our goal is to show the probability of stocks rising or falling tomorrow. The LSTM will be used as a deep learning model. LSTM is good at learning series data. It also serves to hand over important information of past learning to the preceding nodes. In addition, the Binary_crossentropy will be used as a loss function, with only two cases of classes predicting whether the result will rise or fall. It Computes the cross-entropy loss between true labels and predicted labels when there are only two label classes (assumed to be 0 and 1). 

First, we extracted a series of datasets to configure the data to suit LSTM as follows:
(image_figure2)
Figure 2
As you can see in Figure 2, we have extracted five column data of open price, close price, high price, low price, and trading volume of M days (blue bar) from the start date (t) and close data of M+1 day (yellow bar), which we intend to predict. It then extracted data from M days that lasted one day (t+1) from the start date and extracted close data from M+1 day. The above process was repeated over and over the entire dataset.

Second, we applied one-hot encoding to the M+1 (yellow bar) data that we wanted to predict to use the binary_crosentropy loss function.
(image_figure3)
Figure 3
If the close price (t=M+1) rose the following day from the previous day's (t=M) close price, the M+1 data would be replaced with 1 instead of 0 otherwise. In other words, M+1 data was composed of two classes: 1 when rising and 0 when falling.

Lastly, we divided the training set and test set into 80:20 ratio. 
(image_figure4)
Figure 4
With fewer data to be learned than expected, the ratio of training sets to test sets was estimated to be an appropriate ratio(80:20).
