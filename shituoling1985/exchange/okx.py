import json
import time
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Kline
from config import config

# 读取配置文件
with open('config/config.json', 'r') as f:
    config = json.load(f)

# 初始化数据库
engine = create_engine(config['database_url'])
Session = sessionmaker(bind=engine)
session = Session()

class OKX:
    def __init__(self):
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.passphrase = config['passphrase']
        self.base_url = 'https://www.okx.com/api/v5'
        self.max_retries = 3  # 最大重试次数
        self.retry_delay = 2  # 重试间隔（秒）

    def _sign(self, method, path, params):
        import hmac
        import hashlib
        import base64
        import urllib.parse
        timestamp = str(int(time.time() * 1000))
        params['ts'] = timestamp
        params['sign'] = self._generate_signature(method, path, params)
        return params

    def _generate_signature(self, method, path, params):
        import hmac
        import hashlib
        import base64
        import urllib.parse
        query = urllib.parse.urlencode(params)
        payload = method + path + '?' + query
        signature = hmac.new(self.api_secret.encode(), payload.encode(), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()

    def _request(self, method, path, params=None, retries=0):
        if retries > self.max_retries:
            print("达到最大重试次数，放弃请求。")
            return None

        headers = {
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'OK-ACCESS-SIGN': self._sign(method, path, params or {})
        }
        url = self.base_url + path
        try:
            response = requests.request(method, url, headers=headers, params=params)
            response.raise_for_status()  # 检查 HTTP 错误
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败，错误信息：{e}")
            print(f"正在重试第 {retries + 1} 次...")
            time.sleep(self.retry_delay)
            return self._request(method, path, params, retries + 1)

    def validate_api(self):
        try:
            response = self._request('GET', '/users/self/verify')
            if response and response['code'] == '0':
                print("API 验证成功！")
                return True
            else:
                print("API 验证失败：", response['msg'] if response else "未知错误")
                return False
        except Exception as e:
            print("验证 API 时发生错误：", e)
            return False

    def get_klines(self, symbol, interval, limit):
        path = '/market/candles'
        params = {
            'instId': symbol,
            'bar': interval,
            'limit': limit
        }
        response = self._request('GET', path, params)
        if response and response['code'] == '0':
            return response['data']
        else:
            print("获取 K 线数据失败：", response['msg'] if response else "未知错误")
            return []

    def save_klines_to_db(self, symbol, interval, limit):
        klines = self.get_klines(symbol, interval, limit)
        if not klines:
            print(f"未获取到 {symbol} 的 {interval} K 线数据，跳过保存。")
            return

        for kline in klines:
            kline_data = Kline(
                symbol=symbol,
                interval=interval,
                open_time=kline['ts'],
                open=kline['open'],
                high=kline['high'],
                low=kline['low'],
                close=kline['close'],
                volume=kline['vol']
            )
            session.add(kline_data)
        session.commit()
        print(f"已保存 {symbol} 的 {interval} K 线数据到数据库！")

    def place_order(self, symbol, side, ord_type, price, size):
        path = '/trade/order'
        params = {
            'instId': symbol,
            'side': side,
            'ordType': ord_type,
            'px': price,
            'sz': size
        }
        response = self._request('POST', path, params)
        if response and response['code'] == '0':
            print("下单成功：", response['data'][0]['ordId'])
            return response['data'][0]['ordId']
        else:
            print("下单失败：", response['msg'] if response else "未知错误")
            return None

    def cancel_order(self, symbol, order_id):
        path = '/trade/cancel-order'
        params = {
            'instId': symbol,
            'ordId': order_id
        }
        response = self._request('POST', path, params)
        if response and response['code'] == '0':
            print("撤单成功：", response['data'][0]['ordId'])
            return response['data'][0]['ordId']
        else:
            print("撤单失败：", response['msg'] if response else "未知错误")
            return None

    def set_leverage(self, symbol, leverage, direction):
        path = '/account/set-leverage'
        params = {
            'instId': symbol,
            'lever': leverage,
            'mgnMode': 'cross'  # 或 'isolated'
        }
        response = self._request('POST', path, params)
        if response and response['code'] == '0':
            print("设置杠杆成功：", response['data'])
            return response['data']
        else:
            print("设置杠杆失败：", response['msg'] if response else "未知错误")
            return None

# 示例用法
if __name__ == '__main__':
    okx = OKX()
    if okx.validate_api():
        # 获取 K 线数据并保存到数据库
        symbols = ['BTC-USDT', 'ETH-USDT', 'BTC-USDT-SWAP', 'ETH-USDT-SWAP']
        intervals = ['5m', '3D', '1D', '8H', '4H', '1H']
        limits = [500, 500, 1000, 1000, 1000, 1000]
        for symbol, interval, limit in zip(symbols, intervals, limits):
            okx.save_klines_to_db(symbol, interval, limit)

        # 下单示例
        symbol = 'BTC-USDT'
        order_id = okx.place_order(symbol, 'buy', 'limit', '10000', '0.01')
        if order_id:
            # 撤单示例
            okx.cancel_order(symbol, order_id)

        # 设置杠杆示例
        okx.set_leverage('BTC-USDT-SWAP', 10, 'long')
       def get_order_status(self, symbol, order_id):
    """
    查询订单状态
    :param symbol: 交易对 (e.g., 'BTC-USDT')
    :param order_id: 订单 ID
    :return: 订单状态
    """
    path = '/trade/order'
    params = {
        'instId': symbol,
        'ordId': order_id
    }
    response = self._request('GET', path, params)
    if response['code'] == '0':
        return response['data'][0]['state']
    else:
        print("查询订单状态失败：", response['msg'])
        return None
       def get_account_balance(self):
    """
    获取账户余额
    :return: 账户余额
    """
    path = '/account/balance'
    params = {}
    response = self._request('GET', path, params)
    if response['code'] == '0':
        return response['data']
    else:
        print("获取账户余额失败：", response['msg'])
        return None
        def get_positions(self):
    """
    获取持仓信息
    :return: 持仓信息
    """
    path = '/position/holding'
    params = {}
    response = self._request('GET', path, params)
    if response['code'] == '0':
        return response['data']
    else:
        print("获取持仓信息失败：", response['msg'])
        return None
        def set_stop_loss_take_profit(self, symbol, order_id, sl_price, tp_price):
    """
    设置止损和止盈
    :param symbol: 交易对 (e.g., 'BTC-USDT')
    :param order_id: 订单 ID
    :param sl_price: 止损价格
    :param tp_price: 止盈价格
    :return: 设置结果
    """
    path = '/trade/order'
    params = {
        'instId': symbol,
        'ordId': order_id,
        'slTriggerPx': sl_price,
        'tpTriggerPx': tp_price
    }
    response = self._request('POST', path, params)
    if response['code'] == '0':
        print("设置止损和止盈成功：", response['data'])
        return response['data']
    else:
        print("设置止损和止盈失败：", response['msg'])
        return None
        import websocket

def subscribe_realtime_data(self, symbol, interval):
    """
    订阅实时行情数据
    :param symbol: 交易对 (e.g., 'BTC-USDT')
    :param interval: 周期 (e.g., '1m')
    :return: None
    """
    def on_message(ws, message):
        print(f"收到实时行情数据：{message}")

    def on_error(ws, error):
        print(f"实时行情数据订阅错误：{error}")

    def on_close(ws):
        print("实时行情数据订阅已关闭")

    def on_open(ws):
        ws.send(json.dumps({
            'op': 'subscribe',
            'args': [f'{symbol}@candle{interval}']
        }))

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        'wss://www.okx.com/ws/v5/public',
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
