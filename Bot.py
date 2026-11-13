import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = "8811083898:AAE_HXEX7w7ncCuOGHrKk7dsiwuyj5y9PiI"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك يا وطن في بوت إدارة الرسائل!\n\n"
        "لإرسال رسائل متكررة في هذه المحادثة، استخدم الأمر بهذا الشكل:\n"
        "`/send 10 | رسالتك هنا`",
        parse_mode="Markdown"
    )

async def send_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith('/send'):
        return

    try:
        content = text[len('/send'):].strip()
        parts = [p.strip() for p in content.split('|')]
        if len(parts) < 2:
            await update.message.reply_text("❌ الصيغة خاطئة! استخدم:\n`/send العدد | الرسالة`", parse_mode="Markdown")
            return
            
        count = int(parts[0])
        message = parts[1]
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ في تنسيق الأوامر: {e}")
        return

    status_msg = await update.message.reply_text(🚀 جاري إرسال {count} رسالة...)

    sent = 0
    for i in range(1, count + 1):
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            sent += 1
            await asyncio.sleep(0.6) # فاصل زمني لتجنب الحظر
        except Exception as e:
            break

    await status_msg.edit_text(f"✅ تم إرسال {sent} من أصل {count} رسالة بنجاح!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), send_handler))

    print("🤖 البوت يعمل بكامل طاقته...")
    app.run_polling()

if __name__ == '__main__':
    main()
