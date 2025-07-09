import yfinance as yf

# ticker = "BBAS3"
# period = "5d"
# ticker_obj = yf.Ticker(f"{ticker}.SA")

# print(ticker_obj.history(period = period))

def retorna_cotacao(ticker, periodo="1mo"):
    ticker_obj = yf.Ticker(f"{ticker}.SA")
    hist = ticker_obj.history(period = periodo)["Close"]
    hist.index = hist.index.strftime("%Y-%m-%d")
    hist = round(hist,2)

    return hist.to_json()

if __name__ == "__main__":
    hist = retorna_cotacao("BBAS3")
    print(hist)