from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca_secrets import APCA_API_KEY_ID, APCA_API_SECRET_KEY


trading_client = TradingClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))



trading_client = TradingClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

# Get our account information.
account = trading_client.get_account()

# Check our current balance vs. our balance at the last market close
balance_change = float(account.equity) - float(account.last_equity)
print(f'Today\'s portfolio balance change: ${balance_change}')
position: Position = trading_client.get_open_position(symbol)