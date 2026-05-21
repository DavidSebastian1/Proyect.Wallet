from abc import ABC, abstractmethod
import requests
import config 
import json
import sys

#Abrir archivo json con todas las divisas disponibles
try:
  with open('badge.json', 'r', encoding='utf-8') as file:
    badge = json.load(file)
except FileNotFoundError as e:
  print(f'The JSON file with the necessary currencies could not be found! ({e})')
  sys.exit(1)
#*******Mensajes frecuentes*******
menu_msg = '\nPress enter to return to the menu'	
num_value = "You can only enter numeric values!"
#**************************************
try:#Acceso a la API pada obtener valores de divisas
  url = f"https://v6.exchangerate-api.com/v6/{config.API_KEY}/latest/USD"
  response = requests.get(url)
  data = response.json()
  api_currency = data['conversion_rates']
#Manejo de errores en caso de uso  incorrecto de la API
except AttributeError as e:
  print(f"ERROR: The config.py file with the API key is not found!\n({e})")
  sys.exit(1)
except KeyError as e:
  print(f'The API_KEY in the config.py file is invalid, please use a valid API key!\n({e})')
  sys.exit(1)
#Manejo de errores en caso de no tener conexion a internet  
except requests.exceptions.ConnectionError:
  print('---ERROR--- Necesitas una conexion a internet para poder usar el programa!\n')
  sys.exit(1)
#Clase para mostrar y modificar el balance					
class UserWallet(ABC):
  def __init__(self, wallet=0):
    self.wallet = wallet
  
  def add_usd(self, new_balance: float) -> float:
    self.wallet += new_balance 
    return self.wallet
    
  def withdraw_usd(self, withdraw: float) -> float:
    self.wallet -= (withdraw + withdraw * 0.02) #Esto aplica una comision del 2% por retiro 
    return self.wallet
  
  def __str__(self):
    return f'Your Wallet Balance: {self.wallet:,.2f}$'
#Decorador de metodo abstracto para obligar a la clase hija a inplementar estos metodos  
  @abstractmethod
  def user_add(self):
    pass
      
  @abstractmethod
  def user_withdraw(self):
    pass
      
#Clase hija de UserWallet para que el usuario modifique el balance
class UserAdd(UserWallet):
  def __init__(self):
    super().__init__()

  def user_add(self):
    try:
      user_input = float(input('Enter the amount you wish to add: '))
      self.add_usd(user_input)
      print(f'\nSuccesffully added! Your balance: ${self.wallet:,.2f}')
    except ValueError as e:
      print(f"\n{num_value}\n({e})")#Manejo de errores en caso de entrada invalida
    
  def user_withdraw(self):
    try:
      user_input = float(input('Enter the amount you wish to withdraw: '))
      if user_input < self.wallet:
        self.withdraw_usd(user_input)
        print(f"\nSuccesfully withdraw! Your balance: {self.wallet:,.2f}$\n\n**Note: A 2% fee is applied to each withdrawal.**")
      else:
        print("\nInsufficient funds to perform the operation")
    except ValueError as e:
      print(f"\n{num_value}\n({e})")#Manejo de errores en caso de entrada invalida
      
#Clase para comparar el balance con divisas extranjeras     
class Currency(UserAdd):
  def __init__(self):
    super().__init__()
    self.currency = api_currency
    
  def user_currency(self, user_input: str) -> int:
    try:
      new_currency = self.wallet * self.currency[user_input]
      return new_currency
    except KeyError as e:
      print(f"\nThe currency you indicated is incorrect or unavailable ({e})")
  
  @abstractmethod
  def input_currency(self):
    pass
    
#Clase para comparar la divisa que desee el usuario con los metodos de Currency    
class UserCurrency(Currency):
  def __init__(self):
    super().__init__()
    self.user_input = ""	
   
  def input_currency(self):
    try:
      self.user_input = input('Which currency you want to convert your USD? (Ex. VES, EUR, CNY, etc): ').upper()
      convertion = self.user_currency(self.user_input)
      if convertion is not None:
        print(f'\nYour USD {self.wallet:,.2f} is {convertion:,.3f} {badge[self.user_input]}.')
    except TypeError:
      pass
#Metodo para crear archivo de texto con todas las divisas disponibles      
  def currency_txt(self):
    with open("currency.txt", "w", encoding="utf-8") as file:
      for index, (key, value) in enumerate(badge.items(), start=1):
        file.write(f"|{index}. {key}: {value}\n|\n")
#Metodo para guardar el balance en archivo json     	  	  
def balance_json():
  try:
    with open("wallet.json", "r", encoding="utf-8") as file:
      data2 = json.load(file)
      return data2.get('Balance', 0.00)
  except (FileNotFoundError, json.JSONDecodeError):
    pass
  return 0.0  
#Metodo para guardar el balance indroducido por el usuario   
def save_balance(value):
  dict_json = {'Balance': value}
  with open('wallet.json', 'w', encoding='utf-8') as file:
    json.dump(dict_json, file, indent=4)

#Menu principal 
print('---Welcome to your Online Wallet!---')

saved_balance = balance_json()
user_currency = UserCurrency()
user_currency.wallet = saved_balance

while True:
  print('''
Please input your needed action (1, 2, 3, 4, 5):

|1. See Wallet Balance
|2. Add USD to the Wallet
|3. Withdraw USD from the Wallet
|4. See your Wallet USD as other badges
|5. View all available currencies
|6. Exit
''')
  
  user_option = input("Your option: ").strip() 
  
  if user_option == '1':
    print(user_currency)
    input(menu_msg)
  
  elif user_option == '2':
    user_currency.user_add()
    save_balance(user_currency.wallet)
    input(menu_msg)
    
  elif user_option == '3':
    user_currency.user_withdraw()
    save_balance(user_currency.wallet)
    input(menu_msg)
    
  elif user_option == '4':
    user_currency.input_currency()
    input(menu_msg)
  
  elif user_option == '5':
    user_currency.currency_txt()
    print('\nA text file has been created with all available currencies! Check it out in this same directory (currency.txt).')
    input(menu_msg)
  
  elif user_option == '6' or "":
    save_balance(user_currency.wallet)
    print('\nSession closed')
    break 
    
  else:
    print("\nInvalid option, try again") 
