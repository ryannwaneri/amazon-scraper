from playwright.sync_api import sync_playwright

def download_amazon_pages(query, page_from=1, page_to=2, export_location='.'):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False, slow_mo=3000)
        page = browser.new_page()
        for page_num in range(page_from, page_to+1):
            print('process',f'https://www.amazon.com/s?k={query}&page={page_num}')
            page.goto(f'https://www.amazon.com/s?k={query}&page={page_num}')
            page.wait_for_load_state('domcontentloaded')

            with open(f'{export_location}/{query}_{page_num}.html', 'x', encoding='utf-8') as f:
                f.write(page.content())

        browser.close()

url = 'https://www.amazon.com/s?k=soundcore&page=20'

if __name__ == '__main__':
    query = 'soundcore'
    export_location = './export'
    download_amazon_pages(query=query,page_from=1,page_to=3, export_location=export_location)