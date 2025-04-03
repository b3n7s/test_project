import os
import time
import logging
import allure
import requests


class TempMailService:
    def __init__(self):
        self.base_url = os.getenv("TEMP_MAIL_HOST")
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.email = None
        self.key = None

    @allure.step("Создание временного email")
    def create_temp_email(self) -> str:
        """Создание временного email адреса"""
        try:
            response = self.session.get(f"{self.base_url}", params={"action": "new"})
            response.raise_for_status()
            email = response.json().get("email")
            key = response.json().get("key")
            if email is None or key is None:
                self.logger.error(f"Ошибка при создании временного email: {response.json()}")
                raise Exception()
            self.email = email
            self.key = key
            self.logger.info(f"Создан временный email: {email}")
            return email, key
        except Exception as e:
            self.logger.error(f"Ошибка при создании временного email: {str(e)}")
            raise

    @allure.step("Получение писем")
    def get_emails(self) -> list:
        """Получение списка писем для указанного email"""
        try:
            response = self.session.get(f"{self.base_url}", params={"action": "getlist", "key": self.key})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Ошибка при получении писем: {str(e)}")
            raise
    
    @allure.step("Получение содержимого письма")
    def get_email_data(self, id_: int):
        """Получение текста письма"""
        try:
            response = self.session.get(f"{self.base_url}", params={"action": "getmail", "key": self.key, "id": id_})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Ошибка при получении писем: {str(e)}")
            raise
    
    @allure.step("Получение ссылки подтверждения из письма")
    def get_confirmation_link(self, max_attempts: int = 10, delay: int = 5) -> str:
        """Получение ссылки подтверждения из письма"""
        for attempt in range(max_attempts):
            try:
                emails = self.get_emails()
                if emails:
                    for email_data in emails:
                        id_ = email_data["id"]
                        if "подтверждение" in email_data["subject"].lower():
                            body = self.get_email_data(id_)
                            import re
                            link_match = re.search(r'href="([^"]+)"', body)
                            if link_match:
                                confirmation_link = link_match.group(1)
                                self.logger.info(f"Найдена ссылка подтверждения: {confirmation_link}")
                                return confirmation_link
                
                self.logger.info(f"Попытка {attempt + 1}: письмо с подтверждением не найдено")
                time.sleep(delay)
            except Exception as e:
                self.logger.error(f"Ошибка при получении ссылки подтверждения: {str(e)}")
                time.sleep(delay)
        
        raise Exception("Не удалось получить ссылку подтверждения")

    @allure.step("Удаление временного email")
    def delete_temp_email(self, email: str) -> None:
        """Удаление временного email адреса"""
        try:
            response = self.session.delete(f"{self.base_url}", params={"action": "delete"})
            response.raise_for_status()
            self.logger.info(f"Временный email удален: {email}")
        except Exception as e:
            self.logger.error(f"Ошибка при удалении временного email: {str(e)}")
            raise
