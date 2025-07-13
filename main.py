import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import uuid

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox

from kivymd.uix.list import MDList, OneLineListItem, ThreeLineListItem, OneLineIconListItem, TwoLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.chip import MDChip
from kivymd.uix.datatables import MDDataTable
from kivymd.icon_definitions import md_icons
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.uix.widget import Widget

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Currency:
    """Currency information"""
    
    CURRENCIES = {
        "INR": {"symbol": "₹", "name": "Indian Rupee", "code": "INR"},
        "USD": {"symbol": "$", "name": "US Dollar", "code": "USD"},
        "EUR": {"symbol": "€", "name": "Euro", "code": "EUR"},
        "GBP": {"symbol": "£", "name": "British Pound", "code": "GBP"},
        "JPY": {"symbol": "¥", "name": "Japanese Yen", "code": "JPY"},
        "AUD": {"symbol": "A$", "name": "Australian Dollar", "code": "AUD"},
        "CAD": {"symbol": "C$", "name": "Canadian Dollar", "code": "CAD"},
        "CHF": {"symbol": "Fr", "name": "Swiss Franc", "code": "CHF"},
        "CNY": {"symbol": "¥", "name": "Chinese Yuan", "code": "CNY"},
        "KRW": {"symbol": "₩", "name": "South Korean Won", "code": "KRW"},
        "SGD": {"symbol": "S$", "name": "Singapore Dollar", "code": "SGD"},
        "HKD": {"symbol": "HK$", "name": "Hong Kong Dollar", "code": "HKD"},
        "MXN": {"symbol": "MX$", "name": "Mexican Peso", "code": "MXN"},
        "BRL": {"symbol": "R$", "name": "Brazilian Real", "code": "BRL"},
        "RUB": {"symbol": "₽", "name": "Russian Ruble", "code": "RUB"},
        "SAR": {"symbol": "ر.س", "name": "Saudi Riyal", "code": "SAR"},
        "AED": {"symbol": "د.إ", "name": "UAE Dirham", "code": "AED"},
        "ZAR": {"symbol": "R", "name": "South African Rand", "code": "ZAR"},
        "THB": {"symbol": "฿", "name": "Thai Baht", "code": "THB"},
        "IDR": {"symbol": "Rp", "name": "Indonesian Rupiah", "code": "IDR"},
        "MYR": {"symbol": "RM", "name": "Malaysian Ringgit", "code": "MYR"},
        "PHP": {"symbol": "₱", "name": "Philippine Peso", "code": "PHP"},
        "VND": {"symbol": "₫", "name": "Vietnamese Dong", "code": "VND"},
        "BDT": {"symbol": "৳", "name": "Bangladeshi Taka", "code": "BDT"},
        "PKR": {"symbol": "₨", "name": "Pakistani Rupee", "code": "PKR"},
        "LKR": {"symbol": "Rs", "name": "Sri Lankan Rupee", "code": "LKR"},
        "NPR": {"symbol": "Rs", "name": "Nepalese Rupee", "code": "NPR"},
        "EGP": {"symbol": "£", "name": "Egyptian Pound", "code": "EGP"},
        "NGN": {"symbol": "₦", "name": "Nigerian Naira", "code": "NGN"},
        "KES": {"symbol": "Sh", "name": "Kenyan Shilling", "code": "KES"},
        "GHS": {"symbol": "₵", "name": "Ghanaian Cedi", "code": "GHS"},
        "TRY": {"symbol": "₺", "name": "Turkish Lira", "code": "TRY"},
        "ILS": {"symbol": "₪", "name": "Israeli Shekel", "code": "ILS"},
        "NOK": {"symbol": "kr", "name": "Norwegian Krone", "code": "NOK"},
        "SEK": {"symbol": "kr", "name": "Swedish Krona", "code": "SEK"},
        "DKK": {"symbol": "kr", "name": "Danish Krone", "code": "DKK"},
        "CZK": {"symbol": "Kč", "name": "Czech Koruna", "code": "CZK"},
        "PLN": {"symbol": "zł", "name": "Polish Zloty", "code": "PLN"},
        "HUF": {"symbol": "Ft", "name": "Hungarian Forint", "code": "HUF"},
        "RON": {"symbol": "L", "name": "Romanian Leu", "code": "RON"},
        "BGN": {"symbol": "лв", "name": "Bulgarian Lev", "code": "BGN"},
        "HRK": {"symbol": "kn", "name": "Croatian Kuna", "code": "HRK"},
        "ISK": {"symbol": "kr", "name": "Icelandic Krona", "code": "ISK"},
        "NZD": {"symbol": "NZ$", "name": "New Zealand Dollar", "code": "NZD"},
        "CLP": {"symbol": "CLP$", "name": "Chilean Peso", "code": "CLP"},
        "COP": {"symbol": "COL$", "name": "Colombian Peso", "code": "COP"},
        "ARS": {"symbol": "AR$", "name": "Argentine Peso", "code": "ARS"},
        "PEN": {"symbol": "S/", "name": "Peruvian Sol", "code": "PEN"},
        "UYU": {"symbol": "UY$", "name": "Uruguayan Peso", "code": "UYU"},
        "BOB": {"symbol": "Bs", "name": "Bolivian Boliviano", "code": "BOB"},
        "ETB": {"symbol": "Br", "name": "Ethiopian Birr", "code": "ETB"},
        "MAD": {"symbol": "د.م.", "name": "Moroccan Dirham", "code": "MAD"},
        "TND": {"symbol": "د.ت", "name": "Tunisian Dinar", "code": "TND"},
        "DZD": {"symbol": "د.ج", "name": "Algerian Dinar", "code": "DZD"},
        "LYD": {"symbol": "د.ل", "name": "Libyan Dinar", "code": "LYD"},
        "JOD": {"symbol": "د.ا", "name": "Jordanian Dinar", "code": "JOD"},
        "KWD": {"symbol": "د.ك", "name": "Kuwaiti Dinar", "code": "KWD"},
        "QAR": {"symbol": "ر.ق", "name": "Qatari Riyal", "code": "QAR"},
        "BHD": {"symbol": "ب.د", "name": "Bahraini Dinar", "code": "BHD"},
        "OMR": {"symbol": "ر.ع.", "name": "Omani Rial", "code": "OMR"},
        "LBP": {"symbol": "ل.ل", "name": "Lebanese Pound", "code": "LBP"},
        "IQD": {"symbol": "ع.د", "name": "Iraqi Dinar", "code": "IQD"},
        "IRR": {"symbol": "﷼", "name": "Iranian Rial", "code": "IRR"},
        "AFN": {"symbol": "؋", "name": "Afghan Afghani", "code": "AFN"},
        "UZS": {"symbol": "лв", "name": "Uzbekistani Som", "code": "UZS"},
        "KZT": {"symbol": "₸", "name": "Kazakhstani Tenge", "code": "KZT"},
        "KGS": {"symbol": "лв", "name": "Kyrgyzstani Som", "code": "KGS"},
        "TJS": {"symbol": "ЅМ", "name": "Tajikistani Somoni", "code": "TJS"},
        "TMT": {"symbol": "T", "name": "Turkmenistani Manat", "code": "TMT"},
        "AZN": {"symbol": "₼", "name": "Azerbaijani Manat", "code": "AZN"},
        "GEL": {"symbol": "₾", "name": "Georgian Lari", "code": "GEL"},
        "AMD": {"symbol": "֏", "name": "Armenian Dram", "code": "AMD"},
        "BWP": {"symbol": "P", "name": "Botswanan Pula", "code": "BWP"},
        "NAD": {"symbol": "N$", "name": "Namibian Dollar", "code": "NAD"},
        "SZL": {"symbol": "E", "name": "Swazi Lilangeni", "code": "SZL"},
        "LSL": {"symbol": "L", "name": "Lesotho Loti", "code": "LSL"},
        "MWK": {"symbol": "MK", "name": "Malawian Kwacha", "code": "MWK"},
        "ZMW": {"symbol": "ZK", "name": "Zambian Kwacha", "code": "ZMW"},
        "ZWL": {"symbol": "Z$", "name": "Zimbabwean Dollar", "code": "ZWL"},
        "MZN": {"symbol": "MT", "name": "Mozambican Metical", "code": "MZN"},
        "AOA": {"symbol": "Kz", "name": "Angolan Kwanza", "code": "AOA"},
        "XAF": {"symbol": "CFA", "name": "Central African CFA Franc", "code": "XAF"},
        "XOF": {"symbol": "CFA", "name": "West African CFA Franc", "code": "XOF"},
        "BTC": {"symbol": "₿", "name": "Bitcoin", "code": "BTC"},
        "ETH": {"symbol": "Ξ", "name": "Ethereum", "code": "ETH"},
    }
    
    @classmethod
    def get_symbol(cls, code: str) -> str:
        return cls.CURRENCIES.get(code, {}).get("symbol", "$")
    
    @classmethod
    def get_name(cls, code: str) -> str:
        return cls.CURRENCIES.get(code, {}).get("name", "Unknown")
    
    @classmethod
    def get_display_text(cls, code: str) -> str:
        currency = cls.CURRENCIES.get(code, {})
        return f"{currency.get('symbol', '$')} {currency.get('name', 'Unknown')} ({code})"

    def on_period_chip_selected(self, selected_chip, days):
    
        self.current_period = days

        for chip in selected_chip.parent.children:
            chip.md_bg_color = (0.9, 0.9, 0.9, 1)
        selected_chip.md_bg_color = (0.3, 0.7, 0.6, 1)

        self.update_stats()


