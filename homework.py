import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Сохраняем новую запись объекта Record"""
        self.records.append(record)

    def get_today_stats(self):
        """Получаем траты за сегодня числом(integer)"""
        result = sum([record.amount for record in self.records if record.date == dt.date.today()])
        return result

    def get_week_stats(self):
        """Получаем траты за неделю числом(integer)"""
        today = dt.date.today()
        week_ago = dt.date.today() - dt.timedelta(days=7)
        result = sum([record.amount for record in self.records if week_ago <= record.date <= today])
        return result

    def get_balance(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Узнаём не превышен ли объём калорий за сегодня"""

    def get_calories_remained(self):
        calories_can_eat = self.get_balance()

        if calories_can_eat > 0:
            result = f'Сегодня можно съесть что-нибудь ещё, ' \
                     f'но с общей калорийностью не более {calories_can_eat} кКал'
        else:
            result = 'Хватит есть!'

        return result


class CashCalculator(Calculator):
    """Текущие курсы валют"""
    USD_RATE = 76.08
    EURO_RATE = 89.94

    def get_currency_cash(self, currency_rate):
        return round(abs(self.get_balance() / currency_rate), 2)

    def get_today_cash_remained(self, abbr):
        """Узнаём сколько осталось на счету"""
        cash_today_remained = self.get_balance()

        currency_dict = {
            'usd': {'rate': self.USD_RATE, 'currency': 'USD'},
            'eur': {'rate': self.EURO_RATE, 'currency': 'Euro'},
            'rub': {'rate': 1, 'currency': 'руб'},
        }

        currency_cash = self.get_currency_cash(currency_dict[abbr]["rate"])
        abbreviation = currency_dict[abbr]["currency"]

        if cash_today_remained > 0:
            result = f'На сегодня осталось {currency_cash} {abbreviation}'
        elif cash_today_remained == 0:
            result = 'Денег нет, держись'
        else:
            result = f'Денег нет, держись: твой долг - {currency_cash} {abbreviation}'

        return result


class Record:
    """Класс делающий запись трат за конкретную дату"""

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date != None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()
