#!/usr/bin/env python
# coding: utf-8

# # Playwright UDFs

# # Libraries

# In[1]:


from playwright.sync_api import Playwright, sync_playwright


# # User-Defined Functions (UDFs)

# In[ ]:


# Screenshot generator
def screenshot_generator(url_path, img_title, n):
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        page.goto(url_path)
        page.screenshot(path="output/screenshots/{img_title}{n}.png", full_page=True )
        browser.close()


# In[ ]:


def start_run(url_start: str, playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url_start)

    return browser, context, page

def end_run(browser, context):
    context.close()
    browser.close()

