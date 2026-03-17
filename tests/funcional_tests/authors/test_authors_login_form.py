import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseFuncionalTest


class AuthorsLoginFormFunctionalTest(AuthorsBaseFuncionalTest):
    def test_show_message_error_if_form_is_not_valid(self):
        self.browser.get(self.live_server_url + "/authors/login/")

        user = self.browser.find_element(By.ID, "id_username")
        password = self.browser.find_element(By.ID, "id_password")

        user.send_keys("invalid_user")
        password.send_keys("12345")
        password.send_keys(Keys.ENTER)

        time.sleep(5)

        message_erro = self.browser.find_element(By.CLASS_NAME, "message")

        self.assertIn(
            "Por favor, entre com um usuário e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.",
            message_erro.text,
        )
