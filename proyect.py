import requests
import config 

url = f"https://v6.exchangerate-api.com/v6/{config.API_KEY}/latest/USD"

response = requests.get(url)
data = response.json()
coin1 = data['conversion_rates']

class Coin:
  def __init__(self, user, coin, wallet=0):
    self.user = user
    self.coin = coin
    self.wallet = wallet
	
  def see_wallet(self):
    print(f'You have USD {self.wallet:.2f} in the Wallet')
    input('\nPress enter to return to the menu')
	 
  def user_wallet(self):
    user_action  = int(input('Select your needed action (1. Add USD to the wallet, 2. Withdraw USD of the wallet): '))
    if user_action == 1:
      self.user = float(input('How much USD you want to add?: '))
      self.wallet += self.user
      print(f'Successfully added! your wallet now has USD {self.wallet:.2f}')
      input('\nPress enter to return to the menu') 
    elif user_action == 2:
      self.user = float(input('How much USD you want to withdraw?: '))
      if self.user <= self.wallet:
        self.wallet -= self.user
        print(f'Successfully withdrawn! your wallet now has USD {self.wallet:.2f}')
        input('\nPress enter to return to the menu')
      else:
        print('Error, insufficient USD in Wallet') 
        input('\nPress enter to return to the menu')
    else:
      print('Error, invalid action') 
      input('\nPress enter to return to the menu') 
    return self.wallet
		
  def user_input(self):
    try:
      self.coin = input('Which currency you want to convert your USD?(Ex. VES, EUR, CNY, etc): ').upper()
		
      if self.coin in coin1:
        final_coin = self.wallet * coin1[self.coin]
        print(f'Your USD {self.wallet:.2f} is {self.coin} {final_coin:.3f} right now!')
        input('\nPress enter to return to the menu') 
      
      else:
        print('Error, please select a valid currency')
        input('\nPress enter to return to the menu') 
        
    except:
      input('Unexpected error, press enter to return the menu')							

print('---Welcome to your Online Wallet!---')

user_money = 0
user_coin = ''
user_add = 0
money = Coin(user_add, user_coin, user_money)

while True:
  print('Please input your needed action (1, 2, 3, 4.)')
  print('1. See Wallet Balance')
  print('2. Add/Withdraw USD from the Wallet')
  print('3. See your Wallet USD as other coins')
  print('4. Exit')
  
  user_action = input("Select an option: ").strip()
  
  if user_action == '1':
    money.see_wallet()
    
  elif user_action == '2':
    money.user_wallet()
    
  elif user_action == '3':
    money.user_input()
    
  elif user_action == '4':
    print('Session closed')
    break 
    
  else:
    print("Invalid option, try again")
    input('\nPress enter to return to the menu') 
