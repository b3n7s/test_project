import os

from dotenv import load_dotenv
from locust import HttpUser, between, task

# Загружаем переменные окружения
load_dotenv()


class AgroHelperUser(HttpUser):
    # Время ожидания между запросами (в секундах)
    wait_time = between(1, 3)

    # Токен авторизации
    access_token = None

    def on_start(self):
        """Выполняется при старте каждого пользователя"""
        self.authenticate()

    def authenticate(self):
        """Аутентификация пользователя"""
        # Получаем CSRF токен
        csrf_response = self.client.get("/api/auth/csrf")
        if csrf_response.status_code != 200:
            raise Exception("Failed to get CSRF token")

        csrf_token = csrf_response.json().get("csrfToken")
        if not csrf_token:
            raise Exception("CSRF token not found in response")

        # Подготавливаем данные для аутентификации
        auth_data = {
            "username": os.getenv("ADMIN_EMAIL"),
            "password": os.getenv("ADMIN_PASSWORD"),
            "redirect": "false",
            "csrfToken": csrf_token,
            "json": "true",
        }

        # Выполняем аутентификацию
        auth_response = self.client.post(
            "/api/auth/callback/credentials",
            data=auth_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if auth_response.status_code != 200:
            raise Exception("Authentication failed")

        # Получаем сессию и токен
        session_response = self.client.get("/api/auth/session")
        if session_response.status_code != 200:
            raise Exception("Failed to get session")

        session_data = session_response.json()
        self.access_token = session_data.get("user", {}).get("accessToken")
        if not self.access_token:
            raise Exception("Access token not found in session")

        # Устанавливаем заголовок авторизации
        self.client.headers.update(
            {"Authorization": f"Bearer {self.access_token}"}
        )

    @task(1)
    def get_user_profile(self):
        """Получение профиля пользователя"""
        self.client.get("/api/user/profile")

    @task(2)
    def get_dashboard_data(self):
        """Получение данных дашборда"""
        self.client.get("/api/dashboard")

    @task(3)
    def get_notifications(self):
        """Получение уведомлений"""
        self.client.get("/api/notifications")

    @task(1)
    def create_task(self):
        """Создание новой задачи"""
        task_data = {
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи",
            "priority": "medium",
        }
        self.client.post(
            "/api/tasks",
            json=task_data,
            headers={"Content-Type": "application/json"},
        )

    @task(2)
    def update_task(self):
        """Обновление существующей задачи"""
        task_id = "123"  # Здесь нужно использовать реальный ID задачи
        update_data = {
            "status": "in_progress",
            "comment": "Обновление статуса",
        }
        self.client.put(
            f"/api/tasks/{task_id}",
            json=update_data,
            headers={"Content-Type": "application/json"},
        )

    @task(1)
    def delete_task(self):
        """Удаление задачи"""
        task_id = "123"  # Здесь нужно использовать реальный ID задачи
        self.client.delete(f"/api/tasks/{task_id}")

    def on_stop(self):
        """Выполняется при остановке пользователя"""
        # Здесь можно добавить логику очистки, если необходимо
        pass
