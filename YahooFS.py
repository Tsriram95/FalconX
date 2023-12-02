import yfinance as yf
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Stock symbols
stock_symbols = [
    "MCHP", "ENPH", "MSFT", "ADBE", "SWI", "GOOG", 
    "NTNX", "ZS", "PANW", "FDX", "SBUX", 
    "ANET", "IBM", "FLEX", "CDNS", "CTSH"
]

# Function to get stock data
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")
    info = stock.info

    rsi = hist['Close'].diff(1).apply(lambda x: max(x, 0)).rolling(window=14).mean() / hist['Close'].diff(1).apply(lambda x: abs(x)).rolling(window=14).mean()
    rsi = 100 - 100 / (1 + rsi)
    rsi_latest = rsi.iloc[-1]

    price_to_sales = info.get('priceToSalesTrailing12Months', float('nan'))

    free_cash_flow = (info.get('totalCashFromOperatingActivities', 0) - 
                      info.get('capitalExpenditures', 0))

    cash_flow = stock.cashflow.loc['Total Cash From Operating Activities']
    capital_expenditures = stock.cashflow.loc['Capital Expenditures']
    free_cash_flow = cash_flow - capital_expenditures

    stock_price = hist['Close'].iloc[-1]
#    pfcf = stock_price / free_cash_flow if free_cash_flow != 0 else float('nan')
    week_52_low = hist['Low'].min()

    return f"Stock: {symbol}\nStock Price: {stock_price}\nRelative Strength Index: {rsi_latest}\nPrice to FreeCashFlow: {capital_expenditures}\nPrice to Sales: {price_to_sales}\n52 week low: {week_52_low}\n\n"

# Email details
sender_email = "falconx264@gmail.com"
receiver_email = ["sriram200995@gmail.com"]
#receiver_email = ["ritvik.sajja@gmail.com","sachd9143@gmail.com","angadsrandhawa@gmail.com","kyarlagadda@gmail.com","rishidasari@gmail.com","sriram200995@gmail.com"]
password = "cmkj lunm rjbs kdsi" 

# Setting up the MIME
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = ",".join(receiver_email)
message['Subject'] = "Stock Data"

# Email body
email_body = "Here is the stock data:\n\n"
for symbol in stock_symbols:
    email_body += get_stock_data(symbol)

message.attach(MIMEText(email_body, 'plain'))

# SMTP session
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")

