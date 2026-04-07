import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


def test_main_page_loads(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("h1")).to_contain_text("QR 코드")


def test_create_shortlink(page: Page):
    page.goto(BASE_URL)

    page.fill("#originalUrl", "https://example.com")
    page.fill("#expiresInDays", "30")
    page.click('button[type="submit"]')

    page.wait_for_selector("#resultSection", timeout=10000)

    short_url = page.input_value("#shortUrl")
    assert "localhost:8000" in short_url

    qr_image = page.locator("#qrImage")
    expect(qr_image).to_be_visible()


def test_custom_alias(page: Page):
    page.goto(BASE_URL)

    page.fill("#originalUrl", "https://google.com")
    page.fill("#customAlias", "test-alias")
    page.click('button[type="submit"]')

    page.wait_for_selector("#resultSection", timeout=10000)

    short_url = page.input_value("#shortUrl")
    assert "test-alias" in short_url


def test_copy_button(page: Page):
    page.goto(BASE_URL)

    page.fill("#originalUrl", "https://example.com")
    page.click('button[type="submit"]')

    page.wait_for_selector("#resultSection", timeout=10000)

    page.click(".btn-copy")

    page.wait_for_timeout(500)


def test_download_buttons_visible(page: Page):
    page.goto(BASE_URL)

    page.fill("#originalUrl", "https://example.com")
    page.click('button[type="submit"]')

    page.wait_for_selector("#resultSection", timeout=10000)

    expect(page.locator(".btn-group button")).to_have_count(2)
