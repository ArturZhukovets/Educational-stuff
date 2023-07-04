from django.test import SimpleTestCase
from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):

    def test_expense_form_is_valid(self):
        data = {
            "title": "SomeTestTitle",
            "amount": 10_000,
            "category": "SomeTestCategory"
        }
        self.assertTrue(ExpenseForm(data=data).is_valid())

    def test_expense_form_no_data(self):
        data = {}
        self.assertFalse(ExpenseForm(data=data).is_valid())
