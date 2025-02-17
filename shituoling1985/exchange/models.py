# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# 枚举类型定义（需放在模型前）
class OrderType(Enum):
    MARKET = "市价单"
    LIMIT = "限价单"

class OrderStatus(Enum):
    PENDING = "未成交"
    PARTIAL = "部分成交"
    CANCELLED = "已取消"
    COMPLETED = "已完成"

class AlertStatus(Enum):
    ACTIVE = "激活"
    TRIGGERED = "已触发"
    EXPIRED = "过期"

# ---------- 现有K线模型 ----------
class Kline(Base):
    __tablename__ = 'klines'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False)        # 交易对符号
    interval = Column(String(10))                      # K线周期（如1m, 1h）
    open_time = Column(DateTime)                       # 开盘时间
    open = Column(Float)                               # 开盘价
    high = Column(Float)                               # 最高价
    low = Column(Float)                                # 最低价
    close = Column(Float)                              # 收盘价
    volume = Column(Float)                             # 成交量

# ---------- 新增模型 ----------
class Account(Base):
    """用户账户信息"""
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)  # 唯一用户名
    password = Column(String(128), nullable=False)     # 密码（建议存储哈希值）
    balance = Column(Float, default=0.0)               # 账户余额
    created_at = Column(DateTime, server_default=func.now())  # 创建时间
    
    # 定义关系（一对多）
    orders = relationship("Order", back_populates="account")
    alerts = relationship("Alert", back_populates="account")
    strategies = relationship("Strategy", back_populates="account")

class TradePair(Base):
    """交易对信息"""
    __tablename__ = 'trade_pairs'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)      # 如 BTC-USDT
    base_currency = Column(String(10), nullable=False)          # 基础货币（BTC）
    quote_currency = Column(String(10), nullable=False)         # 对应货币（USDT）

class Order(Base):
    """订单信息"""
    __tablename__ = 'orders'
    order_id = Column(String(36), primary_key=True)    # UUID格式
    user_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    trade_pair_id = Column(Integer, ForeignKey('trade_pairs.id'))
    type = Column(Enum(OrderType), nullable=False)      # 订单类型
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    amount = Column(Float)                              # 订单数量
    price = Column(Float)                               # 限价单价格
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)
    
    # 定义关系
    account = relationship("Account", back_populates="orders")
    trade_pair = relationship("TradePair")
    transactions = relationship("Transaction", back_populates="order")

class Transaction(Base):
    """成交记录"""
    __tablename__ = 'transactions'
    transaction_id = Column(String(36), primary_key=True)
    order_id = Column(String(36), ForeignKey('orders.order_id'), index=True)
    qty = Column(Float)                                 # 成交数量
    price = Column(Float)                               # 成交价格
    traded_at = Column(DateTime, server_default=func.now())
    
    order = relationship("Order", back_populates="transactions")

class Alert(Base):
    """预警设置"""
    __tablename__ = 'alerts'
    alert_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    trade_pair_id = Column(Integer, ForeignKey('trade_pairs.id'))
    condition = Column(String(200))                     # 预警条件表达式
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    created_at = Column(DateTime, server_default=func.now())
    
    account = relationship("Account", back_populates="alerts")
    trade_pair = relationship("TradePair")

class Strategy(Base):
    """交易策略"""
    __tablename__ = 'strategies'
    strategy_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    name = Column(String(50))                           # 策略名称
    description = Column(String(500))                   # 策略描述
    parameters = Column(JSON)                           # 策略参数（JSON格式）
    is_active = Column(Boolean, default=False)          # 是否启用
    created_at = Column(DateTime, server_default=func.now())
    
    account = relationship("Account", back_populates="strategies")

class Leverage(Base):
    """杠杆设置"""
    __tablename__ = 'leverages'
    leverage_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    trade_pair_id = Column(Integer, ForeignKey('trade_pairs.id'))
    multiplier = Column(Integer, default=1)             # 杠杆倍数
    set_at = Column(DateTime, server_default=func.now())
    
    account = relationship("Account")
    trade_pair = relationship("TradePair")

class Log(Base):
    """操作日志"""
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('accounts.id'), index=True)
    type = Column(String(20))                           # 操作类型（登录/下单等）
    details = Column(String(500))                       # 操作详情
    logged_at = Column(DateTime, server_default=func.now())
