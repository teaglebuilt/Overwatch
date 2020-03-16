from SeleniumLibrary.base import LibraryComponent, keyword
import wrapt


class HTTPKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def get_requests(self):
        return self.driver.requests

    @keyword
    def wait_for_request(self, url, timeout=10):
        request = self.driver.wait_for_request(url, timeout)
        return request

    @keyword
    def wait_for_response(self, url):
        response = self.driver.wait_for_response(url)
        return response
