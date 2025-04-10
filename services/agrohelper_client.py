import json
import logging
import os
from typing import Optional
from urllib.parse import parse_qs, urljoin, urlparse

import allure
import requests
import urllib3
from bs4 import BeautifulSoup

# Настройка логгера
logger = logging.getLogger(__name__)


class AgroHelperClient:
    def __init__(self):
        self.base_url = os.getenv("AGROHELPER_HOST")
        self.session = requests.Session()
        self._setup_session()
        self.access_token = None

    def _setup_session(self):
        """Setup session with default headers and follow redirects"""
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )
        self.session.max_redirects = 5
        # Отключаем проверку SSL-сертификатов
        self.session.verify = False
        # Отключаем предупреждения о небезопасных запросах
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _parse_auth_form(self, html_content: str) -> dict:
        """Parse HTML form and extract authentication parameters"""
        soup = BeautifulSoup(html_content, "html.parser")
        form = soup.find(
            "form", {"id": "kc-form-login auth-form__form form mb-16"}
        )

        if not form:
            raise ValueError("Login form not found in the response")

        action_url = form.get("action")
        if not action_url:
            raise ValueError("Action URL not found in the form")

        # Парсим параметры из URL
        parsed_url = urlparse(action_url)
        query_params = parse_qs(parsed_url.query)

        # Извлекаем параметры из URL
        return {
            "session_code": query_params.get("session_code", [""])[0],
            "execution": query_params.get("execution", [""])[0],
            "client_id": query_params.get("client_id", [""])[0],
            "tab_id": query_params.get("tab_id", [""])[0],
            "action_url": action_url,
        }

    def _extract_code_from_url(self, url: str) -> str:
        """Extract code parameter from URL"""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("code", [""])[0]

    def _update_auth_header(self):
        """Update Authorization header with access token"""
        if self.access_token:
            self.session.headers.update(
                {"Authorization": f"Bearer {self.access_token}"}
            )

    def _log_json_response(self, response_json: dict, response_text: str):
        """Helper method to log JSON response with proper encoding"""
        json_str = json.dumps(response_json, indent=2, ensure_ascii=False)
        logger.info(f"Response JSON: {json_str}")
        allure.attach(
            json_str,
            name="Response JSON",
            attachment_type=allure.attachment_type.JSON,
        )

    def authenticate(self) -> bool:
        """Authenticate with the server"""
        try:
            # Initial request to get redirects
            response = self.session.get(self.base_url)

            # Парсим HTML форму для получения параметров аутентификации
            auth_params = self._parse_auth_form(response.text)
            logger.info(f"Extracted auth parameters: {auth_params}")

            # Prepare form data
            form_data = {
                "username": os.getenv("ADMIN_EMAIL"),
                "password": os.getenv("ADMIN_PASSWORD"),
                "credentialId": "",
            }

            # Send authentication request using the extracted action URL
            auth_response = self.session.post(
                auth_params["action_url"],
                data=form_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            logger.info(
                f"Authentication response status: {auth_response.status_code}"
            )

            # Извлекаем code из Location
            location = auth_response.history[0].headers.get("Location")
            if not location:
                raise Exception("Location not found in response")

            code = self._extract_code_from_url(location)
            if not code:
                raise Exception("Code not found in referer URL")

            # Получаем CSRF токен
            csrf_response = self.session.get(
                urljoin(self.base_url, "/api/auth/csrf")
            )
            if csrf_response.status_code != 200:
                raise Exception("Failed to get CSRF token")

            csrf_token = csrf_response.json().get("csrfToken")
            if not csrf_token:
                raise Exception("CSRF token not found in response")

            # Отправляем callback запрос
            callback_data = {
                "redirect": "false",
                "code": code,
                "csrfToken": csrf_token,
                "callbackUrl": "https://frontagroservice.softdevcenter.ru/token",
                "json": "true",
            }

            callback_response = self.session.post(
                urljoin(self.base_url, "/api/auth/callback/credentials"),
                data=callback_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if callback_response.status_code != 200:
                raise Exception("Failed to process callback")

            # Получаем сессию
            session_response = self.session.get(
                urljoin(self.base_url, "/api/auth/session")
            )
            if session_response.status_code != 200:
                raise Exception("Failed to get session")

            # Извлекаем access token из сессии
            session_data = session_response.json()
            self.access_token = session_data.get("user", {}).get("accessToken")
            if not self.access_token:
                raise Exception("Access token not found in session")

            # Обновляем заголовок авторизации
            self._update_auth_header()

            # Обновляем base_url
            self.base_url = os.getenv("API_HOST")
            logger.info("Successfully updated base_url and set access token")

            return True

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False

    @allure.step("GET запрос к {endpoint}")
    def get(
        self, endpoint: str, params: Optional[dict] = None
    ) -> requests.Response:
        """Make GET request to API endpoint"""
        url = urljoin(self.base_url, endpoint)
        logger.info(f"GET request to {url} with params: {params}")

        response = self.session.get(url, params=params)

        logger.info(f"Response status code: {response.status_code}")
        try:
            response_json = response.json()
            self._log_json_response(response_json, response.text)
        except ValueError:
            logger.info(f"Response text: {response.text}")
            allure.attach(
                response.text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT,
            )

        return response

    @allure.step("POST запрос к {endpoint}")
    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json_data: Optional[dict] = None,
    ) -> requests.Response:
        """Make POST request to API endpoint"""
        url = urljoin(self.base_url, endpoint)

        if json_data:
            json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
            logger.info(f"POST request to {url} with JSON: {json_str}")
            allure.attach(
                json_str,
                name="Request JSON",
                attachment_type=allure.attachment_type.JSON,
            )
        else:
            logger.info(f"POST request to {url} with data: {data}")
            if data:
                allure.attach(
                    str(data),
                    name="Request Data",
                    attachment_type=allure.attachment_type.TEXT,
                )

        response = self.session.post(url, data=data, json=json_data)

        logger.info(f"Response status code: {response.status_code}")
        try:
            response_json = response.json()
            self._log_json_response(response_json, response.text)
        except ValueError:
            logger.info(f"Response text: {response.text}")
            allure.attach(
                response.text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT,
            )

        return response

    @allure.step("PUT запрос к {endpoint}")
    def put(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json_data: Optional[dict] = None,
    ) -> requests.Response:
        """Make PUT request to API endpoint"""
        url = urljoin(self.base_url, endpoint)

        if json_data:
            json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
            logger.info(f"PUT request to {url} with JSON: {json_str}")
            allure.attach(
                json_str,
                name="Request JSON",
                attachment_type=allure.attachment_type.JSON,
            )
        else:
            logger.info(f"PUT request to {url} with data: {data}")
            if data:
                allure.attach(
                    str(data),
                    name="Request Data",
                    attachment_type=allure.attachment_type.TEXT,
                )

        response = self.session.put(url, data=data, json=json_data)

        logger.info(f"Response status code: {response.status_code}")
        try:
            response_json = response.json()
            self._log_json_response(response_json, response.text)
        except ValueError:
            logger.info(f"Response text: {response.text}")
            allure.attach(
                response.text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT,
            )

        return response

    @allure.step("DELETE запрос к {endpoint}")
    def delete(self, endpoint: str) -> requests.Response:
        """Make DELETE request to API endpoint"""
        url = urljoin(self.base_url, endpoint)
        logger.info(f"DELETE request to {url}")

        response = self.session.delete(url)

        logger.info(f"Response status code: {response.status_code}")
        try:
            response_json = response.json()
            self._log_json_response(response_json, response.text)
        except ValueError:
            logger.info(f"Response text: {response.text}")
            allure.attach(
                response.text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT,
            )

        return response

    @allure.step("OPTIONS запрос к {endpoint}")
    def options(self, endpoint: str) -> requests.Response:
        """Make OPTIONS request to API endpoint"""
        url = urljoin(self.base_url, endpoint)
        logger.info(f"OPTIONS request to {url}")

        response = self.session.options(url)

        logger.info(f"Response status code: {response.status_code}")
        try:
            response_json = response.json()
            self._log_json_response(response_json, response.text)
        except ValueError:
            logger.info(f"Response text: {response.text}")
            allure.attach(
                response.text,
                name="Response Text",
                attachment_type=allure.attachment_type.TEXT,
            )

        return response


def auth_as_admin() -> AgroHelperClient:
    """Create and authenticate an admin client"""
    client = AgroHelperClient()
    if not client.authenticate():
        raise Exception("Failed to authenticate as admin")
    return client
