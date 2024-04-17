import base64
import os
import asyncio
import time
import json
import sys
from telethon import TelegramClient, events, sync, utils
from telethon.errors import SessionPasswordNeededError
from kivy.config import Config
Config.set('kivy','keyboard_mode','systemanddock')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Start'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Quit'
			on_press: app.stop()

<SettingsScreen>:
    GridLayout:
		size_hint: (1, 1)
        id: "MyGrid"
        size: (1, 1)
        spacing: 10
        padding: 10
        cols: 3
		Label:
			text: '№ телефона'
		TextInput:
			id: phone
            multiline: False	
		Button:
			text: ''			
		Label:
			text: 'api_id'
		TextInput:
			id: api_id
            multiline: False	
		Button:
			text: ''	
		Label:
			text: 'api_hash'
		TextInput:
			id: api_hash
            multiline: False								
		Button:
			text: 'Записать данные'
			on_press: root.btn_press_api_hash()		

		Label:
			text: 'Пароль от TG'		
		TextInput:
			id: password
            multiline: False		
		Button:
			text: 'Записать пароль'
			on_press: root.btn_press_pass()			

		Label:
			text: 'Код из TG'		
		TextInput:
			id: code
            multiline: False		
		Button:
			text: 'Отправить код'
			on_press: root.btn_press_code()			

		Label:
			text: 'Сообщение'		
		TextInput:
			id: mess
            multiline: False		
		Button:
			text: 'Отправить сообщение'
			on_press: root.btn_press_mess()										

		Button:
			text: ''					
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
		Button:
			text: ''			
					
<ErrScreen>:
    GridLayout:
		cols: 1
		Label:
			text: 'Введены не все данные, необходимо начать заново'		
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
					
<ErrScreen2>:
    GridLayout:
		cols: 1
		Label:
			text: 'Ошибка подключения, необходимо проверить данные и начать заново'		
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'					
""")

# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):

	def btn_press_api_hash(self):
		data = {
			"phone": self.ids.phone.text,
			"api_id": self.ids.api_id.text,
			"api_hash": self.ids.api_hash.text
			}
		with open("api.json", "w") as write_file:
			json.dump(data, write_file)
	
	def btn_press_pass(self):
		global client
		password = self.ids.password.text
		phone = self.ids.phone.text
		if password == '' or phone == '' or self.ids.api_id.text == '' or self.ids.api_hash.text == '':
			global sm
			sm.add_widget(MenuScreen(name='menu'))
			sm.add_widget(SettingsScreen(name='settings'))
			sm.add_widget(ErrScreen(name='err'))
			sm.add_widget(ErrScreen2(name='err2'))
			sm.current = 'err'
			sm.switch_to(ErrScreen(name='err'))
		else:	
			client = TelegramClient('Alise', self.ids.api_id.text, self.ids.api_hash.text)
			client.connect()
			client.send_code_request(phone)
	def btn_press_code(self):
		global client
		global sm
		password = self.ids.password.text
		code = self.ids.code.text
		phone = self.ids.phone.text
		try:
			client.sign_in(phone=phone, code=code, password=password)
		except SessionPasswordNeededError as err:
			client.sign_in(password=password)
		except:
			sm.add_widget(MenuScreen(name='menu'))
			sm.add_widget(SettingsScreen(name='settings'))
			sm.add_widget(ErrScreen(name='err'))
			sm.add_widget(ErrScreen2(name='err2'))
			sm.current = 'err2'
			sm.switch_to(ErrScreen2(name='err2'))	
		else:	
			sm.add_widget(MenuScreen(name='menu'))
			sm.add_widget(SettingsScreen(name='settings'))
			sm.add_widget(ErrScreen(name='err'))
			sm.add_widget(ErrScreen2(name='err2'))
			sm.current = 'err2'
			sm.switch_to(ErrScreen2(name='err2'))	
			
	def btn_press_mess(self):
		global client	
		if client.is_user_authorized():
			mess = self.ids.mess.text
			data_mess = {
				"text": mess
			}
			with open("mess.json", "w") as write_file:
				json.dump(data_mess, write_file)
			client.send_message('@alice_speaker_bot', 'Громкость 0')
			time.sleep(1)
			client.send_message('@alice_speaker_bot', mess)
			client.disconnect()
			Pass().stop()

class ErrScreen(Screen):
    pass

class ErrScreen2(Screen):
    pass

class Pass(App):

	def build(self):
		global sm
		# Create the screen manager
		sm = ScreenManager()
		sm.add_widget(MenuScreen(name='menu'))
		sm.add_widget(SettingsScreen(name='settings'))
		sm.add_widget(ErrScreen(name='err'))
		sm.add_widget(ErrScreen2(name='err2'))

		return sm
 #       return LoginScreen()

   
class teleg():
	global client
	try:
		with open("api.json", "r") as read_file:
			data = json.load(read_file)
			api_id = data['api_id']
			api_hash = data['api_hash']
			print(api_id)
	except FileNotFoundError as err:
		Pass().run()

	if api_id == '' or api_hash == '':
		Pass().run()
	else:
		client = TelegramClient('Alise', api_id, api_hash)
		try:
			client.connect()
		except:
			Pass().run()	
	try:
		client.is_user_authorized()
	except NameError:
		Pass().stop()
		sys.exit()
	else:
		if client.is_user_authorized():
			try:
				with open("mess.json", "r") as read_file:
					data = json.load(read_file)
					mess = data['text']
			except FileNotFoundError as err:
				Pass().run()			
			client.send_message('@alice_speaker_bot', 'Громкость 0')
			time.sleep(1)
			client.send_message('@alice_speaker_bot', mess)
			client.disconnect()
		if not client.is_user_authorized():
			Pass().run()

if __name__ == '__main__':
	teleg()
