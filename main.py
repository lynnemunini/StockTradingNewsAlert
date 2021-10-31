# To get the account_sid and auth_token make an account on twilio
# Also make acccounts on News API and Alpha_Vantage to get the api keys


import requests
# import os
import html
from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient
account_sid = ""
auth_token = ""
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = ""
ALPHA_VANTAGE_API = ""

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "full",
    "apikey": ALPHA_VANTAGE_API
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()
data_dict = data["Time Series (Daily)"]
# Get yesterday's closing stock price
data_dates_list = list(data_dict.keys())
yesterday_date = data_dates_list[0]
yesterday_stock = data_dict[f"{yesterday_date}"]["4. close"]

# Get the day before yesterday's closing stock price
before_yesterday_date = data_dates_list[1]
before_yesterday_stock = data_dict[f"{before_yesterday_date}"]["4. close"]

# find difference between yesterday_stock and before_yesterday_stock
difference = (float(yesterday_stock) - float(before_yesterday_stock))
print(difference)
average = (float(yesterday_stock)+float(before_yesterday_stock))/2
print(average)
# Percentage difference = Absolute difference / Average x 100
percentage = round((difference/average)*100)
print(percentage)
up_down = None
if percentage > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(percentage) > 1:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    # print(news_data)
    articles = news_data["articles"][1:4]
    # print(len(articles))
    my_articles = []
    for article in articles:
        new_article = html.unescape(article)
        my_articles.append(new_article)

    for each in my_articles:
        client = Client(account_sid, auth_token)
        message = client.messages \
        .create(
        body=f"\nTSLA UPDATES: {up_down} {percentage}%\n\n{each['title']},\n\n{each['description']}",
        # Enter the number here '+1234567890'
        from_="",
        # Enter the number here '+1234567890'
        to=''
        )
        print(message.status)



