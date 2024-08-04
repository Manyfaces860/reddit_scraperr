import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod

class ReddySpider(scrapy.Spider):
    name = "reddy"

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 3,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'PLAYWRIGHT_BROWSER_TYPE': 'firefox',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; AS; rv:11.0) like Gecko',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': False,
            'args': ['--disable-blink-features=AutomationControlled'],
        },
        'LOG_LEVEL': 'DEBUG',
        'LOG_FILE': f"logs.txt",  # Ensure absolute path
        'LOG_FORMAT': '%(levelname)s: %(message)s',
        'LOG_STDOUT': True
    }

    def start_requests(self):
        yield scrapy.Request('https://www.reddit.com/r/deeplearning/' , meta={
            'playwright': True,
            'playwright_page_methods': [
                PageMethod('evaluate','for (let i = 0; i < 20; i++) setTimeout(() => { window.scrollTo(0, document.body.scrollHeight); console.log("Scrolling down " + i); }, i * 2000); setTimeout(() => { for (let j = 0; j < 20; j++) setTimeout(() => { window.scrollTo(0, document.body.scrollHeight - (j + 1) * (document.body.scrollHeight / 20)); console.log("Scrolling up " + j); }, j * 2000); }, 20 * 2000);'),
                PageMethod('wait_for_timeout', 200000),
            ]
        } , callback=self.parse)

    def parse(self, response):
        with open('all.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        posts = response.css('shreddit-post')
        for post in posts:
            title = post.css('a[slot="title"]::text').get()
            new = []
            for line in post.css('a[slot="text-body"] div div p::text').getall():
                new.append(str(line).strip().replace('\n',''))

            yield {
                "title" : title,
                "content" : ' '.join(new)
            }

