import json
from camoufox.sync_api import Camoufox

config = {
    'window.outerHeight': 1056,
    'window.outerWidth': 1920,
    'window.innerHeight': 1008,
    'window.innerWidth': 1920,
    'window.history.length': 4,
    'navigator.userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'navigator.appCodeName': 'Mozilla',
    'navigator.appName': 'Netscape',
    'navigator.appVersion': '5.0 (Windows)',
    'navigator.oscpu': 'Windows NT 10.0; Win64; x64',
    'navigator.language': 'en-US',
    'navigator.languages': ['en-US'],
    'navigator.platform': 'Win32',
    'navigator.hardwareConcurrency': 12,
    'navigator.product': 'Gecko',
    'navigator.productSub': '20030107',
    'navigator.maxTouchPoints': 10,
}

with Camoufox(
    headless=False, 
    persistent_context=True,
    user_data_dir='user-data-dir',
    os=('windows'),
    config=config,
    i_know_what_im_doing=True
) as browser:
    # Open the page
    page = browser.new_page()
    page.goto("https://www.crunchbase.com/organization/scrapingbee")
		
		# Wait for Network Idle
    page.wait_for_load_state('networkidle')
    # Wait more, just in case
    page.wait_for_timeout(10000)
	   
	  # Get the required data
    data = {
        'Name': page.locator('span.entity-name.ng-star-inserted').inner_text(),
        'Description': page.locator('span.expanded-only-content.ng-star-inserted').inner_text()
    }

    score_els = page.locator('.top-row-left-groups score-and-trend').all()
    for el in score_els:
        key_name = el.locator('span.label').inner_text()
        value = int(el.locator('div.chip-text').inner_text())
        data[key_name] = value

    data['Overview'] = []
    overview_els = page.locator('.overview-row label-with-icon').all()
    for el in overview_els:
        value = el.locator('.component--field-formatter').inner_text()
        data['Overview'].append(value)
		
		# print scraped data and close the page
    print(json.dumps(data, indent=2))
    page.close()