import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yfinance as yf
import investpy
from datetime import date, datetime, timedelta

# Configure logging to log errors and other information into the terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the bot token and bot username
TOKEN ='7091989964:AAGFB57OGyqlX0KUXrvC6dUSwCj79v-ah3c'
BOT_USERNAME ='@Threetickersbot'

#Global Function is declared first because we want to  use it in the 
# remaining part of the code. You don't need to return a function if you do not need a value from it.
async def send_message(context, update, message):
    await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=message,
            parse_mode='Markdown'
        )
# Handler function for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a message when the command /start is issued
    await send_message(context, update, "I'm a bot, please talk to me!") #Update your knowledge, you need to pass in parameters into a function to call it, 
    #unless it's a function with inbuilt parameters.

# Handler function for the /tickernews command
async def tickernews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the message text from the bot and split it into parts
    messagefrombot = update.message.text
    message_split =  messagefrombot.split(' ') 
    logging.info(message_split)
    
    instrument = ''
    date_value = ''
    importance_value = ''

    # Extract the instrument (ticker symbol) from the message
    try:
        instrument = message_split[1]
    except:
        # If no instrument is provided, send an error message
        await send_message(context, update, "Please, enter the instrument")
        return
    
    # Extract the date from the message 
    try:
        date_value = message_split[2]
    except:
        date_value = ''
        
          # Extract the importance from the message
    try:
         importance_value = message_split[3]
    except:
         importance_value = ''
    
    # Fetch ticker data from Yahoo Finance
    ticker_data = yf.Ticker(instrument)
    instrument_data = ticker_data.info
    
    # Try to get the long business summary of the instrument
    try:
        long_business_summary = instrument_data['longBusinessSummary']
    except:
        # If the instrument is not found, send an error message
        await send_message(context, update, "Financial Instrument not found. Please check Yahoo finance for the correct ticker code.")
        
    
    # Construct the message with the business summary
    message = f'*About*\n{long_business_summary}\n\n'
    message += "*All News:*\n"
    
    # Get the latest news for the instrument
    allNews = ticker_data.news
    for index in range(len(allNews)):
        news = allNews[index]
        message += f"{index + 1}. [{news['title']}]({news['link']}) \n"  # So many symbols because we are formarting strings and 
        #also using markdwons. Note this, it'll come up a lot.
    
    message += "\n"
    
    # If a date is provided, fetch financial market news for that date
    if date_value != '':
        news_date = datetime.strptime(date_value, "%Y-%m-%d").date()
        final_date = datetime.combine(news_date, datetime.min.time())
        dayBefore = final_date - timedelta(days=1)
        data = investpy.economic_calendar(from_date=dayBefore.strftime("%d/%m/%Y"), to_date=final_date.strftime("%d/%m/%Y"), countries=['united states'])  
       
        news_to_dict = data.to_dict(orient='records') # Data was a Panda,therefore, we can convert pandas to dictionary because converting to methods is a method.
        message += "*Financial Market News*\n"
        
        for index in range(len(news_to_dict)):
            news = news_to_dict[index]
            message += f"{index + 1}.{news['event']}\n"
            # logging.info(news )
    # Send the constructed message to the user
    await send_message(context, update, message)
    
    
    # Filter news by importance
    filtered_news = []
    if importance_value != "":
        for news in news_to_dict:
            if importance_value.lower() == "yes" and news['importance'] == 'high':
                filtered_news.append(news)
            elif importance_value.lower() == "no" and news['importance'] in ['low', 'medium']:
                    filtered_news.append(news)
            else:
                filtered_news = news_to_dict

        # Append filtered news to the message
        for index, news in enumerate(filtered_news):
            message += f"{index + 1}. {news['event']}\n"
           

    # Handler function for unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a message when the command is not recognized
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# Main function to run the bot
if __name__ == '__main__':
    # Create the application instance with the bot token
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Create command handlers
    start_handler = CommandHandler('start', start)
    ticker_news_handler = CommandHandler('tickernews', tickernews)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    # Add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(ticker_news_handler)
    application.add_handler(unknown_handler)

    # Start the bot by polling for updates
    application.run_polling()


