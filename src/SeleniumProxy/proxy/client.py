import http.client
import json
import logging
import threading
from urllib.parse import quote_plus
from SeleniumProxy.proxy.handler import ADMIN_PATH, CaptureRequestHandler, create_custom_capture_request_handler
from SeleniumProxy.proxy.server import ProxyHTTPServer


class AdminClient:
    """Provides an API for sending commands to a remote proxy server."""

    def __init__(self, proxy_mgr_addr=None, proxy_mgr_port=None):
        # The address of the proxy manager if set
        self._proxy_mgr_addr = proxy_mgr_addr
        self._proxy_mgr_port = proxy_mgr_port
        # Reference to a created proxy instance and its address/port
        self._proxy = None
        self._proxy_addr = None
        self._proxy_port = None
        self._capture_request_handler = None

    def create_proxy(self, addr='127.0.0.1', port=0, proxy_config=None, options=None):
        if self._proxy_mgr_addr is not None and self._proxy_mgr_port is not None:
            # TODO: ask the proxy manager to create a proxy and return that
            pass

        if options is None:
            options = {}

        custom_response_handler = options.get('custom_response_handler')
        if custom_response_handler is not None:
            self._capture_request_handler = create_custom_capture_request_handler(
                custom_response_handler)
        else:
            self._capture_request_handler = CaptureRequestHandler
        self._capture_request_handler.protocol_version = 'HTTP/1.1'
        self._capture_request_handler.timeout = options.get(
            'connection_timeout', 5)
        self._proxy = ProxyHTTPServer((addr, port), self._capture_request_handler,
                                      proxy_config=proxy_config, options=options)

        t = threading.Thread(name='Selenium Wire Proxy Server',
                             target=self._proxy.serve_forever)
        t.daemon = not options.get('standalone')
        t.start()

        socketname = self._proxy.socket.getsockname()
        self._proxy_addr = socketname[0]
        self._proxy_port = socketname[1]

        # log.info('Created proxy listening on {}:{}'.format(
        #     self._proxy_addr, self._proxy_port))
        return self._proxy_addr, self._proxy_port

    def destroy_proxy(self):
        """Stops the proxy server and performs any clean up actions."""
        # log.info('Destroying proxy')
        # If proxy manager set, we would ask it to do this
        self._proxy.shutdown()
        self._proxy.server_close()  # Closes the server socket

    def get_requests(self):
        return self._make_request('GET', '/requests')

    def get_last_request(self):
        return self._make_request('GET', '/last_request')

    def clear_requests(self):
        self._make_request('DELETE', '/requests')

    def find(self, path):
        return self._make_request('GET', '/find?path={}'.format(quote_plus(str(path))))

    def get_request_body(self, request_id):
        return self._make_request('GET', '/request_body?request_id={}'.format(request_id)) or None

    def get_response_body(self, request_id):
        return self._make_request('GET', '/response_body?request_id={}'.format(request_id)) or None

    def set_header_overrides(self, headers):
        self._make_request('POST', '/header_overrides', data=headers)

    def clear_header_overrides(self):
        self._make_request('DELETE', '/header_overrides')

    def get_header_overrides(self):
        return self._make_request('GET', '/header_overrides')

    def set_rewrite_rules(self, rewrite_rules):
        self._make_request('POST', '/rewrite_rules', data=rewrite_rules)

    def clear_rewrite_rules(self):
        self._make_request('DELETE', '/rewrite_rules')

    def get_rewrite_rules(self):
        return self._make_request('GET', '/rewrite_rules')

    def set_scopes(self, scopes):
        self._make_request('POST', '/scopes', data=scopes)

    def reset_scopes(self):
        self._make_request('DELETE', '/scopes')

    def get_scopes(self):
        return self._make_request('GET', '/scopes')

    def _make_request(self, command, path, data=None):
        url = '{}{}'.format(ADMIN_PATH, path)
        conn = http.client.HTTPConnection(self._proxy_addr, self._proxy_port)

        args = {}
        if data is not None:
            args['body'] = json.dumps(data).encode('utf-8')

        conn.request(command, url, **args)
        try:
            response = conn.getresponse()
            if response.status != 200:
                raise ProxyException(
                    'Proxy returned status code {} for {}'.format(response.status, url))

            data = response.read()
            try:
                if response.getheader('Content-Type') == 'application/json':
                    data = json.loads(data.decode(encoding='utf-8'))
            except (UnicodeDecodeError, ValueError):
                pass
            return data
        except ProxyException:
            raise
        except Exception as e:
            raise ProxyException(
                'Unable to retrieve data from proxy: {}'.format(e))
        finally:
            try:
                conn.close()
            except ConnectionError:
                pass


class ProxyException(Exception):
    """Raised when there is a problem communicating with the proxy server."""