class Transaction:
    """Represents a financial transaction"""
    
    def __init__(self, amount: float, description: str, transaction_type: TransactionType, 
                 category: str, date: Optional[datetime] = None):
        self.id = str(uuid.uuid4())[:8]
        self.amount = abs(float(amount))
        self.description = description.strip()
        self.transaction_type = transaction_type
        self.category = category
        self.date = date or datetime.now()
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'transaction_type': self.transaction_type.value,
            'category': self.category,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        transaction = cls(
            amount=data['amount'],
            description=data['description'],
            transaction_type=TransactionType(data['transaction_type']),
            category=data['category'],
            date=datetime.fromisoformat(data['date'])
        )
        transaction.id = data['id']
        transaction.created_at = datetime.fromisoformat(data['created_at'])
        return transaction

class FinanceData:
    """Data management class"""
    
    INCOME_CATEGORIES = [
        ("💼", "Salary"),
        ("💻", "Freelance"),
        ("📈", "Investment"),
        ("🎁", "Gift"),
        ("💰", "Business"),
        ("🏠", "Rental"),
        ("🔄", "Refund"),
        ("💳", "Bonus"),
        ("🏆", "Prize"),
        ("💸", "Cashback"),
        ("📦", "Other Income")
    ]
    
    EXPENSE_CATEGORIES = [
        ("🍔", "Food & Dining"),
        ("🚗", "Transportation"),
        ("🏠", "Housing"),
        ("⚡", "Utilities"),
        ("🏥", "Healthcare"),
        ("🎬", "Entertainment"),
        ("🛒", "Shopping"),
        ("📚", "Education"),
        ("💳", "Bills"),
        ("👕", "Clothing"),
        ("✈️", "Travel"),
        ("🎮", "Hobbies"),
        ("💊", "Medicine"),
        ("🔧", "Maintenance"),
        ("📱", "Technology"),
        ("🎵", "Subscriptions"),
        ("🚖", "Taxi/Uber"),
        ("⛽", "Fuel"),
        ("🏋️", "Gym/Sports"),
        ("💄", "Beauty"),
        ("🎪", "Events"),
        ("🎨", "Arts & Crafts"),
        ("📦", "Other Expense")
    ]
    
    def __init__(self, data_file="finance_data.json"):
        self.data_file = data_file
        self.transactions: List[Transaction] = []
        self.currency_code = "USD"  # Default currency
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
                    self.currency_code = data.get('currency_code', 'USD')
        except Exception as e:
            print(f"Error loading data: {e}")
            self.transactions = []
            self.currency_code = "USD"
    
    def save_data(self):
        try:
            data = {
                'transactions': [t.to_dict() for t in self.transactions],
                'currency_code': self.currency_code,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def set_currency(self, currency_code: str):
        self.currency_code = currency_code
        self.save_data()
    
    def get_currency_symbol(self) -> str:
        return Currency.get_symbol(self.currency_code)
    
    def format_amount(self, amount: float) -> str:
        symbol = self.get_currency_symbol()
        return f"{symbol}{amount:,.2f}"
    
    def add_transaction(self, amount: float, description: str, 
                       transaction_type: TransactionType, category: str,
                       date: Optional[datetime] = None) -> bool:
        try:
            if amount <= 0 or not description.strip():
                return False
            
            transaction = Transaction(amount, description, transaction_type, category, date)
            self.transactions.insert(0, transaction)  # Add to beginning for recent first
            self.save_data()
            return True
        except Exception:
            return False
    
    def delete_transaction(self, transaction_id: str) -> bool:
        try:
            self.transactions = [t for t in self.transactions if t.id != transaction_id]
            self.save_data()
            return True
        except Exception:
            return False
    
    def get_balance(self) -> float:
        income = sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.INCOME)
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.EXPENSE)
        return income - expenses
    
    def get_period_stats(self, days: int = 30) -> Dict:
        cutoff = datetime.now() - timedelta(days=days)
        recent = [t for t in self.transactions if t.date >= cutoff]
        
        income = sum(t.amount for t in recent if t.transaction_type == TransactionType.INCOME)
        expenses = sum(t.amount for t in recent if t.transaction_type == TransactionType.EXPENSE)
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses,
            'count': len(recent)
        }
    
    def get_category_stats(self, transaction_type: TransactionType, days: int = 30) -> Dict:
        cutoff = datetime.now() - timedelta(days=days)
        recent = [t for t in self.transactions 
                 if t.date >= cutoff and t.transaction_type == transaction_type]
        
        category_totals = {}
        for transaction in recent:
            category = transaction.category
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += transaction.amount
        
        return category_totals
