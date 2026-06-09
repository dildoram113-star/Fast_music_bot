import os
import telebot
import yt_dlp

API_TOKEN = '8773084476:AAHGtDB1PgATXpFHdQ5tMWnmWePqEPHfga0'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Assalomu alaykum!\n\n"
        "🎵 Botga ixtiyoriy **qo'shiq nomini yoki xonandani** yozib yuboring.\n"
        "Hech qanday ortiqcha belgi yoki buyruq shart emas! Bot uni tezda topib beradi."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def search_any_text(message):
    query = message.text.strip()
    if query.lower().startswith('/music'):
        query = query.replace('/music', '').strip()
    if not query:
        bot.reply_to(message, "❌ Iltimos, qo'shiq nomini yozing!")
        return
    status_msg = bot.reply_to(message, f"⚡ '{query}' qidirilmoqda...")
    ydl_opts = {
        'format': 'wa*[ext=m4a]/ba*[ext=m4a]/bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'no_warnings': True,
        'quiet': True,
        'geo_bypass': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            if 'entries' in info and len(info['entries']) > 0:
                filename = ydl.prepare_filename(info['entries'])
            else:
                filename = ydl.prepare_filename(info)
        base, ext = os.path.splitext(filename)
        audio_file = base + '.mp3'
        os.rename(filename, audio_file)
        with open(audio_file, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"🎵 **{query}** yuklandi.")
        os.remove(audio_file)
        bot.delete_message(message.chat.id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text("❌ Qo'shiq topilmadi yoki yuklashda xatolik bo'ldi.", message.chat.id, status_msg.message_id)

if __name__ == '__main__':
    print("Tezkor musiqa boti faol...")
    bot.infinity_polling(timeout=5, long_polling_timeout=3)
