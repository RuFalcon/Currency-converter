import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    now = dt.datetime.now()

    # Сохраняем новую запись объекта Record
    def add_record(self, record):
        self.records.append(record)

    # Получаем траты за сегодня числом(integer)
    def get_today_stats(self):
        result = 0
        for record in self.records:
            if record.date == self.now.date():
                result += record.amount

        return result

    # Получаем траты за неделю числом(integer)
    def get_week_stats(self):
        result = 0
        for record in self.records:
            if self.now.date() - dt.timedelta(days=7) <= record.date < self.now.date() + dt.timedelta(days=1):
                result += record.amount

        return result


class CaloriesCalculator(Calculator):
    # Узнаём не превышен ли объём калорий за сегодня
    def get_calories_remained(self):
        calories_today = self.get_today_stats()
        calories_can_eat = self.limit - calories_today

        if calories_today < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_can_eat} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    # Текущие курсы валют
    USD_RATE = 76.08
    EURO_RATE = 89.94

    # Узнаём сколько осталось на счету
    def get_today_cash_remained(self, currency):

        cash_today = self.get_today_stats()
        # Узнаём остаток или долг, округляем до положительного числа для правильного вывода
        cash_today_remained = abs(self.limit - cash_today)

        # Фильтруем вывод в зависимости от валюты
        if currency == 'usd':
            cash_today_remained = cash_today_remained / self.USD_RATE
            currency = 'USD'
        elif currency == 'eur':
            cash_today_remained = cash_today_remained / self.EURO_RATE
            currency = 'Euro'
        else:
            currency = 'руб'

        if cash_today < self.limit:
            return f'На сегодня осталось {cash_today_remained:.2f} {currency}'
        elif cash_today == self.limit:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {cash_today_remained:.2f} {currency}'


# Класс делающий запись трат за конкретную дату
class Record:
    def __init__(self, amount, comment, date=dt.datetime.today().strftime("%d.%m.%Y")):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
