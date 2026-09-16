import os
import uuid
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

files = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        file_id = context.args[0]

        if file_id in files:
            await update.message.reply_document(files[file_id])
        else:
            await update.message.reply_text("❌ File not found.")
    else:
        await update.message.reply_text("👋 Welcome!")

async def addfile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    await update.message.reply_text("📁 Ab mujhe file bhejo.")

async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.document:
        await update.message.reply_text("Please send a document/file.")
        return

    file_id = str(uuid.uuid4())[:8]
    files[file_id] = update.message.document.file_id

    bot = await context.bot.get_me()
    link = f"https://t.me/{bot.username}?start={file_id}"

    await update.message.reply_text(
        f"✅ File added!\n\n🔗 Link:\n{link}"
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addfile", addfile))
app.add_handler(MessageHandler(filters.Document.ALL, receive_file))

app.run_polling()
