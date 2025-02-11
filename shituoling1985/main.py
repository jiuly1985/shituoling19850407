from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton  
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import os
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import os_
from kivy.lang import Builder

# 如果字体文件在 src 目录下
resource_add_path(os.path.abspath("./src"))

# 注册自定义字体（需要字体文件）
LabelBase.register(name='CustomFont', fn_regular='DroidSansFallback.ttf')  # 替换为支持中文的字体

Builder.load_string('''
<CustomButton@Button>:
    font_name: 'CustomFont'
    color: (0, 0, 0, 1) if self.background_color[0]+self.background_color[1]+self.background_color[2] > 1.5 else (1, 1, 1, 1)
    background_normal: ''
    background_down: ''
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
''')

# 启动界面
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # 启动按钮
        start_btn = Button(
            text='start',
            size_hint=(0.2, 0.1),  # 调整按钮尺寸
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            background_color=(0, 1, 0, 1),
            font_size=40
        )
        start_btn.bind(on_press=self.switch_to_main)
        
        # 退出按钮
        exit_btn = Button(
            text='Exit',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=(1, 0, 0, 1),
            font_size=40
        )
        exit_btn.bind(on_press=self.exit_app)

        layout.add_widget(start_btn)
        layout.add_widget(exit_btn)
        self.add_widget(layout)

    def switch_to_main(self, instance):
        self.manager.current = 'main'

    def exit_app(self, instance):
        App.get_running_app().stop()

