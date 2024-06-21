from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram import Update
import logging
import yfinance as yf
from telegram import ForceReply, Update


#Defining bot Token & username
TOKEN = 'insert-token'
BOT_USERNAME= '@Stock_Instruments_Bot'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I am your Stock bot. Input your stock name/ticker (check Yahoo Finance for ideas), and I will give you the opening and closing prices for the past 5 days.",
        reply_markup=ForceReply(selective=True),
    )

async def instrumentprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    instrument_data_frombot = update.message.text
    ticker_data = yf.Ticker(instrument_data_frombot)
    instrument_data = ticker_data.info
    try:
        
        long_business_summary = instrument_data['longBusinessSummary']
    except KeyError:
        # If the instrument is not found, send an error message
        await update.message.reply_text("Financial Instrument not found. Please check Yahoo Finance for the correct ticker code.")   
        
        
         # Construct the message with the business summary
    message = f'*About*\n{long_business_summary}\n\n'
   
    try:
        hist =ticker_data.history(period="5d") 
        Open_Price = hist['Open']
        Close_Price = hist['Close']        
        message += "\n*Here are the opening and closing prices for the past 5 days:\n"
        for date in hist.index:
            #This is an interesting piece of code. So, if you have data on the same row in the data frame, you can extract the value 
            #by inserting the common value among all of them.
            message += f"Date: {date.date()}\nOpen: {Open_Price[date]}\nClose: {Close_Price[date]}\n\n"
        
        await update.message.reply_text(message)
    except KeyError:
        # If the instrument is not found, send an error message
        await update.message.reply_text("Financial Instrument not found. Please check Yahoo Finance for the correct ticker code.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    instrumentprice_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, instrumentprice)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(instrumentprice_handler)
    application.add_handler(unknown_handler)    
    
    application.run_polling()









































# coin_market_list= cg.get_coins_markets(vs_currency= "usd", ids ="ethereum")
# coin_market_list_Dataframe = pd.DataFrame.from_dict(coin_market_list)
# coin_df = coin_market_list_Dataframe.download('ethereum', start=start, end=end) 
# how to download data from coingecko

# coin_market_list= cg.get_coin_history_by_id(id='SOL', date=start, end=end)
# coin_market_list_Dataframe = pd.dataframe.from_dict(coin_market_list)
# coin_df = coin_market_list_Dataframe.download('SOL', start=start, end=end) 
# #how to download data from coingecko

# df = yf.download('SOL', start=start, end=end)
# df.head()
# df.reset_index(inplace=True)
# df.set_index("Date", inplace=True)

# #how to save a data frame
# df.to_csv('sol.csv')

# #how to read a data frame
# df = pd.read_csv('sol.csv', parse_dates=True, index_col=0)


# #how to plot data
# df['Adj Close'].plot()
# plt.show()

# df['100ma'] = df['Adj Close'].rolling(window=100,min_periods=0).mean()
# df.dropna(inplace=True)
# # print(df.head())

# # ax1.plot(df.index, df['Adj Close'])
# # ax1.plot(df.index, df['100ma'])
# # ax2.bar(df.index, df['Volume'])

# #resampled
# df_ohlc = df['Adj Close'].resample('10D').ohlc()
# df_volume = df['Volume'].resample('10D').sum()

# # Converting Date to columns
# df_ohlc = df_ohlc.reset_index()
# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)


# #multiple graphs

# fig = plt.figure()
# ax1 = plt.subplot2grid((10,1), (0,0), rowspan=5, colspan=1)
# ax2 = plt.subplot2grid((10,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
# ax1.xaxis_date()

# # candle stick graph
# candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')

# # Volume graph
# ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)

# # # Show
# # plt.show()


