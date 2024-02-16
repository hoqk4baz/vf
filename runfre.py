from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# API anahtarları ve bot tokenı
api_id = '27149351'
api_hash = '2edf2bdf7cb587effd7dc089f1989cb5'
bot_token = '6800985671:AAE0mTM4g_slnIqwwoJ87omchimO0bQ4fXk'

# Client oluşturma
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Kullanıcı verilerini saklamak için bir sözlük oluştur
user_data = {}
head1 = {
    'Host': 'mobileapi.tolcompany.com',
    'x-lang': 'TR',
    'x-device-type': 'ANDROID',
    'x-device-os-version': '33',
    'x-api-uuid': '8c1495bd-9f76-4106-8e58-9fc9de34f73f',
    'x-api-hash': '439f5c9ce005a83fb0e2370db7b7442c',
    'content-type': 'application/json; charset=UTF-8',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/4.11.0'
}

# Start komutunu işle
@app.on_message(filters.command(["start"]))
def start(client, message):
    # Kullanıcı adını al
    user_name = message.from_user.first_name
    # Hoş geldin mesajını oluştur
    welcome_message = f"Merhaba {user_name}👑\n\nBotu öylesine yaptım\nBu Yüzden Kötülemeyin\nNe demişler tipi değil işlevi :)\nBilgi butonuna basarak bilgilen\n\nKanal: @darkenza_official"
    # Butonları oluştur
    buttons = [
        [InlineKeyboardButton("BiSohbet", callback_data="bi_sohbet"),
         InlineKeyboardButton("Bilgi", callback_data="bilgi")]
    ]
    # Butonları içeren bir markup oluştur
    reply_markup = InlineKeyboardMarkup(buttons)
    # Mesajı gönder
    client.send_message(message.chat.id, welcome_message, reply_markup=reply_markup)

# Bilgi butonuna basıldığında çağrılacak işlev
@app.on_callback_query(filters.regex("bilgi"))
def bilgi_callback(client, callback_query):
    # Bilgi metni
    bilgi_mesaji = "👑 Bot Sayesinde BiSohbet Premium Ücretsiz\nBiSohbet Butonuna Tıkla Numaranı Gir\nArdından Sms ile Gelen kodu gir\nArtık Premium'a Sahipsin :)\n\nBot Sahibi Kanal @darkenza_official"
    # Mesajı güncelle
    callback_query.message.edit_text(f"{bilgi_mesaji}")

    # Geri düğmesini oluştur
    back_button = InlineKeyboardButton("Geri", callback_data="back")
    # Butonları içeren bir markup oluştur
    reply_markup = InlineKeyboardMarkup([[back_button]])

    # Mesajı güncelle
    callback_query.message.edit_reply_markup(reply_markup)

# Geri düğmesine basıldığında çağrılacak işlev
@app.on_callback_query(filters.regex("back"))
def back_callback(client, callback_query):
    # Hoş geldin mesajını al
    user_name = callback_query.message.from_user.first_name
    welcome_message = f"Merhaba {user_name}! Benimle sohbet etmeye başlayabilirsin."
    # Butonları oluştur
    buttons = [
        [InlineKeyboardButton("BiSohbet", callback_data="bi_sohbet"),
         InlineKeyboardButton("Bilgi", callback_data="bilgi")]
    ]
    # Butonları içeren bir markup oluştur
    reply_markup = InlineKeyboardMarkup(buttons)
    # Mesajı güncelle
    callback_query.message.edit_text(welcome_message, reply_markup=reply_markup)


# BiSohbet butonuna basıldığında işle
@app.on_callback_query(filters.regex("^bi_sohbet$"))
def bi_sohbet(client, callback_query):
    # Kullanıcıdan telefon numarasını iste
    client.send_message(callback_query.from_user.id, "• Tel No Gir 0' olmadan")

# Telefon numarası alındığında işle
@app.on_message(filters.regex(r"^\d{10}$") & filters.private)
def get_phone_number(client, message):
    user_id = message.from_user.id
    user_data[user_id] = {"telno": message.text}
    # Numarayı kullanarak ilk isteği yap
    url1 = 'https://mobileapi.tolcompany.com/production/generate-otp'
    data1 = {
        'msisdn': '90'+user_data[user_id]["telno"]
    }
    res1 = requests.post(url1, headers=head1, json=data1).json()

    client.send_message(message.chat.id, "• Gelen Kodu Gir")

# Kod alındığında işle
@app.on_message(filters.regex(r"^\d{6}$") & filters.private)
def get_code(client, message):
    user_id = message.from_user.id
    kod = message.text
    # İkinci isteği yap
    url2 = 'https://mobileapi.tolcompany.com/production/login'
    data2 = {
        'etkApproved': False,
        'msisdn': '90'+user_data[user_id]["telno"],
        'otp': kod
    }
    token = requests.post(url2, headers=head1, json=data2).json()["token"]

    # Üçüncü isteği yap
    url3 = 'https://mobileapi.tolcompany.com/production/start-subscription-android'
    headx = {
        'Host': 'mobileapi.tolcompany.com',
        'x-lang': 'TR',
        'x-device-type': 'ANDROID',
        'x-device-os-version': '33',
        'x-api-uuid': 'fdadc049-2248-46c8-a502-41f06ee50e4e',
        'x-api-hash': '4324db9ebeb075041d323572591bdece',
        'x-auth-token': token,
        'content-type': 'application/json; charset=UTF-8',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/4.11.0'
    }
    data3 = {
        'productId': 'fourplay.tol.subscription',
        'receipt': 'amdfnjfcikbcebgbdhdiklge.AO-J1OwohGw1OYkF4nxRcmLrfB05IUkl2FDFVwOa6rvC6lwc_X4_l9oJCWFvxetdU_5trqkDGBL96gFrbjZnz8MHimcMIfCjcVykmvQDlce5azbHrUBzFjc'
    }
    res3 = requests.post(url3, headers=headx, json=data3).json()
    
    url4 = "https://mobileapi.tolcompany.com/production/tags"
    data4 = {"zodiac":"By","bodyType":"Dark","occupation":"Enza","team":"Bu","car":"Alemde","hobby":"Tekk👑","location":"Bugger"}
    res4 = requests.post(url4, headers=headx, json=data4).json()
    
    sonuc = res3["success"]
    if sonuc == True:
        client.send_message(message.chat.id, "[+]Premium Alındı İşlem Tamam /start")
print("Bot Başlatıldı")
app.run()
  
