#!/usr/bin/env python
# coding: utf-8

import os
import json
import argparse
from playwright.sync_api import Playwright, sync_playwright

def run_monparis(playwright: Playwright, input_json):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.monparis.mx/")
    page.locator("#comp-kahemd186").get_by_test_id("linkElement").click()
    
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="SAN JERONIMO").click()
    
    page1 = page1_info.value

    page1.get_by_role("textbox", name="Orden").click()
    page1.get_by_role("textbox", name="Orden").fill(input_json["ticket_data"]["ticket_number"])

    page1.locator("#Total").click()
    page1.locator("#Total").fill(input_json["ticket_data"]["ticket_total"])

    page1.locator("#TotalInvoice").click()
    page1.locator("#TotalInvoice").fill(input_json["ticket_data"]["ticket_total"])

    page1.get_by_role("textbox", name="RFC").click()
    page1.get_by_role("textbox", name="RFC").fill(input_json["user_data"]["RFC"])

    page1.get_by_role("textbox", name="Correo electrónico").click()
    page1.get_by_role("textbox", name="Correo electrónico").fill(input_json["user_data"]["correo_electronico"])

    page1.locator("#legalName").click()
    page1.locator("#legalName").fill(input_json["user_data"]["Razon_social"])
    
    page1.locator("#CP").click()
    page1.locator("#CP").fill(input_json["user_data"]["codigo_postal"])
    
    #page1.get_by_role("button", name="General de Ley Personas Morales").click()
    #page1.get_by_role("listbox").get_by_role("option", name=input_json["user_data"]["regimen_fiscal"]).click()

    #page1.get_by_role("button", name="G03 Gastos en general").click()
    #page1.get_by_role("listbox").get_by_role("option", name=input_json["user_data"]["uso_de_cfdi"]).click()

    # Ensure the screenshots folder exists
    screenshot_path = "output/screenshots/monparis/monparis-filled-in-form.png"
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    
    page1.screenshot(path=screenshot_path, full_page=True)
    print(f"Screenshot saved: {screenshot_path}")

    context.close()
    browser.close()

# Parse command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy Playwright script for Mon Paris.")
    parser.add_argument("input_json", help="Path to the JSON file containing user and ticket data.")

    args = parser.parse_args()

    # Load JSON data
    with open(args.input_json, "r", encoding="utf-8") as file:
        input_data = json.load(file)

    # Run Playwright script
    with sync_playwright() as playwright:
        run_monparis(playwright, input_data)
