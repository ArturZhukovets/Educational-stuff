import json
from django.test import TestCase, Client
from django.urls import reverse

from budget.models import Project, Category, Expense


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.list_url = reverse("budget:list")
        self.detail_url = reverse("budget:detail", args=["project-test"])
        self.create_url = reverse("budget:add")
        self.project_test_obj = Project.objects.create(
            name="project-test",
            budget=1_000_000,
        )
        self.category_test_obj = Category.objects.create(
            project=self.project_test_obj,
            name="development",
        )

    def test_project_list_GET(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "budget/project-list.html")

    def test_project_detail_test_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "budget/project-detail.html")

    def test_project_detail_POST_add_new_expense(self):
        """Test POST method of `project_detail`. When create new expense"""
        _payload_data = {
            "title": "some-expense",
            "amount": 1_000,
            "category": "development",
        }
        response = self.client.post(
            path=self.detail_url,
            data=_payload_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project_test_obj.expenses.first().title, "some-expense")

    def test_project_detail_POST_no_data(self):
        """Test POST method of `project_detail`. When no data specified"""

        response = self.client.post(path=self.detail_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project_test_obj.expenses.count(), 0)

    def test_project_detail_DELETE_expense(self):
        Expense.objects.create(
            project=self.project_test_obj,
            title="test_category",
            amount=250_000,
            category=self.category_test_obj,
        )

        response = self.client.delete(path=self.detail_url, data=json.dumps({"id": 1}))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.project_test_obj.expenses.count(), 0)

    def test_project_detail_DELETE_no_data(self):
        Expense.objects.create(
            project=self.project_test_obj,
            title="test_category",
            amount=250_000,
            category=self.category_test_obj,
        )

        response = self.client.delete(path=self.detail_url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.project_test_obj.expenses.count(), 1)

    def test_project_detail_DELETE_wrong_id(self):
        Expense.objects.create(
            project=self.project_test_obj,
            title="test_category",
            amount=250_000,
            category=self.category_test_obj,
        )

        response = self.client.delete(path=self.detail_url, data=json.dumps({"id": 8_000}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.project_test_obj.expenses.count(), 1)

    def test_project_create(self):
        """Test checks new created project and also checks created categories after usage endpoint `add`."""
        before_creating_count = Project.objects.count()
        before_categories_count = Category.objects.count()
        response = self.client.post(path=self.create_url, data={
            "name": "NewTestProject",
            "budget": 1000,
            "categoriesString": "TestCat1,TestCat2"
        })

        after_creating_count = Project.objects.count()
        after_categories_count = Category.objects.count()
        proj = Project.objects.get(name="NewTestProject", budget=1_000)
        first_created_category = Category.objects.filter(name="TestCat1").first()
        second_created_category = Category.objects.filter(name="TestCat2").first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(after_creating_count - before_creating_count, 1)
        self.assertEqual(Project.objects.last(), proj)

        self.assertEqual(after_categories_count - before_categories_count, 2)
        self.assertEqual(Category.objects.get(name="TestCat1"), first_created_category)
        self.assertEqual(Category.objects.get(name="TestCat2"), second_created_category)

