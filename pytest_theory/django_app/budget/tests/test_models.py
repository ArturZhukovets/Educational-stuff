from django.test import TestCase, Client
from django.urls import reverse

from budget.models import Project, Expense, Category


class TestModels(TestCase):

    def setUp(self) -> None:
        self.project_1 = Project.objects.create(
            name="Test Project Name 1",
            budget=10_000,
        )

    def test_project_is_slugged_correctly(self):
        self.assertEqual(self.project_1.slug, "test-project-name-1")

    def test_budget_left_property(self):
        test_category = Category.objects.create(project=self.project_1, name="design")
        _expense = Expense.objects.create(project=self.project_1, title="specialists", amount=730, category=test_category)
        _expense_2 = Expense.objects.create(project=self.project_1, title="specialists", amount=1870, category=test_category)
        self.assertEqual(self.project_1.budget_left, 10_000 - 730 - 1870)

    def test_total_transactions_property(self):
        test_category = Category.objects.create(project=self.project_1, name="design")
        other_project = Project.objects.create(name="Test project 2", budget=100_000)
        _amount = 1_000
        _num_of_transactions = 5

        Expense.objects.create(project=other_project, title="add", amount=_amount, category=test_category)

        for _ in range(_num_of_transactions):
            Expense.objects.create(
                project=self.project_1,
                title="specialists",
                amount=_amount,
                category=test_category,
            )
            _amount += 1000

        self.assertEqual(self.project_1.total_transactions, _num_of_transactions)

    def test_project_get_absolute_url(self):
        expected_url = "/budget/" + self.project_1.slug + "/"
        self.assertEqual(self.project_1.get_absolute_url(), expected_url)
