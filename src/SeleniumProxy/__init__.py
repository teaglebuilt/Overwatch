from SeleniumLibrary import SeleniumLibrary
from SeleniumProxy.keywords import BrowserKeywords, HTTPKeywords
from SeleniumProxy.listeners import RobotFrameworkListener, SeleniumProxyListener
from robot.utils import is_truthy


class SeleniumProxy(SeleniumLibrary):

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None, plugins=None,
                 event_firing_webdriver=None):
        SeleniumLibrary.__init__(self, timeout=5.0, implicit_wait=0.0,
                                 run_on_failure='Capture Page Screenshot',
                                 screenshot_root_directory=None, plugins=None,
                                 event_firing_webdriver=None)
        self.ROBOT_LIBRARY_LISTENER = RobotFrameworkListener()
        self.event_firing_webdriver = SeleniumProxyListener
        if is_truthy(event_firing_webdriver):
            self.event_firing_webdriver = self._parse_listener(
                event_firing_webdriver)
        self.add_library_components(
            [BrowserKeywords(self), HTTPKeywords(self)])
