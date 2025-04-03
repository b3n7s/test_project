import pytest
from playwright.sync_api import sync_playwright
import allure
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page(ignore_https_errors=True)
    yield page
    page.close()

@pytest.fixture(scope="function")
def admin_page(page):
    from pages.admin_page import AdminPage
    return AdminPage(page)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            try:
                if 'page' in item.funcargs:
                    page = item.funcargs['page']
                    allure.attach(
                        page.screenshot(),
                        name='screenshot',
                        attachment_type=allure.attachment_type.PNG
                    )
            except Exception as e:
                print(f'Не удалось сделать скриншот: {e}') 