from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

# Steps of the form
NAME, PHONE, EMAIL = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args # ['apply'] if they used the link

    if args and args[0] == 'apply':
        await update.message.reply_text("Karibu! Jaza fomu hii haraka.\n\n1. Jina Kamili *")
        return NAME

    await update.message.reply_text("Habari! Tumia link ya maombi kuanza.")
    return ConversationHandler.END

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("2. Namba ya Simu *")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("3. Barua Pepe *")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text

    # Summary
    msg = f"✅ Imekamilika!\n\nJina: {context.user_data['name']}\nSimu: {context.user_data['phone']}\nEmail: {context.user_data['email']}"
    await update.message.reply_text(msg)

    # Save to Google Sheets/DB here if you want
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Maombi yameghairiwa.")
    return ConversationHandler.END

def main():
    app = Application.builder().token("YOUR_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
