#!/usr/bin/env python
# coding: utf-8

import os
import json
import argparse
from playwright.sync_api import Playwright, sync_playwright

def run_alsea(playwright: Playwright, input_json):

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.alsea.com.mx/factura-electronica.html")
    
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name=input_json["ticket_data"]["store_name"]).click()    
    page1 = page1_info.value
    
    page1.get_by_role("textbox", name="RFC*").click()
    page1.get_by_role("textbox", name="RFC*").fill(input_json["user_data"]["RFC"])
    page1.get_by_role("textbox", name="Ticket*").click()
    page1.get_by_role("textbox", name="Ticket*").fill(input_json["ticket_data"]["ticket_number"])
    page1.get_by_role("textbox", name="Total*").click()
    page1.get_by_role("textbox", name="Total*").fill(input_json["ticket_data"]["ticket_total"])

    # Ensure the screenshots folder exists
    screenshot_path = "output/screenshots/alsea/alsea-filled-in-form.png"
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    
    page1.screenshot(path=screenshot_path, full_page=True)
    print(f"Screenshot saved: {screenshot_path}")

    context.close()
    browser.close()

# Parse command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy Playwright script for Alsea.")
    parser.add_argument("input_json", help="Path to the JSON file containing user and ticket data.")

    args = parser.parse_args()

    # Load JSON data
    with open(args.input_json, "r", encoding="utf-8") as file:
        input_data = json.load(file)

    # Run Playwright script
    with sync_playwright() as playwright:
        run_alsea(playwright, input_data)