class DataHandler(FinanceData):
    def __init__(self):
        super().__init__()
        print("✅ DataHandler initialized with FinanceData features")

    def process_data(self):
        print("⚙️ Custom processing")
    

class AnimatedCard(MDCard):
    """Custom animated card with hover effects"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elevation = 4
        self.radius = [15]
        self.original_elevation = self.elevation
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Animate card press
            anim = Animation(elevation=8, duration=0.1)
            anim.start(self)
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # Animate card release
            anim = Animation(elevation=self.original_elevation, duration=0.1)
            anim.start(self)
        return super().on_touch_up(touch)

class DashboardScreen(MDScreen):
    """Enhanced dashboard screen with better animations"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.build_ui()
    
    def build_ui(self):
        # Main scrollable layout
        scroll = MDScrollView()
        main_layout = MDBoxLayout(
            orientation="vertical", 
            spacing=dp(20), 
            padding=dp(20),
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Header with currency selector
        header_layout = MDBoxLayout(
            orientation="horizontal", 
            spacing=dp(15),
            size_hint_y=None, 
            height=dp(50)
        )
        
        welcome_label = MDLabel(
            text="💰 Finance Dashboard",
            font_style="H4",
            theme_text_color="Primary",
            bold=True,
            size_hint_x=0.7
        )
        
        self.currency_button = MDRaisedButton(
            text="USD $",
            icon="currency-usd",
            size_hint_x=0.3,
            md_bg_color=get_color_from_hex("#FF6B6B"),
            on_release=self.open_currency_menu
        )
        
        header_layout.add_widget(welcome_label)
        header_layout.add_widget(self.currency_button)
        
        # Balance Card with gradient effect
        self.balance_card = AnimatedCard(
            md_bg_color=get_color_from_hex("#667eea"),
            size_hint_y=None,
            height=dp(180),
            padding=dp(25),
            elevation=12
        )
        
        balance_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        balance_header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40)
        )
        
        self.balance_label = MDLabel(
            text="💳 Current Balance",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.9),
            font_style="H6",
            size_hint_x=0.8
        )
        
        # Currency symbol in balance
        self.balance_currency = MDLabel(
            text="$",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            font_style="H6",
            size_hint_x=0.2,
            halign="right"
        )
        
        balance_header.add_widget(self.balance_label)
        balance_header.add_widget(self.balance_currency)
        
        self.balance_amount = MDLabel(
            text="0.00",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H2",
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )
        
        # Balance trend indicator
        self.balance_trend = MDLabel(
            text="📈 Looking good!",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            font_style="Subtitle1",
            size_hint_y=None,
            height=dp(30)
        )
        
        balance_layout.add_widget(balance_header)
        balance_layout.add_widget(self.balance_amount)
        balance_layout.add_widget(self.balance_trend)
        self.balance_card.add_widget(balance_layout)
        
        # Enhanced Stats Cards
        stats_layout = MDGridLayout(
            cols=2, 
            spacing=dp(15), 
            size_hint_y=None, 
            height=dp(140)
        )
        
        # Income Card
        self.income_card = AnimatedCard(
            md_bg_color=get_color_from_hex("#4ECDC4"),
            padding=dp(20),
            elevation=8
        )
        
        income_layout = MDBoxLayout(orientation="vertical", spacing=dp(5))
        
        income_header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(35)
        )
        
        income_header.add_widget(MDLabel(
            text="💚 This Month",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Subtitle1",
            size_hint_x=0.8
        ))
        
        income_header.add_widget(MDIconButton(
            icon="trending-up",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 0.8),
            size_hint_x=0.2
        ))
        
        self.income_amount = MDLabel(
            text="0.00",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            bold=True
        )
        
        income_layout.add_widget(income_header)
        income_layout.add_widget(self.income_amount)
        self.income_card.add_widget(income_layout)
        
        # Expense Card
        self.expense_card = AnimatedCard(
            md_bg_color=get_color_from_hex("#FF6B6B"),
            padding=dp(20),
            elevation=8
        )
        
        expense_layout = MDBoxLayout(orientation="vertical", spacing=dp(5))
        
        expense_header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(35)
        )
        
        expense_header.add_widget(MDLabel(
            text="💸 This Month",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="Subtitle1",
            size_hint_x=0.8
        ))
        
        expense_header.add_widget(MDIconButton(
            icon="trending-down",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 0.8),
            size_hint_x=0.2
        ))
        
        self.expense_amount = MDLabel(
            text="0.00",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            bold=True
        )
        
        expense_layout.add_widget(expense_header)
        expense_layout.add_widget(self.expense_amount)
        self.expense_card.add_widget(expense_layout)
        
        stats_layout.add_widget(self.income_card)
        stats_layout.add_widget(self.expense_card)
        
        # Quick Actions
        quick_actions_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(60)
        )
        
        add_income_btn = MDRaisedButton(
            text="💰 Add Income",
            md_bg_color=get_color_from_hex("#4ECDC4"),
            size_hint_x=0.5,
            on_release=self.quick_add_income
        )
        
        add_expense_btn = MDRaisedButton(
            text="💸 Add Expense",
            md_bg_color=get_color_from_hex("#FF6B6B"),
            size_hint_x=0.5,
            on_release=self.quick_add_expense
        )
        
        quick_actions_layout.add_widget(add_income_btn)
        quick_actions_layout.add_widget(add_expense_btn)
        
        # Recent Transactions Header
        recent_header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50)
        )
        
        recent_label = MDLabel(
            text="📋 Recent Transactions",
            font_style="H5",
            theme_text_color="Primary",
            bold=True,
            size_hint_x=0.8
        )
        
        view_all_btn = MDFlatButton(
            text="View All",
            theme_text_color="Primary",
            size_hint_x=0.2,
            on_release=self.view_all_transactions
        )
        
        recent_header.add_widget(recent_label)
        recent_header.add_widget(view_all_btn)
        
        # Recent Transactions List
        self.recent_list = MDList()
        recent_card = MDCard(
            elevation=4,
            radius=[10],
            padding=dp(5),
            size_hint_y=None
        )
        recent_card.bind(minimum_height=recent_card.setter('height'))
        recent_card.add_widget(self.recent_list)
        
        # Add all widgets to main layout
        main_layout.add_widget(header_layout)
        main_layout.add_widget(self.balance_card)
        main_layout.add_widget(stats_layout)
        main_layout.add_widget(quick_actions_layout)
        main_layout.add_widget(recent_header)
        main_layout.add_widget(recent_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def open_currency_menu(self, instance):
        """Open currency selection menu"""
        menu_items = []
        
        # Popular currencies first
        popular_currencies = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CHF", "CNY", "KRW"]
        
        for code in popular_currencies:
            currency_info = Currency.CURRENCIES.get(code, {})
            menu_items.append({
                "text": f"{currency_info.get('symbol', '$')} {currency_info.get('name', 'Unknown')}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=code: self.select_currency(x),
            })
        
        # Add separator
        menu_items.append({
            "text": "─" * 30,
            "viewclass": "OneLineListItem",
            "disabled": True,
        })
        
        # Add more currencies button
        menu_items.append({
            "text": "🌍 More Currencies...",
            "viewclass": "OneLineListItem",
            "on_release": lambda x: self.show_all_currencies(),
})

        self.currency_menu = MDDropdownMenu(
            caller=self.currency_button,
            items=menu_items,
            width_mult=4,
            max_height=dp(400),
        )
        self.currency_menu.open()

    def show_all_currencies(self):
        """Show all available currencies in a dialog"""
        self.currency_menu.dismiss()
        
        # Create a dialog with all currencies
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(400)
        )
        
        scroll = MDScrollView()
        currency_list = MDList()
        
        for code, info in Currency.CURRENCIES.items():
            item = OneLineListItem(
                text=f"{info['symbol']} {info['name']} ({code})",
                on_release=lambda x, code=code: self.select_currency_from_dialog(code)
            )
            currency_list.add_widget(item)
        
        scroll.add_widget(currency_list)
        content.add_widget(scroll)
        
        self.all_currencies_dialog = MDDialog(
            title="Select Currency",
            content=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.all_currencies_dialog.dismiss()
                )
            ]
        )
        self.all_currencies_dialog.open()

    def select_currency_from_dialog(self, currency_code):
        """Select currency from dialog"""
        self.all_currencies_dialog.dismiss()
        self.select_currency(currency_code)

    def select_currency(self, currency_code):
        """Select a currency and update the display"""
        if self.data:
            self.data.set_currency(currency_code)
            self.update_currency_display()
            self.update_dashboard()
            self.currency_menu.dismiss()

    def update_currency_display(self):
        """Update currency display in UI"""
        if self.data:
            symbol = self.data.get_currency_symbol()
            name = Currency.get_name(self.data.currency_code)
            self.currency_button.text = f"{self.data.currency_code} {symbol}"
            self.balance_currency.text = symbol

    def quick_add_income(self, instance):
        """Quick add income dialog"""
        self.show_add_transaction_dialog(TransactionType.INCOME)

    def quick_add_expense(self, instance):
        """Quick add expense dialog"""
        self.show_add_transaction_dialog(TransactionType.EXPENSE)

    def show_add_transaction_dialog(self, transaction_type):
   

    # Create content layout
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(10),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter("height"))

        # Amount Field
        self.amount_field = MDTextField(
            hint_text="Amount",
            helper_text="Enter amount",
            helper_text_mode="on_focus",
            icon_right="currency-usd",
            size_hint_y=None,
            height=dp(60)
        )

        # Description Field
        self.description_field = MDTextField(
            hint_text="Description",
            helper_text="Enter description",
            helper_text_mode="on_focus",
            icon_right="text",
            size_hint_y=None,
            height=dp(60)
        )

        # Category
        categories = (self.data.INCOME_CATEGORIES if transaction_type == TransactionType.INCOME 
                    else self.data.EXPENSE_CATEGORIES)

        category_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(40))
        category_label = MDLabel(text="Category:", size_hint_x=0.3, theme_text_color="Primary")

        self.category_button = MDRaisedButton(
            text=f"{categories[0][0]} {categories[0][1]}",
            size_hint_x=0.7,
            on_release=lambda x: self.open_category_menu(categories, transaction_type)
        )
        category_layout.add_widget(category_label)
        category_layout.add_widget(self.category_button)

        # Date
        date_layout = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(40))
        date_label = MDLabel(text="Date:", size_hint_x=0.3, theme_text_color="Primary")
        self.date_button = MDRaisedButton(
            text=datetime.now().strftime("%Y-%m-%d"),
            size_hint_x=0.7,
            on_release=self.open_date_picker
        )
        date_layout.add_widget(date_label)
        date_layout.add_widget(self.date_button)

        # Add widgets to content
        content_layout.add_widget(self.amount_field)
        content_layout.add_widget(self.description_field)
        content_layout.add_widget(category_layout)
        content_layout.add_widget(date_layout)

        # Wrap in ScrollView
        scroll = MDScrollView()
        scroll.add_widget(content_layout)

        # Save selection state
        self.selected_category = categories[0][1]
        self.selected_date = datetime.now()
        self.current_transaction_type = transaction_type

        # Dialog Title
        title = "Add Income" if transaction_type == TransactionType.INCOME else "Add Expense"

        # Create Dialog
        self.add_dialog = MDDialog(
            title=title,
            content_cls=scroll,
            type="custom",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.add_dialog.dismiss()),
                MDRaisedButton(text="ADD", on_release=self.add_transaction)
            ]
        )
        self.add_dialog.open()


    def open_category_menu(self, categories, transaction_type):
        """Open category selection menu"""
        menu_items = []
        for emoji, category in categories:
            menu_items.append({
                "text": f"{emoji} {category}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=category, e=emoji: self.select_category(e, x),
            })

        self.category_menu = MDDropdownMenu(
            caller=self.category_button,
            items=menu_items,
            width_mult=4,
        )
        self.category_menu.open()

    def select_category(self, emoji, category):
        """Select category"""
        self.selected_category = category
        self.category_button.text = f"{emoji} {category}"
        self.category_menu.dismiss()

    def open_date_picker(self, instance):
        """Open date picker"""
        date_dialog = MDDatePicker(
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
        )
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()

    def get_date(self, instance, value, date_range):
        """Get selected date"""
        self.selected_date = datetime.combine(value, datetime.min.time())
        self.date_button.text = value.strftime("%Y-%m-%d")

    def add_transaction(self, instance):
        """Add transaction to database"""
        try:
            amount = float(self.amount_field.text)
            description = self.description_field.text.strip()
            
            if amount <= 0:
                Snackbar(text="Please enter a valid amount").open()
                return
            
            if not description:
                Snackbar(text="Please enter a description").open()
                return

            success = self.data.add_transaction(
                amount=amount,
                description=description,
                transaction_type=self.current_transaction_type,
                category=self.selected_category,
                date=self.selected_date
            )

            if success:
                self.add_dialog.dismiss()
                self.update_dashboard()
                Snackbar(text="Transaction added successfully!").open()
            else:
                Snackbar(text="Failed to add transaction").open()

        except ValueError:
            Snackbar(text="Please enter a valid amount").open()

    def view_all_transactions(self, instance):
        """Navigate to transactions screen"""
        self.manager.current = "transactions"

    def update_dashboard(self):
        """Update dashboard with current data"""
        if not self.data:
            return

        # Update balance
        balance = self.data.get_balance()
        self.balance_amount.text = f"{abs(balance):,.2f}"
        
        # Update balance trend
        if balance > 0:
            self.balance_trend.text = "📈 Looking good!"
            self.balance_card.md_bg_color = get_color_from_hex("#4ECDC4")
        elif balance == 0:
            self.balance_trend.text = "➖ Break even"
            self.balance_card.md_bg_color = get_color_from_hex("#95a5a6")
        else:
            self.balance_trend.text = "📉 Watch your spending!"
            self.balance_card.md_bg_color = get_color_from_hex("#e74c3c")

        # Update monthly stats
        monthly_stats = self.data.get_period_stats(30)
        self.income_amount.text = f"{monthly_stats['income']:,.2f}"
        self.expense_amount.text = f"{monthly_stats['expenses']:,.2f}"

        # Update recent transactions
        self.update_recent_transactions()

    def update_recent_transactions(self):
        """Update recent transactions list"""
        self.recent_list.clear_widgets()
        
        recent_transactions = self.data.transactions[:5]  # Show last 5 transactions
        
        if not recent_transactions:
            no_data_item = OneLineListItem(
                text="No transactions yet",
                theme_text_color="Hint"
            )
            self.recent_list.add_widget(no_data_item)
            return

        for transaction in recent_transactions:
            # Get category emoji
            categories = (self.data.INCOME_CATEGORIES if transaction.transaction_type == TransactionType.INCOME 
                         else self.data.EXPENSE_CATEGORIES)
            emoji = "💰"
            for cat_emoji, cat_name in categories:
                if cat_name == transaction.category:
                    emoji = cat_emoji
                    break

            # Format amount with currency
            amount_text = self.data.format_amount(transaction.amount)
            if transaction.transaction_type == TransactionType.EXPENSE:
                amount_text = f"-{amount_text}"
            else:
                amount_text = f"+{amount_text}"

            item = ThreeLineListItem(
                text=f"{emoji} {transaction.description}",
                secondary_text=f"{transaction.category} • {transaction.date.strftime('%Y-%m-%d')}",
                tertiary_text=amount_text,
                on_release=lambda x, t=transaction: self.show_transaction_details(t)
            )
            self.recent_list.add_widget(item)

    def show_add_transaction_dialog(self, transaction_type):
  

        # Save selection state
        categories = (self.data.INCOME_CATEGORIES if transaction_type == TransactionType.INCOME 
                    else self.data.EXPENSE_CATEGORIES)
        self.selected_category = categories[0][1]
        self.selected_date = datetime.now()
        self.current_transaction_type = transaction_type

        # Create the actual layout for dialog content
        self.amount_field = MDTextField(
            hint_text="Amount",
            helper_text="Enter amount",
            helper_text_mode="on_focus",
            icon_right="currency-inr",
        )

        self.description_field = MDTextField(
            hint_text="Description",
            helper_text="Enter description",
            helper_text_mode="on_focus",
            icon_right="text",
        )

        self.category_button = MDRaisedButton(
            text=f"{categories[0][0]} {categories[0][1]}",
            on_release=lambda x: self.open_category_menu(categories, transaction_type)
        )

        self.date_button = MDRaisedButton(
            text=self.selected_date.strftime("%Y-%m-%d"),
            on_release=self.open_date_picker
        )

        # Use MDBoxLayout without height problems
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(240)  # enough to fit all widgets without scroll
        )

        content.add_widget(self.amount_field)
        content.add_widget(self.description_field)
        content.add_widget(self.category_button)
        content.add_widget(self.date_button)

        title = "Add Income" if transaction_type == TransactionType.INCOME else "Add Expense"

        self.add_dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,  # 👈 Directly adding layout (no scroll!)
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.add_dialog.dismiss()),
                MDRaisedButton(text="ADD", on_release=self.add_transaction)
            ]
        )
        self.add_dialog.open()


    def delete_transaction(self, transaction_id):
        """Delete transaction"""
        if self.data.delete_transaction(transaction_id):
            self.transaction_dialog.dismiss()
            self.update_dashboard()
            Snackbar(text="Transaction deleted successfully!").open()
        else:
            Snackbar(text="Failed to delete transaction").open()

    def on_enter(self):
        """Called when screen is entered"""
        if self.data:
            self.update_currency_display()
            self.update_dashboard()

