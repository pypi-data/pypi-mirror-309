from typing import Optional


class Frequency:
    def __init__(self, frequency: str, date: Optional[str] = None):
        self.frequency = frequency
        self.date = date

    def __eq__(self, other):
        return self.frequency == other.frequency and self.date == other.date

    def __repr__(self):
        return (
            f'Frequency(frequency="{self.frequency}", date="{self.date})"'
            if self.date
            else f'Frequency(frequency="{self.frequency}")'
        )

    def to_dict(self):
        return (
            {"frequency": self.frequency, "date": self.date}
            if self.date
            else {"frequency": self.frequency}
        )
