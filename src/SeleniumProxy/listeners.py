from SeleniumLibrary import SeleniumLibrary
from collections import UserDict
from collections import OrderedDict
from collections.abc import Mapping, MutableMapping
from selenium.webdriver.support.events import AbstractEventListener
from SeleniumProxy.events import LogEventManager
import structlog


class SeleniumProxyListener(AbstractEventListener):

    def __init__(self):
        self.http_event = {}
        self.logger = LogEventManager().getLogger("http_metrics")

    def build_request(self, request):
        req = dict(body={})
        req['path'] = request.path
        req['method'] = request.method
        if 'Referer' in request.headers.keys():
            req['referrer'] = request.headers['Referer']
        self.http_event['request'] = req

    def build_response(self, response):
        res = dict(body={})
        res['status_code'] = response.status_code
        self.http_event['response'] = res

    def after_navigate_to(self, url, driver):
        for req in driver.requests:
            request = self.build_request(req)
            response = self.build_response(req.response)
            self.logger.bind(http=self.http_event)
            self.logger.debug("after navigate to")

    def before_change_value_of(self, element, driver):
        obj = element.get_property('attributes')
        for req in driver.requests:
            request = self.build_request(req)
            self.logger.bind(http=self.http_event)
            self.logger.debug("before change value")

    def after_change_value_of(self, element, driver):
        for req in driver.requests:
            request = self.build_request(req)
            self.logger.bind(http=self.http_event)
            self.logger.debug("after change value")

    def before_click(self, element, driver):
        for req in driver.requests:
            request = self.build_request(req)
            self.logger.bind(http=self.http_event)
            self.logger.debug("before click")

    def after_click(self, element, driver):
        for req in driver.requests:
            request = self.build_request(req)
            self.logger.bind(http=self.http_event)
            self.logger.debug("after click")

    def before_quit(self, driver):
        for req in driver.requests:
            request = self.build_request(req)
            self.logger.bind(http=self.http_event)
            self.logger.debug("before quit")

    # def after_execute_script(self, script, driver):
    #     import sys
    #     import pdb
    #     pdb.Pdb(stdout=sys.__stdout__).set_trace()

    def before_close(self, url, driver):
        for req in driver.requests:
            request = self.build_request(req)
            self.logger.bind(http=self.http_event)
            self.logger.debug("before close")

    def on_exception(self, exception, driver):
        import sys
        import pdb
        pdb.Pdb(stdout=sys.__stdout__).set_trace()


class RobotFrameworkListener(object):
    ROBOT_LISTENER_API_VERSION = '2'

    def __init__(self):
        self.logger = LogEventManager().getLogger('suite_metrics')
        self.robot_event = {
            'longname': 'action',
            'kwname': 'action',
            'libname': 'module',
            'type': 'type',
            'status': 'outcome',
            'starttime': 'start',
            'endtime': 'end',
            'elapsedtime': 'duration',
        }

    def mapper(self, obj):
        event = dict()
        for k, v in obj.items():
            try:
                field = self.robot_event[k]
                event.update({field: v})
            except KeyError:
                self.logger.bind(data={k: v})
                continue
        return event

    def start_suite(self, name, attrs):
        record = self.mapper(attrs)
        self.logger.bind(ecsevent=record)
        self.logger.debug("start keyword")

    def start_test(self, name, attrs):
        record = self.mapper(attrs)
        self.logger.bind(ecsevent=record)
        self.logger.debug("start keyword")

    def start_keyword(self, name, attrs):
        record = self.mapper(attrs)
        self.logger.bind(ecsevent=record)
        self.logger.debug("start keyword")

    def end_keyword(self, name, attrs):
        record = self.mapper(attrs)
        self.logger.bind(ecsevent=record)
        self.logger.debug("end keyword")

    def end_test(self, data, test):
        record = self.mapper(test)
        self.logger.bind(ecsevent=record)
        self.logger.debug("end suite")

    def end_suite(self, data, suite):
        record = self.mapper(suite)
        self.logger.bind(ecsevent=record)
        self.logger.debug("end suite")
