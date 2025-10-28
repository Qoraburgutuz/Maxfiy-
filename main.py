import os
import asyncio
from telethon import TelegramClient, events
import openai
import config

# Sozlamalarni yuklash
api_id = config.TELEGRAM_API_ID
api_hash = config.TELEGRAM_API_HASH
openai.api_key = config.OPENAI_API_KEY

# Telegram client yaratish
client = TelegramClient('brisscoin_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def brisscoin_auto_reply(event):
    """
    Brisscoin uchun AI avtojavob funksiyasi
    """
    # Faqat shaxsiy xabarlarga javob berish
    if event.is_private:
        sender = await event.get_sender()
        
        # O'zimizga va botlarga javob bermaslik
        if not sender.bot and sender.id != (await client.get_me()).id:
            
            # 1. Avval kutish xabarini yuboramiz
            waiting_msg = await event.reply(
                f"💠 {config.BRISSCOIN_NAME} AI Assistant\n\n"
                f"🔸 Assalomu alaykum! {config.BRISSCOIN_DEVELOPER} hozirda tarmoqda emas! Iltimos kuting.\n\n"
                "Sizning xabaringiz qabul qilindi! Tez orada Brisscoin jamoasi tomonidan javob qaytariladi.\n\n"
                f"🔹 Ushbu profil \"{config.BRISSCOIN_NAME}\" kompaniyasining rasmiy AI yordamchisi."
            )
            
            try:
                # 2. AI ga so'rov yuboramiz
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system", 
                            "content": f"""Siz {config.BRISSCOIN_NAME} kompaniyasining rasmiy AI yordamchisisiz. 
                            Developer: {config.BRISSCOIN_DEVELOPER}.
                            Vazifangiz: foydalanuvchilarga professional, xushmuomala va foydali javob berish.
                            Brisscoin - kriptovalyuta va blockchain texnologiyalari kompaniyasi.
                            Har doim hurmatli va yordamchi bo'ling."""
                        },
                        {
                            "role": "user", 
                            "content": event.message.text
                        }
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                # 3. AI javobini olamiz
                ai_response = response.choices[0].message.content
                
                # 4. Kutish xabarini o'chirib, asosiy javobni yuboramiz
                await waiting_msg.delete()
                await event.reply(ai_response)
                
            except openai.error.AuthenticationError:
                await event.reply("❌ API kalit xatosi. Iltimos, konfiguratsiyani tekshiring.")
                
            except openai.error.RateLimitError:
                await event.reply("❌ API limit tugadi. Iltimos, keyinroq urinib ko'ring.")
                
            except Exception as e:
                await event.reply(f"❌ Texnik xatolik: {str(e)}")

@client.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    """
    /start komandasi uchun javob
    """
    await event.reply(
        f"🤖 Salom! Men {config.BRISSCOIN_NAME} kompaniyasining AI yordamchisiman.\n\n"
        f"🔹 Developer: {config.BRISSCOIN_DEVELOPER}\n"
        "🔹 Vazifam: sizga yordam berish\n\n"
        "Shunchaki xabar yozing, men javob beraman!"
    )

async def main():
    """
    Botni ishga tushirish
    """
    # Botni ishga tushirish
    await client.start()
    
    # Ma'lumot chiqaramiz
    me = await client.get_me()
    print(f"✅ {config.BRISSCOIN_NAME} Boti muvaffaqiyatli ishga tushdi!")
    print(f"🔹 Akkaunt: {me.first_name} (@{me.username})")
    print(f"🔹 Developer: {config.BRISSCOIN_DEVELOPER}")
    print("⏳ Xabarlarni kutish...")
    
    # Botni ishlatish
    await client.run_until_disconnected()

if name == "main":
    # Botni ishga tushirish
    asyncio.run(main())
