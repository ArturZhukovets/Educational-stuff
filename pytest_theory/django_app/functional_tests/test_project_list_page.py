from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.parse import urljoin

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from budget.models import Project, Expense, Category
from django.urls import reverse


class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self) -> None:
        service = ChromeService(executable_path="chromedriver")
        self.browser = webdriver.Chrome(service=service)

    def tearDown(self) -> None:
        self.browser.close()

    def test_project_list_page(self):
        # The user requests for the page for the first time
        self.browser.get(self.live_server_url)
        alert = self.browser.find_element(by="class name", value="noproject-wrapper")
        self.assertEqual(
            alert.find_element(by=By.TAG_NAME, value="h3").text,
            "Sorry, you don't have any projects, yet."
        )

    def test_redirect_if_no_projects_initialized_yet(self):
        # The user requests for the page for the first time
        self.browser.get(self.live_server_url)
        add_url = self.live_server_url + reverse("budget:add")
        print(f"ADD URL: {add_url}")
        self.browser.find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(
            self.browser.current_url,
            add_url
        )

    def test_user_sees_initialized_projects(self):
        project = Project.objects.create(
            name="SomeProject",
            budget=10_000,
        )
        self.browser.get(self.live_server_url)
        # The user sees the project on the screen
        self.assertEqual(
            self.browser.find_element(by=By.TAG_NAME, value="h5").text,
            project.name
        )

    def test_detail_page_redirect_user_after_click(self):
        project = Project.objects.create(
            name="SomeProject",
            budget=10_000,
        )
        detail_url = urljoin(self.live_server_url, reverse("budget:detail", args=[project.slug]))
        self.browser.get(url=self.live_server_url)
        self.browser.find_element(by=By.TAG_NAME, value="a").click()
        self.assertEqual(self.browser.current_url, detail_url)








