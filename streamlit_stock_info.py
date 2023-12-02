import streamlit as st
import yfinance as yf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data.diff().dropna()
    up = delta.where(delta > 0, 0.0)
    down = -delta.where(delta < 0, 0.0)
    ema_up = up.ewm(span=window, adjust=False).mean()
    ema_down = down.ewm(span=window, adjust=False).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

# Function to fetch and display stock data
def show_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")
    info = stock.info

    # Calculating RSI
    rsi = calculate_rsi(hist['Close'])
    
    # Other calculations
    stock_price = hist['Close'].iloc[-1]
    week_52_low = hist['Low'].min()
    price_to_sales = info.get('priceToSalesTrailing12Months', float('nan'))

    # Displaying the data
    st.write(f"Stock: {symbol}")
    st.write(f"Stock Price: {stock_price}")
    st.write(f"Relative Strength Index: {rsi}")
    st.write(f"Price to Sales: {price_to_sales}")
    st.write(f"52 week low: {week_52_low}")

# Function to send email
def send_email(recipients, subject, body):
    sender_email = "falconx264@gmail.com"
    password = "cmkj lunm rjbs kdsi" 


    # Setting up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ", ".join(recipients)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # SMTP session
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, recipients, message.as_string())
    server.quit()

# Streamlit app layout
st.title("Stock Data and Report Sender")

# Input box for stock symbols
stock_symbols = st.text_input("Enter Stock Symbols (comma-separated)", "")

# Input for email addresses
#email_list = st.text_input("Enter email addresses to send report (comma-separated)", "")

#email_list = ["ritvik.sajja@gmail.com", "sachd9143@gmail.com", "angadsrandhawa@gmail.com", "kyarlagadda@gmail.com", "rishidasari@gmail.com", "sriram200995@gmail.com"]
email_list = ["sriram200995@gmail.com"]

# Button to process data and send email
if st.button("Generate and Send Report"):
    if stock_symbols:
        symbols = stock_symbols.split(',')
        report = ""
        for symbol in symbols:
            show_stock_data(symbol.strip().upper())
            rsi = calculate_rsi(hist['Close'])
            report += f"Stock: {symbol.strip().upper()}\n"
            report += f"Stock Price: {stock_price}\n"
            report += f"Relative Strength Index: {rsi}\n"
            report += f"Price to Sales: {price_to_sales}\n"
            report += f"52 week low: {week_52_low}\n\n"

        # Email functionality
        if email_list:
            recipients = email_list.split(',')
            send_email(recipients, "Stock Report", report)
            st.success("Report sent successfully!")
        else:
            st.error("Please enter at least one email address.")
    else:
        st.error("Please enter at least one stock symbol.")
