from abc import ABC, abstractmethod
import requests
import config 
import os

#*******Mensajes frecuentes*******
menu_msg = '\nPress enter to return to the menu'	
#**************************************

try:
  url = f"https://v6.exchangerate-api.com/v6/{config.API_KEY}/latest/USD"
  response = requests.get(url)
  data = response.json()
  api_currency = data['conversion_rates']
#Manejo de errores en caso de uso  incorrecto de la API
except AttributeError:
  print("ERROR: The config.py file with the API key is not found!")
  
except KeyError:
  print('The API_KEY in the config.py file is invalid, please use a valid API key!')  		
  
#Clase para mostrar y modificar el balance					
class UserWallet(ABC):
  def __init__(self, wallet=0):
    self.wallet = wallet
  
  def add_usd(self, new_balance: int) -> int:
    self.wallet += new_balance 
    return self.wallet
    
  def withdraw_usd(self, withdraw: int) -> int:
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
      user_input = int(input('Enter the amount you wish to add: '))
      self.add_usd(user_input)
      print(f'\nSuccesffully added! Your balance: ${self.wallet:,.2f}')
    except ValueError as e:
      print(f"\nYou can only enter numeric values! ({e})")#Manejo de errores en caso de entrada invalida
    
  def user_withdraw(self):
    try:
      user_input = int(input('Enter the amount you wish to withdraw: '))
      if user_input < self.wallet:
        self.withdraw_usd(user_input)
        print(f"\nSuccesfully withdraw! Your balance: {self.wallet:,.2f}$\n\n**Note: A 2% fee is applied to each withdrawal.**")
      else:
        print("\nInsufficient funds to perform the operation")
    except ValueError as e:
      print(f"\nYou can only enter numeric values! ({e})")#Manejo de errores en caso de entrada invalida
      
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
      print(f"The currency you indicated is incorrect or unavailable ({e})")
  
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
      self.user_currency(self.user_input)
      print(f'\nYour USD {self.wallet:,.2f} is {self.user_input} {self.user_currency(self.user_input):,.3f} right now!')
    except TypeError:
      pass
    	  	  
#Menu principal 
print('---Welcome to your Online Wallet!---')

user_currency = UserCurrency()

while True:
  print('''
Please input your needed action (1, 2, 3, 4, 5):

|1. See Wallet Balance
|2. Add USD to the Wallet
|3. Withdraw USD from the Wallet
|4. See your Wallet USD as other badges
|5. Exit
''')
  
  user_option = input("Your option: ").strip()
      
  if user_option == '1':
    print(user_currency)
    input(menu_msg)
  
  elif user_option == '2':
    user_currency.user_add()
    input(menu_msg)
    
  elif user_option == '3':
    user_currency.user_withdraw()
    input(menu_msg)
    
  elif user_option == '4':
    user_currency.input_currency()
    input(menu_msg)
  
  elif user_option == '5':
    print('\nSession closed')
    break 
    
  else:
    print("\nInvalid option, try again") 