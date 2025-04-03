import logging
import allure

from typing import Optional, List
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    @allure.step("Открыть страницу {url}")
    def open(self, url: str) -> None:
        """Открыть страницу по указанному URL"""
        self.page.goto(url)
        self.logger.info(f"Открыта страница: {url}")

    @allure.step("Кликнуть по элементу {selector}")
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Кликнуть по элементу"""
        self.page.click(selector, timeout=timeout)
        self.logger.info(f"Клик по элементу: {selector}")

    @allure.step("Ввести текст '{text}' в поле {selector}")
    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """Заполнить поле ввода"""
        self.page.fill(selector, text, timeout=timeout)
        self.logger.info(f"Введен текст '{text}' в поле: {selector}")

    @allure.step("Выбрать опцию '{value}' в селекте {selector}")
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """Выбрать опцию в выпадающем списке"""
        self.page.select_option(selector, value, timeout=timeout)
        self.logger.info(f"Выбрана опция '{value}' в селекте: {selector}")

    @allure.step("Проверить видимость элемента {selector}")
    def is_element_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Проверить видимость элемента"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except:
            return False

    @allure.step("Дождаться загрузки элемента {selector}")
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """Дождаться появления элемента"""
        self.page.wait_for_selector(selector, timeout=timeout)
        self.logger.info(f"Элемент загружен: {selector}")

    @allure.step("Получить текст элемента {selector}")
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Получить текст элемента"""
        text = self.page.text_content(selector, timeout=timeout)
        self.logger.info(f"Получен текст '{text}' из элемента: {selector}")
        return text

    @allure.step("Проверить наличие текста '{text}' на странице")
    def check_text_present(self, text: str) -> None:
        """Проверить наличие текста на странице"""
        expect(self.page).to_contain_text(text)
        self.logger.info(f"Текст '{text}' найден на странице")

    @allure.step("Навести курсор на элемент {selector}")
    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """Навести курсор на элемент"""
        self.page.hover(selector, timeout=timeout)
        self.logger.info(f"Курсор наведен на элемент: {selector}")

    @allure.step("Проверить URL страницы")
    def check_url(self, expected_url: str) -> None:
        """Проверить текущий URL страницы"""
        expect(self.page).to_have_url(expected_url)
        self.logger.info(f"URL страницы соответствует ожидаемому: {expected_url}")

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str) -> None:
        """Сделать скриншот страницы"""
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        self.logger.info(f"Сделан скриншот: {name}")

    @allure.step("Проверить состояние чекбокса {selector}")
    def is_checkbox_checked(self, selector: str) -> bool:
        """Проверить состояние чекбокса"""
        return self.page.is_checked(selector)

    @allure.step("Установить состояние чекбокса {selector}")
    def set_checkbox(self, selector: str, checked: bool) -> None:
        """Установить состояние чекбокса"""
        if checked:
            self.page.check(selector)
        else:
            self.page.uncheck(selector)
        self.logger.info(f"Установлено состояние чекбокса {selector}: {checked}")

    @allure.step("Очистить поле {selector}")
    def clear_input(self, selector: str) -> None:
        """Очистить поле ввода"""
        self.page.fill(selector, "")
        self.logger.info(f"Очищено поле: {selector}")

    @allure.step("Получить значение атрибута {attribute} элемента {selector}")
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Получить значение атрибута элемента"""
        return self.page.get_attribute(selector, attribute)

    @allure.step("Дождаться загрузки страницы")
    def wait_for_load_state(self, state: str = "load") -> None:
        """Дождаться загрузки страницы"""
        self.page.wait_for_load_state(state)
        self.logger.info(f"Страница загружена в состоянии: {state}")

    @allure.step("Проверить наличие элемента {selector}")
    def is_element_present(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Проверить наличие элемента на странице"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except:
            return False

    @allure.step("Получить список элементов {selector}")
    def get_elements(self, selector: str) -> List:
        """Получить список элементов"""
        return self.page.query_selector_all(selector)

    @allure.step("Выполнить JavaScript: {script}")
    def execute_script(self, script: str) -> None:
        """Выполнить JavaScript на странице"""
        self.page.evaluate(script)
        self.logger.info(f"Выполнен JavaScript: {script}")
