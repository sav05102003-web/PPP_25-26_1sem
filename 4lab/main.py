import json
import abc
import sys

class CurrencyManager:
    base_currency = "RUB"
    rates = {}  

    @classmethod
    def set_base_currency(cls, code):
        cls.base_currency = code.upper()
        cls.rates[cls.base_currency] = 1.0

    @classmethod
    def add_rate(cls, code, rate):
        cls.rates[code.upper()] = float(rate)

    @classmethod
    def get_rate(cls, code):
        code = code.upper()
        if code not in cls.rates:
            raise ValueError(f"Неизвестная валюта: {code}")
        return cls.rates[code]

    @classmethod
    def convert_to_base(cls, amount, code):
        rate = cls.get_rate(code)
        return amount * rate

class Money(abc.ABC):
    def __init__(self, raw_value):
        self.raw_value = raw_value  
        self._amount = 0.0
        self._currency = CurrencyManager.base_currency
        self.parse_value() 

    @abc.abstractmethod
    def parse_value(self):
        pass

    def get_value_in_base(self):
        return CurrencyManager.convert_to_base(self._amount, self._currency)

    def __lt__(self, other):
        return self.get_value_in_base() < other.get_value_in_base()

    def __str__(self):
        base_val = self.get_value_in_base()
        if self._currency == CurrencyManager.base_currency:
            return f"{self._amount:.2f} {self._currency}"
        return f"{self._amount:.2f} {self._currency} = {base_val:.2f} {CurrencyManager.base_currency}"

class CodeMoney(Money):
    """Формат: code 1000 RUB"""
    def parse_value(self):
        parts = self.raw_value.strip().split()
        if len(parts) != 2:
            raise ValueError("Неверный формат code. Ожидается: ЧИСЛО КОД")
        self._amount = float(parts[0])
        self._currency = parts[1].upper()

class JsonMoney(Money):
    def parse_value(self):
        try:
            data = json.loads(self.raw_value)
            self._amount = float(data["amount"])
            self._currency = data["currency"].upper()
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")

class LocalMoney(Money):
    # Карта символов валют
    SYMBOL_MAP = {
        '₽': 'RUB', '$': 'USD', '€': 'EUR', '£': 'GBP', '¥': 'CNY'
    }

    def parse_value(self):
        s = self.raw_value.strip()
        found_symbol = None
        for symbol, code in self.SYMBOL_MAP.items():
            if symbol in s:
                found_symbol = symbol
                self._currency = code
                break
        
        if not found_symbol:
            raise ValueError("Не найден известный символ валюты (₽, $, € и т.д.)")

        number_str = s.replace(found_symbol, "").replace(" ", "").strip()
        number_str = number_str.replace(",", ".")
        
        self._amount = float(number_str)

class DefaultMoney(Money):
    def parse_value(self):
        self._amount = float(self.raw_value.strip())
        self._currency = CurrencyManager.base_currency

def create_money_object(line):
    try:
        prefix, content = line.split(maxsplit=1)
    except ValueError:
        return None,

    prefix = prefix.lower()
    
    try:
        if prefix == 'code':
            return CodeMoney(content), None
        elif prefix == 'json':
            return JsonMoney(content), None
        elif prefix == 'local':
            return LocalMoney(content), None
        elif prefix == 'default':
            return DefaultMoney(content), None
        else:
            return None, f"Неизвестный тип данных: {prefix}"
    except ValueError as e:
        return None, f"Ошибка данных в строке '{line}': {e}"

def main():
    print("--- Настройка системы ---")
    
    base_curr = input("Введите код базовой валюты (например, RUB): ").strip()
    if not base_curr:
        base_curr = "RUB"
    CurrencyManager.set_base_currency(base_curr)
    print(f"Базовая валюта установлена: {CurrencyManager.base_currency}")

    print("Введите курсы валют (формат: CODE RATE). Пустая строка для завершения:")
    while True:
        line = input().strip()
        if not line:
            break
        try:
            parts = line.split()
            if len(parts) == 2:
                code, rate = parts[0], parts[1]
                CurrencyManager.add_rate(code, rate)
            else:
                print("Ошибка формата. Используйте: ВАЛЮТА КУРС")
        except ValueError:
            print("Ошибка: курс должен быть числом.")

    money_collection = []

    print("\n--- Ввод данных ---")
    print("Введите суммы в форматах: code ..., json ..., local ..., default ...")
    print("Или введите команду (sum, max, min, list) для выполнения операции.")
    
    commands = {'sum', 'max', 'min', 'list', 'exit'}

    while True:
        line = input("> ").strip()
        if not line:
            continue

        if line.lower() in commands:
            cmd = line.lower()
            
            if not money_collection:
                print("Коллекция пуста.")
                continue

            if cmd == 'sum':
                total = sum(m.get_value_in_base() for m in money_collection)
                print(f"Total: {total:.2f} {CurrencyManager.base_currency}")
            
            elif cmd == 'max':
                max_obj = max(money_collection)
                print(f"Max: {max_obj}")
            
            elif cmd == 'min':
                min_obj = min(money_collection)
                print(f"Min: {min_obj}")
            
            elif cmd == 'list':
                print("Список всех сумм (нормализованный):")
                for m in money_collection:
                    print(m)
            
            elif cmd == 'exit':
                break
            
            continue

        obj, error = create_money_object(line)
        if obj:
            money_collection.append(obj)
        else:
            print(f"Ошибка: {error}")
main()