class TransactionsScreen(MDScreen):
    """Screen for viewing all transactions"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.build_ui()

    def build_ui(self):
        # Main layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20)
        )

        # Header
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )

        back_button = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back
        )

        title_label = MDLabel(
            text="All Transactions",
            font_style="H5",
            theme_text_color="Primary",
            bold=True
        )

        filter_button = MDIconButton(
            icon="filter-variant",
            on_release=self.show_filter_dialog
        )

        header.add_widget(back_button)
        header.add_widget(title_label)
        header.add_widget(filter_button)

        # Filters
        self.filter_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )

        self.filter_chips = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(5),
            size_hint_y=None,
            height=dp(40)
        )

        # Add default filter chips
        self.add_filter_chip("All", True)
        self.add_filter_chip("Income", False)
        self.add_filter_chip("Expense", False)

        self.filter_layout.add_widget(self.filter_chips)

        # Transactions list
        self.transactions_scroll = MDScrollView()
        self.transactions_list = MDList()
        self.transactions_scroll.add_widget(self.transactions_list)

        # Add widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(self.filter_layout)
        main_layout.add_widget(self.transactions_scroll)

        self.add_widget(main_layout)

        # Current filter
        self.current_filter = "All"

    def add_filter_chip(self, text, is_selected=False):
    
        chip = MDChip(text=text)
    
    # Set default or selected background
        chip.md_bg_color = (0.3, 0.7, 0.6, 1) if is_selected else (0.9, 0.9, 0.9, 1)
        chip.text_color = (1, 1, 1, 1)

        # Assign callback after creation to avoid UnboundLocalError
        chip.on_release = lambda x=chip, t=text: self.on_chip_selected(x, t)

        self.filter_chips.add_widget(chip)

    def on_chip_selected(self, selected_chip, filter_type):
    
        self.current_filter = filter_type

        for chip in self.filter_chips.children:
            chip.md_bg_color = (0.9, 0.9, 0.9, 1)  # Unselected
        selected_chip.md_bg_color = (0.3, 0.7, 0.6, 1)  # Selected

        self.update_transactions_list()



    def show_filter_dialog(self, instance):
        """Show advanced filter dialog"""
        # This could be expanded to include date range, category filters, etc.
        pass

    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = "dashboard"

    def update_transactions_list(self):
        """Update transactions list based on current filter"""
        if not self.data:
            return

        self.transactions_list.clear_widgets()
        
        transactions = self.data.transactions
        
        # Apply filter
        if self.current_filter == "Income":
            transactions = [t for t in transactions if t.transaction_type == TransactionType.INCOME]
        elif self.current_filter == "Expense":
            transactions = [t for t in transactions if t.transaction_type == TransactionType.EXPENSE]

        if not transactions:
            no_data_item = OneLineListItem(
                text="No transactions found",
                theme_text_color="Hint"
            )
            self.transactions_list.add_widget(no_data_item)
            return

        for transaction in transactions:
            # Get category emoji
            categories = (self.data.INCOME_CATEGORIES if transaction.transaction_type == TransactionType.INCOME 
                         else self.data.EXPENSE_CATEGORIES)
            emoji = "💰"
            for cat_emoji, cat_name in categories:
                if cat_name == transaction.category:
                    emoji = cat_emoji
                    break

            # Format amount with currency
            amount_text = self.data.format_amount(transaction.amount)
            if transaction.transaction_type == TransactionType.EXPENSE:
                amount_text = f"-{amount_text}"
            else:
                amount_text = f"+{amount_text}"

            item = ThreeLineListItem(
                text=f"{emoji} {transaction.description}",
                secondary_text=f"{transaction.category} • {transaction.date.strftime('%Y-%m-%d')}",
                tertiary_text=amount_text,
                on_release=lambda x, t=transaction: self.show_transaction_details(t)
            )
            self.transactions_list.add_widget(item)

    def show_transaction_details(self, transaction):
        """Show transaction details dialog"""
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(200)
        )

        # Transaction details
        details = [
            ("Amount:", self.data.format_amount(transaction.amount)),
            ("Type:", transaction.transaction_type.value.title()),
            ("Category:", transaction.category),
            ("Date:", transaction.date.strftime("%Y-%m-%d %H:%M")),
            ("Description:", transaction.description)
        ]

        for label, value in details:
            detail_layout = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(30)
            )
            
            detail_layout.add_widget(MDLabel(
                text=label,
                theme_text_color="Primary",
                size_hint_x=0.4,
                bold=True
            ))
            
            detail_layout.add_widget(MDLabel(
                text=value,
                theme_text_color="Secondary",
                size_hint_x=0.6
            ))
            
            content.add_widget(detail_layout)

        self.transaction_dialog = MDDialog(
            title="Transaction Details",
            content=content,
            buttons=[
                MDFlatButton(
                    text="DELETE",
                    theme_text_color="Error",
                    on_release=lambda x: self.delete_transaction(transaction.id)
                ),
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: self.transaction_dialog.dismiss()
                )
            ]
        )
        self.transaction_dialog.open()

    def delete_transaction(self, transaction_id):
        """Delete transaction"""
        if self.data.delete_transaction(transaction_id):
            self.transaction_dialog.dismiss()
            self.update_transactions_list()
            Snackbar(text="Transaction deleted successfully!").open()
        else:
            Snackbar(text="Failed to delete transaction").open()

    def on_enter(self):
        """Called when screen is entered"""
        if self.data:
            self.update_transactions_list()

class StatsScreen(MDScreen):
    """Screen for viewing statistics"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.build_ui()

    def build_ui(self):
        # Main scrollable layout
        scroll = MDScrollView()
        main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Header
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )

        back_button = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back
        )

        title_label = MDLabel(
            text="📊 Statistics",
            font_style="H5",
            theme_text_color="Primary",
            bold=True
        )

        header.add_widget(back_button)
        header.add_widget(title_label)

        # Period selector
        period_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )

        period_chips = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(5),
            size_hint_y=None,
            height=dp(40)
        )

        # Add period chips
        periods = [("7 Days", 7), ("30 Days", 30), ("90 Days", 90), ("1 Year", 365)]
        for i, (text, days) in enumerate(periods):
            chip = MDChip(text=text)

        # Set selection appearance
            chip.md_bg_color = (0.3, 0.7, 0.6, 1) if i == 1 else (0.9, 0.9, 0.9, 1)
            chip.text_color = (1, 1, 1, 1)

            # Assign callback after chip is created
            chip.on_release = lambda x=chip, d=days: self.on_period_chip_selected(x, d)

            period_chips.add_widget(chip)


        # Summary cards
        self.summary_layout = MDGridLayout(
            cols=2,
            spacing=dp(15),
            size_hint_y=None,
            height=dp(280)
        )

        # Income summary card
        self.income_summary_card = AnimatedCard(
            md_bg_color=get_color_from_hex("#4ECDC4"),
            padding=dp(20),
            elevation=8
        )

        income_summary_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        income_summary_layout.add_widget(MDLabel(
            text="💚 Total Income",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        self.income_summary_amount = MDLabel(
            text="$0.00",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )

        self.income_summary_count = MDLabel(
            text="0 transactions",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(25)
        )

        income_summary_layout.add_widget(self.income_summary_amount)
        income_summary_layout.add_widget(self.income_summary_count)
        self.income_summary_card.add_widget(income_summary_layout)

        # Expense summary card
        self.expense_summary_card = AnimatedCard(
            md_bg_color=get_color_from_hex("#FF6B6B"),
            padding=dp(20),
            elevation=8
        )

        expense_summary_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        expense_summary_layout.add_widget(MDLabel(
            text="💸 Total Expenses",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            size_hint_y=None,
            height=dp(30)
        ))

        self.expense_summary_amount = MDLabel(
            text="$0.00",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H4",
            bold=True,
            size_hint_y=None,
            height=dp(50)
        )

        self.expense_summary_count = MDLabel(
            text="0 transactions",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            font_style="Subtitle2",
            size_hint_y=None,
            height=dp(25)
        )

        expense_summary_layout.add_widget(self.expense_summary_amount)
        expense_summary_layout.add_widget(self.expense_summary_count)
        self.expense_summary_card.add_widget(expense_summary_layout)

        self.summary_layout.add_widget(self.income_summary_card)
        self.summary_layout.add_widget(self.expense_summary_card)

        # Category breakdown
        self.category_header = MDLabel(
            text="📈 Category Breakdown",
            font_style="H6",
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )

        # Income categories
        self.income_categories_card = MDCard(
            elevation=4,
            radius=[10],
            padding=dp(15),
            size_hint_y=None,
            height=dp(200)
        )

        income_categories_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        income_categories_layout.add_widget(MDLabel(
            text="💚 Income Categories",
            font_style="Subtitle1",
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        ))

        self.income_categories_list = MDList()
        income_categories_scroll = MDScrollView()
        income_categories_scroll.add_widget(self.income_categories_list)
        income_categories_layout.add_widget(income_categories_scroll)

        self.income_categories_card.add_widget(income_categories_layout)

        # Expense categories
        self.expense_categories_card = MDCard(
            elevation=4,
            radius=[10],
            padding=dp(15),
            size_hint_y=None,
            height=dp(200)
        )

        expense_categories_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        expense_categories_layout.add_widget(MDLabel(
            text="💸 Expense Categories",
            font_style="Subtitle1",
            theme_text_color="Primary",
            bold=True,
            size_hint_y=None,
            height=dp(30)
        ))

        self.expense_categories_list = MDList()
        expense_categories_scroll = MDScrollView()
        expense_categories_scroll.add_widget(self.expense_categories_list)
        expense_categories_layout.add_widget(expense_categories_scroll)

        self.expense_categories_card.add_widget(expense_categories_layout)

        # Add all widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(period_layout)
        main_layout.add_widget(self.summary_layout)
        main_layout.add_widget(self.category_header)
        main_layout.add_widget(self.income_categories_card)
        main_layout.add_widget(self.expense_categories_card)

        scroll.add_widget(main_layout)
        self.add_widget(scroll)

        # Current period
        self.current_period = 30

    def change_period(self, days):
        """Change statistics period"""
        self.current_period = days
        
        # Update chip selection
        for chip in self.parent.children[0].children[1].children[0].children:
            if hasattr(chip, 'text'):
                chip.selected = (f"{days} Days" in chip.text or 
                               (days == 365 and "1 Year" in chip.text))
        
        self.update_stats()

    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = "dashboard"

    def update_stats(self):
        """Update statistics display"""
        if not self.data:
            return

        # Get period stats
        stats = self.data.get_period_stats(self.current_period)
        
        # Update summary cards
        self.income_summary_amount.text = self.data.format_amount(stats['income'])
        self.expense_summary_amount.text = self.data.format_amount(stats['expenses'])
        
        # Count transactions
        cutoff = datetime.now() - timedelta(days=self.current_period)
        recent_transactions = [t for t in self.data.transactions if t.date >= cutoff]
        income_count = len([t for t in recent_transactions if t.transaction_type == TransactionType.INCOME])
        expense_count = len([t for t in recent_transactions if t.transaction_type == TransactionType.EXPENSE])
        
        self.income_summary_count.text = f"{income_count} transactions"
        self.expense_summary_count.text = f"{expense_count} transactions"

        # Update category breakdowns
        self.update_category_breakdown()

    def update_category_breakdown(self):
        """Update category breakdown lists"""
        # Clear existing items
        self.income_categories_list.clear_widgets()
        self.expense_categories_list.clear_widgets()

        # Get category stats
        income_categories = self.data.get_category_stats(TransactionType.INCOME, self.current_period)
        expense_categories = self.data.get_category_stats(TransactionType.EXPENSE, self.current_period)

        # Update income categories
      
# Update income categories (completing the incomplete section)
        if income_categories:
            sorted_income = sorted(income_categories.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_income:
                # Get emoji for category
                emoji = "💰"
                for cat_emoji, cat_name in self.data.INCOME_CATEGORIES:
                    if cat_name == category:
                        emoji = cat_emoji
                        break
                
                item = TwoLineIconListItem(
                    text=f"{emoji} {category}",
                    secondary_text=f"{self.data.format_amount(amount)}",
                    _icon=emoji,
                    theme_text_color="Primary"
                )
                self.income_categories_list.add_widget(item)
        else:
            self.income_categories_list.add_widget(
                OneLineListItem(text="No income data", theme_text_color="Hint")
            )

        # Update expense categories (completing the incomplete section)
        if expense_categories:
            sorted_expense = sorted(expense_categories.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_expense:
                emoji = "💸"
                for cat_emoji, cat_name in self.data.EXPENSE_CATEGORIES:
                    if cat_name == category:
                        emoji = cat_emoji
                        break
                
                item = TwoLineIconListItem(
                    text=f"{emoji} {category}",
                    secondary_text=f"{self.data.format_amount(amount)}",
                    _icon=emoji,
                    theme_text_color="Primary"
                )
                self.expense_categories_list.add_widget(item)
        else:
            self.expense_categories_list.add_widget(
                OneLineListItem(text="No expense data", theme_text_color="Hint")
            )

    def on_enter(self):
        """Called when screen is entered"""
        if self.data:
            self.update_stats()


# Additional utility classes that might be needed
class AnimatedCard(MDCard):
    """Animated card with hover effects"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_touch_down=self.on_touch_down_event)
        self.bind(on_touch_up=self.on_touch_up_event)
    
    def on_touch_down_event(self, instance, touch):
        if self.collide_point(*touch.pos):
            self.elevation = 12
            return True
        return False
    
    def on_touch_up_event(self, instance, touch):
        self.elevation = 8
        return False


# Main App class to tie everything together
class FinanceApp(MDApp):
    """Main application class"""
    
    def build(self):
        """Build the app"""
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        # Create screen manager
        sm = ScreenManager()
        
        # Create data handler
        data_handler = DataHandler()
        
        # Create screens
        dashboard = DashboardScreen(name="dashboard")
        transactions = TransactionsScreen(name="transactions")
        stats = StatsScreen(name="stats")
        
        # Set data handler for all screens
        dashboard.data = data_handler
        transactions.data = data_handler
        stats.data = data_handler
        
        # Add screens to manager
        sm.add_widget(dashboard)
        sm.add_widget(transactions)
        sm.add_widget(stats)
        
        return sm


if __name__ == "__main__":
    FinanceApp().run()
