from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests
import json
import base64

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        self.orientation = 'vertical'

        self.add_widget(Label(text='Telefon Numarası:'))
        self.phone_input = TextInput()
        self.add_widget(self.phone_input)

        self.add_widget(Label(text='Şifre:'))
        self.password_input = TextInput(password=True)
        self.add_widget(self.password_input)

        self.login_button = Button(text='Giriş Yap', on_press=self.login)
        self.add_widget(self.login_button)

        self.sms_code_input = TextInput(hint_text='SMS Kodu', multiline=False)
        self.add_widget(self.sms_code_input)

        self.verify_button = Button(text='Onayla', on_press=self.verify)
        self.add_widget(self.verify_button)

        self.spin_button = Button(text='Çarkı Çevir', on_press=self.spin_wheel, disabled=True)
        self.add_widget(self.spin_button)

    def login(self, instance):
        telno = self.phone_input.text
        parola = self.password_input.text

        headers = {
            "User-Agent": "VodafoneMCare/2308211432 CFNetwork/1325.0.1 Darwin/21.1.0",
            "Content-Length": "83",
            "Connection": "keep-alive",
            "Accept-Language": "tr_TR",
            "Accept-Encoding": "gzip, deflate, br",
            "Host": "m.vodafone.com.tr",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        url = "https://m.vodafone.com.tr/maltgtwaycbu/api/"

        data = {
            "context": "e30=",
            "username": telno,
            "method": "twoFactorAuthentication",
            "password": parola
        }

        response = requests.post(url, headers=headers, data=data)
        proid = response.json().get('process_id')
        print(proid)

        # Giriş başarılı yazdır ve Çarkı Çevir butonunu etkinleştir
        print("Giriş başarılı")
        self.proid = proid
        self.spin_button.disabled = False

    def verify(self, instance):
        kod = self.sms_code_input.text

        # İkinci isteği burada yapabilirsiniz.
        veri = {
            "langId": "tr_TR",
            "clientVersion": "17.2.5",
            "reportAdvId": "0AD98FF8-C8AB-465C-9235-DDE102D738B3",
            "pbmRight": "1",
            "rememberMe": "true",
            "sid": self.proid,
            "otpCode": kod,
            "platformName": "iPhone"
        }

        base64_veri = base64.b64encode(json.dumps(veri).encode('utf-8'))

        data2 = {
            "context": base64_veri,
            "grant_type": "urn:vodafone:params:oauth:grant-type:two-factor",
            "code": kod,
            "method": "tokenUsing2FA",
            "process_id": self.proid,
            "scope": "ALL"
        }

        response2 = requests.post(url, headers=headers, data=data2)
        sonuc2 = response2.json()
        # İkinci isteğin sonucuna göre gerekli işlemleri yapabilirsiniz.

    def spin_wheel(self, instance):
        # Çarkı Çevir butonuna basıldığında çalışacak istek
        o_head = {
            "Accept": "application/json",
            "Language": "tr",
            "ApplicationType": "1",
            "ClientKey": "AC491770-B16A-4273-9CE7-CA790F63365E",
            "sid": self.proid,
            "Content-Type": "application/json",
            "Content-Length": "54",
            "Host": "m.vodafone.com.tr",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.10.0"
        }

        cark_data = {"clientKey":"AC491770-B16A-4273-9CE7-CA790F63365E","clientVersion":"16.8.3","language":"tr","operatingSystem":"android"}
        cark_url = f"https://m.vodafone.com.tr/squat/getSquatMarketingProduct?sid={self.proid}"
        cark = requests.post(cark_url, headers=o_head, json=cark_data)
        c1 = cark.json()["data"]["name"]
        c2 = cark.json()["data"]["code"]
        c3 = cark.json()["data"]["interactionID"]
        c4 = cark.json()["data"]["identifier"]
        
        al_url = "your_al_url"  # your_al_url'u gerçek al_url ile değiştirin
        al_data = {"clientKey":"AC491770-B16A-4273-9CE7-CA790F63365E","clientVersion":"16.8.3","code":"","identifier":c4,"interactionId":c3,"language":"tr","operatingSystem":"android"}
        al = requests.post(al_url, headers=o_head, json=al_data).json()

        # İşlemleri tamamlayın ve sonuçları yazdırın
        print(c1)
        print(c2)

class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
