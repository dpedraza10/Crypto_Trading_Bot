# Packages
import config
import alpaca_trade_api as tradeapi

api = tradeapi.REST(
    base_url=config.APCA_API_BASE_URL,
    key_id=config.ALPACA_API_KEY,
    secret_key=config.ALPACA_SECRET_KEY,
    api_version='v2'
)

account = api.get_account()
print(account.status)
equity = float(account.equity)
margin_multiplier = float(account.multiplier)
total_buying_power = margin_multiplier * equity
print(f'Initial total buying power = {total_buying_power}')

api.submit_order(symbol="ETHUSD", qty=1, side="buy", type="market", time_in_force="day")

