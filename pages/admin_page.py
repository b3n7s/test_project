import os
import allure
from typing import Optional
from pages.base_page import BasePage
from services.temp_mail_service import TempMailService

class AdminPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.temp_mail = TempMailService()
        
        # Селекторы элементов
        self.username_field = "input[id='username']"
        self.password_field = "input[id='password']"
        self.login_button = "button[id='js-sign-in-button']"
        self.users_link = "text=Пользователи"
        self.add_user_button = "text=Добавить пользователя"
        self.user_name = "input[id='user-name']"
        self.user_surname = "input[id='user-surname']"
        self.email_field = "input[id='user-email']"
        self.role_select = "div[role='combobox']"
        self.organizator = "text=Организатор"
        self.phone_number = "input[id='user-phone']"
        self.save_button = "text=Добавить"
        self.search_field = "input[placeholder='Поиск']"
        self.edit_button = "text=Редактировать"
        self.update_button = "text=Обновить"
        self.user_checkbox = "input[type='checkbox']"
        self.deactivate_button = "text=Деактивировать"
        self.user_status = "td:last-child"

    @allure.step("Открыть сайт")
    def open_site(self):
        """Открыть сайт через переход по ссылке"""
        self.open(os.getenv("AGROHELPER_HOST"))

    @allure.step("Авторизация администратора")
    def login_as_admin(self, username: str, password: str) -> None:
        """Авторизация под администратором"""
        self.fill(self.username_field, username)
        self.fill(self.password_field, password)
        self.click(self.login_button)
        self.wait_for_load_state()

    @allure.step("Переход в раздел пользователей")
    def navigate_to_users(self) -> None:
        """Переход в раздел пользователей"""
        self.click(self.users_link)
        self.wait_for_load_state()

    @allure.step("Открытие формы добавления пользователя")
    def open_add_user_form(self) -> None:
        """Открытие формы добавления пользователя"""
        self.click(self.add_user_button)
        self.wait_for_load_state()

    @allure.step("Заполнение формы регистрации организатора")
    def fill_organizer_registration_form(self, email: str) -> None:
        """Заполнение формы регистрации организатора"""
        self.fill(self.user_name, "Иван")
        self.fill(self.user_surname, "Иванов")
        self.click(self.role_select)
        self.click(self.organizator)
        self.fill(self.email_field, email)
        self.fill(self.phone_number, "+79000000032")

    @allure.step("Сохранение нового пользователя")
    def save_new_user(self) -> None:
        """Сохранение нового пользователя"""
        self.click(self.save_button)
        self.wait_for_load_state()

    @allure.step("Поиск пользователя по email")
    def search_user_by_email(self, email: str) -> None:
        """Поиск пользователя по email"""
        self.fill(self.search_field, email)
        self.wait_for_element(f"text={email}")

    @allure.step("Открытие профиля пользователя")
    def open_user_profile(self, email: str) -> None:
        """Открытие профиля пользователя"""
        self.click(f"text={email}")
        self.wait_for_load_state()

    @allure.step("Открытие формы редактирования пользователя")
    def open_edit_form(self) -> None:
        """Открытие формы редактирования пользователя"""
        self.click(self.edit_button)
        self.wait_for_load_state()

    @allure.step("Обновление email пользователя")
    def update_user_email(self, new_email: str) -> None:
        """Обновление email пользователя"""
        self.clear_input(self.email_field)
        self.fill(self.email_field, new_email)
        self.click(self.update_button)
        self.wait_for_load_state()

    @allure.step("Выбор пользователя в списке")
    def select_user(self, email: str) -> None:
        """Выбор пользователя в списке"""
        self.click(f"tr:has-text('{email}') {self.user_checkbox}")

    @allure.step("Деактивация пользователя")
    def deactivate_user(self) -> None:
        """Деактивация пользователя"""
        self.click(self.deactivate_button)
        self.wait_for_load_state()

    @allure.step("Проверка статуса пользователя")
    def check_user_status(self, email: str, expected_status: str) -> None:
        """Проверка статуса пользователя"""
        status = self.get_text(f"tr:has-text('{email}') {self.user_status}")
        assert status == expected_status, f"Статус пользователя {status} не соответствует ожидаемому {expected_status}"

    @allure.step("Получение ссылки подтверждения из временной почты")
    def get_confirmation_link(self, email: str) -> str:
        """Получение ссылки подтверждения из временной почты"""
        return self.temp_mail.get_confirmation_link(email)

    @allure.step("Завершение регистрации организатора")
    def complete_organizer_registration(self, email: str, username: str, password: str) -> None:
        """Завершение регистрации организатора"""
        confirmation_link = self.get_confirmation_link(email)
        self.open(confirmation_link)
        self.fill(self.username_field, username)
        self.fill(self.password_field, password)
        self.click(self.save_button)
        self.wait_for_load_state()

    @allure.step("Полный процесс регистрации организатора")
    def register_organizer(self, admin_email: str, admin_password: str, organizer_email: str, 
                         organizer_username: str, organizer_password: str) -> None:
        """Полный процесс регистрации организатора"""
        self.open_site()
        # Шаг 1: Авторизация администратора
        self.login_as_admin(admin_email, admin_password)
        
        # Шаг 2-5: Создание пользователя
        self.navigate_to_users()
        self.open_add_user_form()
        self.fill_organizer_registration_form(organizer_email)
        self.save_new_user()
        
        # Шаг 6-7: Завершение регистрации
        self.complete_organizer_registration(organizer_email, organizer_username, organizer_password)
        
        # Шаг 8-17: Редактирование и деактивация
        self.navigate_to_users()
        self.search_user_by_email(organizer_email)
        self.open_user_profile(organizer_email)
        self.open_edit_form()
        
        self.temp_mail.create_temp_email()
        new_email = f"{self.faker.word()}@{self.faker.word()}.ru"
        self.update_user_email(new_email)
        
        self.navigate_to_users()
        self.search_user_by_email(new_email)
        self.select_user(new_email)
        self.deactivate_user()
        self.check_user_status(new_email, "Не активен")
