import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ParseMode
from datetime import datetime

# قراءة التوكن و الـ ADMIN من متغيرات البيئة
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))

if not TOKEN or ADMIN_ID == 0:
    raise Exception("ERROR: Please set TOKEN and ADMIN_ID environment variables.")

tickets = {}
ticket_counter = 1

def reply(update, context):
    try:
        args = context.args
        if len(args) < 2:
            update.message.reply_text("❗ الصيغة الصحيحة:\n/reply user_id الرسالة")
            return

        user_id = int(args[0])
        reply_text = " ".join(args[1:])
        context.bot.send_message(chat_id=user_id, text=f"💬 رد الإدارة:\n{reply_text}")
        update.message.reply_text("✅ تم إرسال الرد.")
    except Exception as e:
        update.message.reply_text(f"❗ خطأ: {e}")

def forward_msg(update, context):
    global ticket_counter
    user = update.message.from_user
    if update.message.text:
        msg = update.message.text
    else:
        msg = "<non-text message>"

    if user.id not in tickets:
        tickets[user.id] = ticket_counter
        ticket_counter += 1

    ticket_number = tickets[user.id]
    time_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    formatted = f"""
📨 *رسالة جديدة*

👤 *الاسم:* {user.first_name}
🔗 *اليوزر:* @{user.username if user.username else "لا يوجد"}
🆔 *معرّف المستخدم:* `{user.id}`

🎫 *رقم التذكرة:* {ticket_number}

💬 *الرسالة:* 
{msg}

⏱ *الوقت:* {time_now}
"""

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=formatted,
        parse_mode=ParseMode.MARKDOWN
    )

def start_cmd(update, context):
    update.message.reply_text("أهلاً! اكتب رسالتك وسيتم إرسالها للإدارة.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(CommandHandler("reply", reply))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_msg))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
