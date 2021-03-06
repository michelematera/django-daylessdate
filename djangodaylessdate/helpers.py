from django.utils.dates import MONTHS


class DaylessDate:

    def __init__(self, month, year):
        self.month = month
        self.year = year
        self._validate()

    def _validate(self):
        try:
            self.month = int(self.month)
        except ValueError:
            raise Exception('Invalid month')

        try:
            self.year = int(self.year)
        except ValueError:
            raise Exception('Invalid year')

        if self.month not in (range(1, 13)):
            raise Exception('Invalid month')

        if self.year < 2000 or self.year > 2050:
            raise Exception('Invalid year')

    @property
    def month_name(self):
        return MONTHS[self.month]

    def __str__(self):
        return '{} {}'.format(self.month_name, self.year)

    def __eq__(self, other):
        if not isinstance(other, DaylessDate):
            return False
        return (self.month == other.month) and (self.year == other.year)

    def __gt__(self, other):
        if self.year != other.year:
            return self.year > other.year
        return self.month > other.month

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return (self > other) or self == other

    def __lt__(self, other):
        return not self >= other
