import os
import pytest
import allure

from pages.admin_page import AdminPage


@allure.feature("Управление пользователями")
@allure.story("Регистрация организатора")
class TestOrganizerRegistration:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.admin_page = AdminPage(page)
        self.admin_email = os.getenv("ADMIN_EMAIL")
        self.admin_password = os.getenv("ADMIN_PASSWORD")
        self.organizer_username = "test_organizer"
        self.organizer_password = "Test123456!"
        yield

    @allure.title("Полный процесс регистрации и деактивации организатора")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_complete_organizer_registration_flow(self):
        """
        Тест проверяет полный процесс:
        1. Регистрации организатора администратором
        2. Подтверждения регистрации через email
        3. Редактирования данных организатора
        4. Деактивации организатора
        """
        with allure.step("Создание временного email для организатора"):
            temp_email, key = self.admin_page.temp_mail.create_temp_email()
        try:
            with allure.step("Выполнение полного процесса регистрации организатора"):
                self.admin_page.register_organizer(
                    admin_email=self.admin_email,
                    admin_password=self.admin_password,
                    organizer_email=temp_email,
                    organizer_username=self.organizer_username,
                    organizer_password=self.organizer_password
                )
        finally:
            with allure.step("Очистка: удаление временного email"):
                self.admin_page.temp_mail.delete_temp_email(temp_email)

    @allure.title("Проверка регистрации организатора с невалидными данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_organizer_registration_with_invalid_data(self):
        """
        Тест проверяет обработку невалидных данных при регистрации организатора:
        - Неверный формат email
        - Слишком короткий пароль
        - Пустые обязательные поля
        """
        with allure.step("Попытка регистрации с невалидным email"):
            self.admin_page.login_as_admin(self.admin_username, self.admin_password)
            self.admin_page.navigate_to_users()
            self.admin_page.open_add_user_form()
            
            # Попытка ввести невалидный email
            self.admin_page.fill_organizer_registration_form("invalid_email")
            self.admin_page.save_new_user()
            
            # Проверка сообщения об ошибке
            assert self.admin_page.is_element_visible("text=Неверный формат email")

    @allure.title("Проверка деактивации активного организатора")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_deactivate_active_organizer(self):
        """
        Тест проверяет процесс деактивации активного организатора:
        1. Создание организатора
        2. Проверка статуса "Активен"
        3. Деактивация
        4. Проверка статуса "Не активен"
        """
        with allure.step("Создание временного email для организатора"):
            temp_email = self.admin_page.temp_mail.create_temp_email()

        try:
            with allure.step("Регистрация организатора"):
                self.admin_page.login_as_admin(self.admin_username, self.admin_password)
                self.admin_page.navigate_to_users()
                self.admin_page.open_add_user_form()
                self.admin_page.fill_organizer_registration_form(temp_email)
                self.admin_page.save_new_user()
                self.admin_page.complete_organizer_registration(
                    temp_email, 
                    self.organizer_username, 
                    self.organizer_password
                )

            with allure.step("Проверка и деактивация организатора"):
                self.admin_page.navigate_to_users()
                self.admin_page.search_user_by_email(temp_email)
                self.admin_page.select_user(temp_email)
                self.admin_page.deactivate_user()
                self.admin_page.check_user_status(temp_email, "Не активен")

        finally:
            with allure.step("Очистка: удаление временного email"):
                self.admin_page.temp_mail.delete_temp_email(temp_email)

    @allure.title("Проверка редактирования данных организатора")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_organizer_data(self):
        """
        Тест проверяет процесс редактирования данных организатора:
        1. Создание организатора
        2. Изменение email
        3. Проверка обновленных данных
        """
        with allure.step("Создание временного email для организатора"):
            temp_email = self.admin_page.temp_mail.create_temp_email()

        try:
            with allure.step("Регистрация и редактирование данных организатора"):
                self.admin_page.login_as_admin(self.admin_username, self.admin_password)
                self.admin_page.navigate_to_users()
                self.admin_page.open_add_user_form()
                self.admin_page.fill_organizer_registration_form(temp_email)
                self.admin_page.save_new_user()
                self.admin_page.complete_organizer_registration(
                    temp_email, 
                    self.organizer_username, 
                    self.organizer_password
                )

                # Редактирование данных
                self.admin_page.navigate_to_users()
                self.admin_page.search_user_by_email(temp_email)
                self.admin_page.open_user_profile(temp_email)
                self.admin_page.open_edit_form()
                
                new_email = f"updated_{temp_email}"
                self.admin_page.update_user_email(new_email)
                
                # Проверка обновленных данных
                self.admin_page.navigate_to_users()
                self.admin_page.search_user_by_email(new_email)
                assert self.admin_page.is_element_visible(f"text={new_email}")

        finally:
            with allure.step("Очистка: удаление временного email"):
                self.admin_page.temp_mail.delete_temp_email(temp_email) 