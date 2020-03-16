from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords
from selenium.webdriver.support.events import EventFiringWebDriver
from robot.utils import is_truthy
from SeleniumProxy import webdriver


class BrowserKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.manager = BrowserManagementKeywords(ctx)

    @keyword
    def open_proxy_browser(self, url=None, browser='chrome', proxy_options=None, alias=None):
        index = self.drivers.get_index(alias)
        if index:
            self.info('Using existing browser from index %s.' % index)
            self.manager.switch_browser(alias)
            if is_truthy(url):
                self.manager.go_to(url)
            return index
        return self._make_new_browser(url, browser, proxy_options, alias)

    @keyword
    def create_webdriver(self, driver_name, alias=None, kwargs={}, **init_kwargs):
        pass

    def _make_new_browser(self, url, browser, proxy_options, alias=None):
        driver = self._make_proxy_driver(browser, proxy_options)
        driver = self._wrap_event_firing_webdriver(driver)
        index = self.ctx.register_driver(driver, alias)
        if is_truthy(url):
            try:
                driver.get(url)
            except Exception:
                self.debug("Opened browser with session id %s but failed to open url '%s'." % (
                    driver.session_id, url))
                raise
        self.debug('Opened browser with session id %s.' % driver.session_id)
        return index

    def _wrap_event_firing_webdriver(self, driver):
        if not self.ctx.event_firing_webdriver:
            return driver
        self.debug('Wrapping driver to event_firing_webdriver.')
        return EventFiringWebDriver(driver, self.ctx.event_firing_webdriver())

    def _make_proxy_driver(self, browser, proxy_options):
        if browser == 'Chrome':
            driver = webdriver.Chrome(options=proxy_options)
        elif browser == 'Firefox':
            driver = webdriver.Firefox(options=proxy_options)
        else:
            raise Exception("Browser Type Not Available")
        driver.set_script_timeout(self.ctx.timeout)
        driver.implicitly_wait(self.ctx.implicit_wait)
        return driver
