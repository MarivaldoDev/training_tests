from selenium.webdriver.common.by import By

from .base import TaskBaseFunctionalTest


class TaskHomePageFunctionalTest(TaskBaseFunctionalTest):
    def test_task_home_page_return_welcome_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.CLASS_NAME, "hero-title")

        self.assertIn("Bem-vindo ao Task Manager", body.text)