# 主界面
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')
        
        # 信息显示区域
        scroll = ScrollView(size_hint=(1, 0.8))
        self.info_label = Label(
            text='Main Screen Information Display',
            size_hint_y=None,
            height=500,
            text_size=(Window.width*0.9, None),
            halign='left',
            valign='top',
            font_name='CustomFont'
        )
        scroll.add_widget(self.info_label)
        
        # 底部按钮布局
        btn_layout = BoxLayout(
            size_hint=(1, 0.15),  # 增加按钮高度
            spacing=10,
            padding=10
        )
        
        # 五个功能按钮（调整颜色对比度）
        buttons = [
            ('Back', self.back_to_start, (0.2, 0.2, 1, 1)),
            ('Connect', self.show_api_popup, (0.2, 0.8, 0.2, 1)),
            ('Operate', self.go_to_operations, (0.8, 0.5, 0.2, 1)),
            ('Log', self.go_to_logs, (0.5, 0.2, 0.8, 1)),
            ('Strategy', self.go_to_strategy, (0.9, 0.7, 0.3, 1))
        ]
        
        for text, callback, color in buttons:
            btn = Button(
                text=text,
                size_hint=(0.2, 1),
                background_color=color,
                font_size=32,
                bold=True
            )
            btn.bind(on_press=callback)
            btn_layout.add_widget(btn)

        main_layout.add_widget(scroll)
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)

    def back_to_start(self, instance):
        self.manager.current = 'start'

    def show_api_popup(self, instance):
        # API输入弹窗
        content = BoxLayout(orientation='vertical', padding=10)

        self.api_key = TextInput(
            hint_text='Enter API Key',
            font_name='CustomFont',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.api_secret = TextInput(
            hint_text='Enter API Secret',
            font_name='CustomFont',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.passphrase = TextInput(
            hint_text='Enter Passphrase',
            font_name='CustomFont',
            background_color=(0.9, 0.9, 0.9, 1)
        )

        btn_layout = BoxLayout(size_hint=(1, 0.2))
        confirm = Button(
            text='Confirm',
            background_color=(0, 0.7, 0, 1),
            font_size=32
        )
        cancel = Button(
            text='Cancel',
            background_color=(0.7, 0, 0, 1),
            font_size=32
        )

        confirm.bind(on_press=self.save_api)
        cancel.bind(on_press=lambda x: self.popup.dismiss())

        btn_layout.add_widget(confirm)
        btn_layout.add_widget(cancel)

        content.add_widget(self.api_key)
        content.add_widget(self.api_secret)
        content.add_widget(self.passphrase)
        content.add_widget(btn_layout)

        self.popup = Popup(
            title='API Configuration',
            title_font='CustomFont',
            content=content,
            size_hint=(0.8, 0.5),
            separator_color=(0, 0.5, 1, 1)
        )
        self.popup.open()

    def save_api(self, instance):
        self.info_label.text += "\nAPI Configuration Saved"
        self.popup.dismiss()

    def go_to_operations(self, instance):
        self.manager.current = 'operations'

    def go_to_logs(self, instance):
        self.manager.current = 'logs'

    def go_to_strategy(self, instance):
        self.manager.current = 'strategy'

# 操作界面
class OperationsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # K 线图表区域
        self.chart_layout = BoxLayout(size_hint=(1, 0.6))
        self.kline_chart = Label(
            text='K-line Chart Area',
            font_name='CustomFont',
            font_size=24,
            color=(1, 1, 1, 1)
        )
        self.chart_layout.add_widget(self.kline_chart)

        # 指标图表区域（上下排列）
        self.indicators_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        
        # MACD 指标
        self.macd_chart = Label(
            text='MACD Indicator',
            font_name='CustomFont',
            font_size=20,
            color=(1, 1, 1, 1)
        )
        
        # KDJ 指标
        self.kdj_chart = Label(
            text='KDJ Indicator',
            font_name='CustomFont',
            font_size=20,
            color=(1, 1, 1, 1)
        )
        
        # RSI 指标
        self.rsi_chart = Label(
            text='RSI Indicator',
            font_name='CustomFont',
            font_size=20,
            color=(1, 1, 1, 1)
        )
        
        # STOCHRSI 指标
        self.stochrsi_chart = Label(
            text='STOCHRSI Indicator',
            font_name='CustomFont',
            font_size=20,
            color=(1, 1, 1, 1)
        )

        self.indicators_layout.add_widget(self.macd_chart)
        self.indicators_layout.add_widget(self.kdj_chart)
        self.indicators_layout.add_widget(self.rsi_chart)
        self.indicators_layout.add_widget(self.stochrsi_chart)

        # 底部按钮布局（并排排列）
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10, padding=10)
        close_position_btn = Button(
            text='Close Position',
            size_hint=(0.25, 1),
            background_color=(0.2, 0.8, 0.2, 1),
            font_size=32,
            bold=True
        )
        auto_btn = Button(
            text='Auto',
            size_hint=(0.25, 1),
            background_color=(0.8, 0.5, 0.2, 1),
            font_size=32,
            bold=True
        )
        open_position_btn = Button(
            text='Open Position',
            size_hint=(0.25, 1),
            background_color=(0.9, 0.7, 0.3, 1),
            font_size=32,
            bold=True
        )
        back_btn = Button(
            text='Back',
            size_hint=(0.25, 1),
            background_color=(0.7, 0.7, 0.7, 1),
            font_size=32,
            bold=True
        )

        close_position_btn.bind(on_press=self.close_position)
        auto_btn.bind(on_press=self.auto_mode)
        open_position_btn.bind(on_press=self.open_position)
        back_btn.bind(on_press=self.back_to_main)

        btn_layout.add_widget(close_position_btn)
        btn_layout.add_widget(auto_btn)
        btn_layout.add_widget(open_position_btn)
        btn_layout.add_widget(back_btn)

        layout.add_widget(self.chart_layout)
        layout.add_widget(self.indicators_layout)
        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def close_position(self, instance):
        self.kline_chart.text = "Close Position Button Clicked"
        # 在这里添加平仓逻辑

    def auto_mode(self, instance):
        self.kline_chart.text = "Auto Mode Button Clicked"
        # 在这里添加自动模式逻辑

    def open_position(self, instance):
        self.kline_chart.text = "Open Position Button Clicked"
        # 在这里添加开仓逻辑

    def back_to_main(self, instance):
        self.manager.current = 'main'

# 日志界面
class LogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()  # 使用 FloatLayout 以便自由定位按钮

        # 标题
        title_label = Label(
            text='Trade Log Screen',
            font_name='CustomFont',
            font_size=24,
            pos_hint={'center_x': 0.5, 'top': 1},
            size_hint=(0.8, 0.1)
        )

        # 日志显示区域（可滚动）
        scroll_view = ScrollView(
            pos_hint={'x': 0, 'top': 0.1},
            size_hint=(1, 0.9)
        )
        self.log_label = Label(
            text='Log information will be displayed here\n',
            font_name='CustomFont',
            font_size=18,
            text_size=(Window.width * 0.9, None),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        self.log_label.bind(texture_size=lambda *args: setattr(self.log_label, 'height', self.log_label.texture_size[1]))
        scroll_view.add_widget(self.log_label)

        # 查看按钮
        view_btn = Button(
            text='View',
            font_name='CustomFont',
            font_size=20,
            background_color=(0.2, 0.8, 0.2, 1),
            pos_hint={'right': 0.6, 'top': 1},
            size_hint=(0.2, 0.1)
        )
        view_btn.bind(on_press=self.show_log_popup)

        # 关闭按钮（退回到主界面）
        close_btn = Button(
            text='Close',
            font_name='CustomFont',
            font_size=20,
            background_color=(1, 0, 0, 1),
            pos_hint={'right': 1, 'top': 1},
            size_hint=(0.2, 0.1)
        )
        close_btn.bind(on_press=self.back_to_main)

        layout.add_widget(title_label)
        layout.add_widget(scroll_view)
        layout.add_widget(view_btn)
        layout.add_widget(close_btn)
        self.add_widget(layout)

    def show_log_popup(self, instance):
        # 弹窗：查看指定时间段的交易记录
        content = BoxLayout(orientation='vertical', padding=10)
        start_date = TextInput(
            hint_text='Start Date (YYYY-MM-DD)',
            font_name='CustomFont',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        end_date = TextInput(
            hint_text='End Date (YYYY-MM-DD)',
            font_name='CustomFont',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        btn_layout = BoxLayout(size_hint=(1, 0.2))
        confirm = Button(
            text='OK',
            background_color=(0, 0.7, 0, 1),
            font_size=20
        )
        cancel = Button(
            text='Cancel',
            background_color=(0.7, 0, 0, 1),
            font_size=20
        )
        confirm.bind(on_press=lambda x: self.load_logs(start_date.text, end_date.text))
        cancel.bind(on_press=lambda x: self.popup.dismiss())
        btn_layout.add_widget(confirm)
        btn_layout.add_widget(cancel)
        content.add_widget(start_date)
        content.add_widget(end_date)
        content.add_widget(btn_layout)
        self.popup = Popup(
            title='Select Time Period',
            title_font='CustomFont',
            content=content,
            size_hint=(0.8, 0.5),
            separator_color=(0, 0.5, 1, 1)
        )
        self.popup.open()

    def load_logs(self, start_date, end_date):
        # 加载指定时间段的日志（示例逻辑）
        self.log_label.text = f"Loading logs from {start_date} to {end_date}\n"
        self.popup.dismiss()

    def back_to_main(self, instance):
        # 退回到主界面
        self.manager.current = 'main'

# 策略配置界面
class StrategyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_strategy = None  # 存储选中的策略
        self.selected_symbol = None    # 存储选中的交易品种
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ================== 策略选择区域 ==================
        strategy_label = Label(
            text="选择策略类型",
            font_name='CustomFont',
            font_size=24,
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(strategy_label)
        
        # 策略滚动列表
        strategy_scroll = ScrollView(size_hint=(1, 0.4))
        strategy_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        strategy_grid.bind(minimum_height=strategy_grid.setter('height'))
        
        # 策略选项列表（通过 ToggleButton 实现单选）
        self.strategy_group = "strategy_group"
        strategies = [
            ("小资金高风险（资产≤1000美元，合约杠杆30倍）", "1"),
            ("小资金极高风险（资产≤1000美元，合约杠杆100倍）", "2"),
            ("中资金低风险（1000美元<资产≤100000美元，合约杠杆5倍）", "3"),
            ("中资金高风险（1000美元<资产≤100000美元，合约杠杆20倍）", "4"),
            ("中资金极高风险（1000美元<资产≤100000美元，合约杠杆50倍）", "5"),
            ("大资金低风险（资产>100000美元，合约杠杆3倍）", "6"),
            ("只做期权", "7"),
            ("只做现货（无杠杆）", "8")
        ]
        
        for text, id in strategies:
            btn = ToggleButton(
                text=text,
                group=self.strategy_group,
                font_name='CustomFont',
                font_size=18,
                size_hint_y=None,
                height=60,
                background_normal='',
                background_color=(0.3, 0.3, 0.3, 1) if int(id) % 2 == 0 else (0.2, 0.2, 0.2, 1)
            )
            btn.bind(on_press=self.update_selected_strategy)
            strategy_grid.add_widget(btn)
        
        strategy_scroll.add_widget(strategy_grid)
        main_layout.add_widget(strategy_scroll)
        
        # ================== 交易品种选择区域 ==================
        symbol_label = Label(
            text="选择交易品种",
            font_name='CustomFont',
            font_size=24,
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(symbol_label)
        
        # 交易品种网格布局（6个指定选项）
        symbol_grid = GridLayout(cols=3, spacing=10, size_hint=(1, 0.3))
        symbols = [
            "BTC/USDT",
            "ETH/USDT",
            "BTC/USDT 永续合约",
            "ETH/USDT 永续合约",
            "BTC 期权",
            "ETH 期权"
        ]
        
        for symbol in symbols:
            btn = ToggleButton(
                text=symbol,
                group="symbol_group",
                font_name='CustomFont',
                font_size=16,
                size_hint_y=None,
                height=60,  # 固定高度确保长文本显示完整
                background_normal='',
                background_color=(0.2, 0.5, 0.8, 1),
                halign='center',  # 文本居中
                valign='middle'
            )
            btn.bind(on_press=self.update_selected_symbol)
            symbol_grid.add_widget(btn)
        
        main_layout.add_widget(symbol_grid)
        
        # ================== 操作按钮区域 ==================
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=20)
        
        select_btn = Button(
            text="确认选择",
            font_name='CustomFont',
            font_size=24,
            background_color=(0, 0.7, 0, 1)
        )
        select_btn.bind(on_press=self.save_strategy)
        
        back_btn = Button(
            text="返回主界面",
            font_name='CustomFont',
            font_size=24,
            background_color=(0.7, 0, 0, 1)
        )
        back_btn.bind(on_press=self.back_to_main)
        
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(back_btn)
        main_layout.add_widget(btn_layout)
        
        self.add_widget(main_layout)
    
    # 更新选中的策略
    def update_selected_strategy(self, instance):
        if instance.state == 'down':
            self.selected_strategy = instance.text
    
    # 更新选中的交易品种
    def update_selected_symbol(self, instance):
        if instance.state == 'down':
            self.selected_symbol = instance.text
    
    # 保存策略配置
    def save_strategy(self, instance):
        if not self.selected_strategy or not self.selected_symbol:
            # 弹出错误提示
            error_popup = Popup(
                title="错误",
                content=Label(text="请先选择策略和交易品种！", font_name='CustomFont'),
                size_hint=(0.6, 0.3)
            )
            error_popup.open()
            return
        
        # 实际保存逻辑（示例）
        print(f"已保存策略：{self.selected_strategy}\n交易品种：{self.selected_symbol}")
        
        # 显示成功提示
        success_popup = Popup(
            title="成功",
            content=Label(text="策略配置已保存！", font_name='CustomFont'),
            size_hint=(0.6, 0.3)
        )
        success_popup.open()
    
    # 返回主界面
    def back_to_main(self, instance):
        self.manager.current = 'main'
# 主应用
class TradingApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        # 删除 Window.system_orientation = "portrait"（无效代码）
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(OperationsScreen(name='operations'))
        sm.add_widget(LogScreen(name='logs'))
        sm.add_widget(StrategyScreen(name='strategy'))
        return sm

if __name__ == '__main__':
    from kivy.config import Config
    Config.set('kivy', 'orientation', 'portrait')  # 添加此行
    TradingApp().run()
