import random

from django.db import models

# Create your models here.


class TextLog(models.Model):
    ONE = "One"
    TWO = "Two"
    THREE = "Three"
    CHOICES = (
        (ONE, "One Million Dollars"),
        (TWO, "Two Million Dollars"),
        (THREE, "Three Million Dollars"),
    )
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField()
    some_str_field = models.CharField(default="Strange reaction")
    some_choices_field = models.CharField(choices=CHOICES, default=ONE, max_length=5)

    def save(self, *args, **kwargs) -> None:
        if "update_fields" not in kwargs:
            super(TextLog, self).save()
        else:
            super(TextLog, self).save(update_fields=kwargs.get('update_fields'))

    def __str__(self) -> str:
        return f"Message - {self.message}\nSome str field - {self.some_str_field}\nChoice field - {self.some_choices_field}"

    def random_choice(self):
        choice = self.some_choices_field
        while choice == self.some_choices_field:
            choice = random.choice([self.ONE, self.TWO, self.THREE])
        return choice
