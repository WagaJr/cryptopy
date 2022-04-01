# A python cryptocurrency application
# developed by: Benjamin Waga

from tkinter import *
import requests
import pandas as pd
import plotly.graph_objects as go
import datetime
from pycoingecko import CoinGeckoAPI
from bs4 import BeautifulSoup

# <div class="priceValue "></div>
# webscrape price function
def getPrice():
    global textBox
    global input

    coin = input.get()

    # waits for user input
    if len(coin.strip()) == 0:
        textBox.delete('1.0', END)                                      # the error handling isn't great
        empty = "Please enter a cryptocurrency"
        textBox.insert('1.0', empty)
    else:
        # replaces spaces with hyphen(s)
        coin = input.get().replace(" ", "-")  # coins with multiple words require hyphens in order for due to how coinmarketcap formats their coins in the URL

        # appends user input into url
        # GET url webscrape
        url = 'https://coinmarketcap.com/currencies/'+coin+'/'

        # website request
        page = requests.get(url)

        # parse HTML
        soup = BeautifulSoup(page.text, 'lxml')

        # current price
        link = soup.select_one('.priceValue span').text
        
        coin = input.get().replace("-", " ")     # removes hyphen(s) to clean up displayed text
        textBox.delete('1.0', END)
        textBox.insert('1.0', coin + " is currently worth: " + link)
        

        # creates button to call the getGraph() function
        graphButton = Button(rightFrame, text="Show Historical Graph", padx=5, pady=5, command=lambda: getGraph(coin))
        graphButton.grid(row=1, column=0, padx=10, pady=10, sticky='w'+'e'+'n'+'s')


# candlestick graph function
def getGraph(coin):
    global root
    coin = input.get().replace(" ", "-")

    # assign CoinGecko API
    cg = CoinGeckoAPI()

    # pulls data using CoinGecko API
    coinData = cg.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=90, symbol='btc')
    type(coinData)

    # sets up graph
    coinPriceData = coinData['prices']    
    coinPriceData[0:5]
    data = pd.DataFrame(coinPriceData, columns=['TimeStamp', 'Price'])
    data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))
    chartData = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})

    coin = input.get().replace("-", " ")

    # display graph
    fig = go.Figure(data=[go.Candlestick(x=chartData['date'],
                    open=chartData['Price']['first'], 
                    high=chartData['Price']['max'],
                    low=chartData['Price']['min'], 
                    close=chartData['Price']['last'])
                    ])
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title=coin,
        xaxis_title="Days",
        yaxis_title="Price",
        font=dict(size=14)
    )
    fig.show()

# clear text
def clearText():
    global textBox
    global input

    textBox.delete('1.0', END)
    input.delete(0, END)
    

# window creation
root = Tk()
root.title("My Crypto App")
root.configure(background="#A9A9A9")
root.maxsize(1045, 400)
root.minsize(1045, 400)

# create in-window frames
leftFrame = Frame(root, width=200, height=400)
leftFrame.grid(row=0, column=0, padx=10, pady=5)

rightFrame = Frame(root)
rightFrame.grid(row=0, column=1, padx=10, pady=5)

# search bar
input = Entry(leftFrame, font=("helvetica", 20))
input.grid(row=2, column=0, padx=10, pady=10, sticky='w'+'e')
input.focus_set()

# labels
searchNoteLabel = Label(leftFrame, text="NOTE: Spelling has to be accurate & include spaces if more than one word. \n For example, 'shibainu' needs to be 'shiba inu'.", relief=RAISED)
searchNoteLabel.config(font=(25))
searchNoteLabel.grid(row=0, column=0, padx=5)

searchLabel = Label(leftFrame, text="Enter desired cyrptocurrency into the search bar:")
searchLabel.config(font=(25))
searchLabel.grid(row=1, column=0, padx=5, sticky='w')

# search button
searchButton = Button(leftFrame, text="Search", padx=5, pady=5, command=getPrice)
searchButton.grid(row=3, column=0, padx=10, pady=10, sticky='w'+'e'+'n'+'s')

# clear button
clearButton = Button(leftFrame, text="Clear", padx=5, pady=5, command=clearText)
clearButton.grid(row=4, column=0, padx=10, pady=10, sticky='w'+'e'+'n'+'s')

# create text box
textBox = Text(rightFrame, width=40, height=5, font=("helvetica", 15))
textBox.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()