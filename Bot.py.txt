import os
import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# بيانات تيليجرام API الخاصة بك
API_ID = 31873798
API_HASH = '7a29803bd239bb321cce7b242f1ddb14'

# توكن بوت تيليجرام الخاص بك (ستحصل عليه من @BotFather)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ضع_توكن_البوت_هنا_إذا_لم تستخدم_Environment_Variables")

# إنشاء عميل Telethon (جلسة لحسابك الشخصي)
client = TelegramClient('bot_watan_session', API_ID, API_HASH)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك يا وطن في بوت إدارة حسابك عبر تيليجرام!\n\n"
        "لإرسال رسائل متكررة لمجموعة أو شخص، استخدم الأمر بهذا الشكل:\n"
        "`/send <الوجهة> | <عدد المرات> | <الرسالة>`\n\n"
        "مثال:\n"
        "`/send @groupname | 10 | مرحبا هذه رسالة تجريبية`",
        parse_mode="Markdown"
    )

async def send_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith('/send'):
        return

    # استخراج المدخلات بعد أمر /send
    try:
        content = text[len('/send'):].strip()
        parts = [p.strip() for p in content.split('|')]
        if len(parts) < 3:
            await update.message.reply_text("❌ الصيغة خاطئة! استخدم:\n`/send الوجهة | العدد | الرسالة`", parse_mode="Markdown")
            return
            
        target = parts[0]
        count = int(parts[1])
        message = parts[2]
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ في تنسيق الأوامر: {e}")
        return

    status_msg = await update.message.reply_text(f"🚀 جاري إرسال {count} رسالة إلى {target}...")

    if not client.is_connected():
        await client.connect()

    try:
        entity = await client.get_entity(target)
    except Exception as e:
        await status_msg.edit_text(f"❌ تعذر الوصول للوجهة: {e}")
        return

    sent = 0
    for i in range(1, count + 1):
        try:
            await client.send_message(entity, message)
            sent += 1
            await asyncio.sleep(0.6) # فاصل زمني بسيط لتجنب الحظر
        except FloodWaitError as e:
            await update.message.reply_text(f"⚠️ تقييد مؤقت! يجب الانتظار {e.seconds} ثانية.")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            break

    await status_msg.edit_text(f"✅ تمت العملية بنجاح! تم إرسال {sent} من أصل {count} رسالة.")

def main():
    # ربط جلسة Telethon
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.connect())

    # تشغيل بوت تيليجرام التفاعلي
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), send_handler))

    print("🤖 بوت تيليجرام يعمل الآن 24/7...")
    app.run_polling()

if __name__ == '__main__':
    main()
