import datetime as dt
from typing import Optional, List, Dict


class Record:
    def __init__(self, amount: int, comment: str,
                 date: Optional[str] = None) -> None:
        """Конструктор класса."""
        self.amount = amount
        self.comment = comment
        self.DATE_FORMAT: str = '%d.%m.%Y'
        if date is not None:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()
        else:
            self.date = dt.date.today()


class Calculator:
    # Стоит ли анторировать в конструкторе, перменные которые берутся
    # из функции конструктора?
    def __init__(self, limit: int) -> None:
        self.records: List = []
        self.limit = limit

    def add_record(self, record: Record) -> None:
        """Добавление записи."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        today_amount: int = 0
        # Стоит ли сокращать до двух строк в цикл for c тернарным оператором?
        for record in self.records:
            if dt.date.today() == record.date:
                today_amount += record.amount
        return today_amount

    def get_week_stats(self) -> int:
        week_amount: int = 0
        start_week = dt.date.today()
        end_week = start_week - dt.timedelta(days=6)
        # Стоит ли сокращать до двух строк в цикл for c тернарным оператором?
        for record in self.records:
            if start_week >= record.date >= end_week:
                week_amount += record.amount
        return week_amount

    def difference(self) -> int:
        """Сравниваем дневную статистику с лимитом"""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        if(self.difference() > 0):
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.difference()} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE: float = 60.0
    EURO_RATE: float = 70.0

    A_C: Dict = {
        'usd': ['USD', USD_RATE],
        'eur': ['Euro', EURO_RATE],
        'rub': ['руб', 1]
    }

    def get_today_cash_remained(self, currency: str) -> str:
        if currency in self.A_C:
            currency_name: str = self.A_C[currency][0]
        else:
            return 'Нет такой валюты'

        balance: int = (round(((self.limit - self.get_today_stats())
                        / self.A_C[currency][1]), 2))

        if balance < 0:
            balance = -balance

        if self.difference() > 0:
            return f'На сегодня осталось {balance} {currency_name}'
        if self.difference() == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {balance} {currency_name}'


if __name__ == "__main__":

    cash_calculator = CashCalculator(0)
    cash_calculator.add_record(Record(amount=84, comment='Йогурт.',
                                      date='23.02.2019'))
    cash_calculator.add_record(Record(amount=1140, comment='Баночка чипсов.'))
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='07.10.2021'))

    cash_calculator.get_today_stats()
    cash_calculator.get_week_stats()
    print(cash_calculator.get_today_cash_remained('eur'))
