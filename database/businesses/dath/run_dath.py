#!/usr/bin/env python
# coding: utf-8

import os
import json
import argparse
from playwright.sync_api import Playwright, sync_playwright

def run_dath(playwright: Playwright, input_json):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.dath.com.mx/")

    page.get_by_role("link", name="Facturación").click()
    page.locator("#lightbox a").nth(3).click()
    
    page.locator("iframe").content_frame.get_by_role("button", name="Facturar").click()
    page.locator("iframe").content_frame.locator("#Tienda").select_option("2011")
    page.locator("iframe").content_frame.get_by_role("textbox", name="Número de Ticket").click()
    page.locator("iframe").content_frame.get_by_role("textbox", name="Número de Ticket").fill(input_json["ticket_data"]["ticket_number"])
    page.locator("iframe").content_frame.get_by_placeholder("Total").click()
    page.locator("iframe").content_frame.get_by_placeholder("Total").fill(input_json["ticket_data"]["ticket_total"])

    # Ensure the screenshots folder exists
    screenshot_path = "output/screenshots/dath/dath-filled-in-form.png"
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    
    page.screenshot(path=screenshot_path, full_page=True)
    print(f"Screenshot saved: {screenshot_path}")

    context.close()
    browser.close()

# Parse command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy Playwright script for Dath.")
    parser.add_argument("input_json", help="Path to the JSON file containing user and ticket data.")

    args = parser.parse_args()

    # Load JSON data
    with open(args.input_json, "r", encoding="utf-8") as file:
        input_data = json.load(file)

    # Run Playwright script
    with sync_playwright() as playwright:
        run_dath(playwright, input_data)
