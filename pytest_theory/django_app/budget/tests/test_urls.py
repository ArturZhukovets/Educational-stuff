from django.test import SimpleTestCase
from django.urls import reverse, resolve

from budget.views import project_list, project_detail, ProjectCreateView


class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse("budget:list")
        print(url)
        self.assertEqual(resolve(url).func, project_list)
        self.assertEqual(resolve(url).url_name, "list")

    def test_project_detail_url_is_resolved(self):
        url = reverse("budget:detail", args=["some-slug-arg"])
        print(url)
        self.assertEqual(resolve(url).func, project_detail)
        self.assertEqual(resolve(url).url_name, "detail")

    def test_project_create_url_is_resolved(self):
        url = reverse("budget:add")
        print(url)
        self.assertEqual(resolve(url).func.view_class, ProjectCreateView)
        self.assertEqual(resolve(url).url_name, "add")

    def test_page_not_found(self):
        url = "/some-not-existing-url/15/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
