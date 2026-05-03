import requests
import config 

try:
  url = f"https://v6.exchangerate-api.com/v6/{config.API_KEY}/latest/USD"
  response = requests.get(url)
  data = response.json()
  api_currency = data['conversion_rates']
except AttributeError:
  print("ERROR: The config.py file with the API key is not found!")
except KeyError:
  print('The API_KEY in the config.py file is invalid, please use a valid API key!')
class Wallet:
  def __init__(self, user_money, currency, wallet=0):
    self.user_money = user_money
    self.currency = currency
    self.__wallet = wallet
	
  def see_wallet(self):
    print(f'You have USD {self.__wallet:.2f} in the Wallet')
    input('\nPress enter to return to the menu')
	 
  def user_wallet(self):
    user_action  = int(input('Select your needed action (1. Add USD to the wallet, 2. Withdraw USD of the wallet): '))
    if user_action == 1:
      self.user_money = float(input('How much USD you want to add?: '))
      self.__wallet += self.user_money
      print(f'Successfully added! your wallet now has USD {self.__wallet:.2f}')
      input('\nPress enter to return to the menu') 
    elif user_action == 2:
      self.user_money = float(input('How much USD you want to withdraw?: '))
      if self.user_money <= self.__wallet:
        self.__wallet -= self.user_money
        print(f'Successfully withdrawn! your wallet now has USD {self.__wallet:.2f}')
        input('\nPress enter to return to the menu')
      else:
        print('Error, insufficient USD in Wallet') 
        input('\nPress enter to return to the menu')
    else:
      print('Error, invalid action') 
      input('\nPress enter to return to the menu') 
    return self.__wallet
		
  def user_input(self):
    try:
      self.currency = input('Which currency you want to convert your USD? (Ex. VES, EUR, CNY, etc): ').upper()
		
      if self.currency in api_currency:
        final_coin = self.__wallet * api_currency[self.currency]
        print(f'Your USD {self.__wallet:.2f} is {self.currency} {final_coin:.3f} right now!')
        input('\nPress enter to return to the menu') 
      
      else:
        print('Error, please select a valid currency')
        input('\nPress enter to return to the menu') 
    except NameError:
      input("API Error, press enter to return the menu")							

print('---Welcome to your Online Wallet!---')

user_usd = 0
user_currency = ''
user_add = 0
money = Wallet(user_add, user_currency, user_usd)

while True:
  print('''
Please input your needed action (1, 2, 3, 4):

|1. See Wallet Balance
|2. Add/Withdraw USD from the Wallet
|3. See your Wallet USD as other badges
|4. Exit
''')
  
  user_option = input("Select an option: ").strip()
  
  if user_option == '1':
    money.see_wallet()
    
  elif user_option == '2':
    money.user_wallet()
    
  elif user_option == '3':
    money.user_input()
    
  elif user_option == '4':
    print('Session closed')
    break 
    
  else:
    print("Invalid option, try again")
    input('\nPress enter to return to the menu')
