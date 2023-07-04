from playwright.sync_api import Playwright, sync_playwright, expect
import time

auth = 'brd-customer-hl_8fd2fe43-zone-zone1:8860y9lyjij8'
browser_url = f'wss://{auth}@zproxy.lum-superproxy.io:9222'

def main():
  with sync_playwright() as pw:

    # open browser
    print('connecting...')
    browser = pw.chromium.connect_over_cdp(browser_url)
    print('connected')
    page = browser.new_page()

    # opening booking.com
    print('goto booking.com')
    page.goto('https://www.booking.com', timeout=1000000)
    print('done, evaluating')
    time.sleep(50)

    # now we close the pop up
    page.get_by_role("button", name="Dismiss sign-in info.").click()
    print('pop-up dismiss')
    time.sleep(20)

    # enter destination
    page.get_by_placeholder("Where are you going?").click()
    page.get_by_placeholder("Where are you going?").fill("Amsterdam")
    page.get_by_role("button", name="Amsterdam Noord-Holland, Netherlands").click()
    print('destination entered')
    time.sleep(20)

    # select date and search
    page.get_by_role("checkbox", name="20 April 2023").click()
    page.get_by_role("checkbox", name="25 April 2023").click()
    time.sleep(20)
    page.get_by_role("button", name="Search").click()
    print('date + search')
    time.sleep(20)

    # get hotels and prices on the page
    hotel = page.get_by_test_id('title')
    time.sleep(20)
    price = page.get_by_test_id('price-and-discounted-price')
    time.sleep(20)
    hotelNames = hotel.all_inner_texts()
    hotelPrices = price.all_inner_texts()
    print(len(hotelNames), len(hotelPrices))

    # sort it along the values
    values = dict(zip(hotelNames, hotelPrices))
    print(str(values))

    # close your browser
    browser.close()


main()