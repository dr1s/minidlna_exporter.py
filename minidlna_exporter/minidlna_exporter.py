#!/usr/bin/env python3

import argparse
import threading
import urllib.request
from bs4 import BeautifulSoup
from prometheus_client import Gauge, generate_latest
from wsgiref.simple_server import make_server, WSGIRequestHandler, WSGIServer

class minidlna_exporter:

    class _SilentHandler(WSGIRequestHandler):
        """WSGI handler that does not log requests."""

        def log_message(self, format, *args):
            """Log nothing."""

    def __init__(self, url):
        self.url = url
        self.client_stats = dict()
        self.file_stats = dict()
        self.metrics = dict()
        self.metrics['files'] = Gauge('minidlna_files', 'file metrcis', [ 'type' ])
        self.metrics['clients'] = Gauge('minidlna_clients', 'client metrics', ['type', 'ip_address', 'hw_address'])
        self.update_metrics()

    def update_data(self):
        response = urllib.request.urlopen(self.url)
        data = response.read()
        soup = BeautifulSoup(data, 'html.parser')
        tables = soup.find_all('table')
        self.file_stats = self.parse_data_files(tables[0])
        self.client_stats = self.parse_data_clients(tables[1])

    def update_metrics(self):
        self.update_data()
        for i in self.client_stats:
            c = self.client_stats[i]
            self.metrics['clients'].labels(c['type'], c['ip_address'], c['hw_address']).set('1')
        for i in self.file_stats:
            self.metrics['files'].labels(i).set(self.file_stats[i])
        return generate_latest()

    def parse_data_files(self, table):
        tds = [row.findAll('td') for row in table.findAll('tr')]
        results = dict()
        for td in tds:
            results[td[0].string.lower().replace(' ','_')] = td[1].string.lower()
        return results

    def parse_data_clients(self, table):
        tds = [row.findAll('td') for row in table.findAll('tr')]
        results = dict()
        title = tds[0]
        for td in tds[1:]:
            client = dict()
            col = 0
            while col < len(td):
                client[title[col].string.lower().replace(' ','_')] = td[col].string.lower()
                if col < len(td):
                    col += 1
            results[client['hw_address']] = client

        return results


    def print_data(self, data):
        for i in data:
            if not isinstance(i, dict):
                print('%s: %s' %(i, data[i]))
            else:
                for l in i:
                    print('%s: %s' % (l, i[l]))

    def make_prometheus_app(self):

        def prometheus_app(environ, start_response):
            output = self.update_metrics()
            status = str('200 OK')
            headers = [(str('Content-type'), str('text/plain'))]
            start_response(status, headers)
            return [output]
        return prometheus_app

    def make_server(self, interface, port):
        server_class = WSGIServer

        if ':' in interface:
            if getattr(server_class, 'address_family') == socket.AF_INET:
                    server_class.address_family = socket.AF_INET6

        print("* Listening on %s:%s" % (interface, port))
        self.httpd = make_server(   interface,
                                    port,
                                    self.make_prometheus_app(),
                                    server_class=server_class,
                                    handler_class=self._SilentHandler)
        t = threading.Thread(target=self.httpd.serve_forever)
        t.start()



def main():

    parser = argparse.ArgumentParser(
        description='minidlna_exporter')
    parser.add_argument('-m', '--minidlna',
        help='minidlna adress',
        default='http://localhost:8200')
    parser.add_argument('-p', '--port', type=int,
        help='port minidlna_exporter is listening on',
        default=9312)
    parser.add_argument('-i', '--interface',
        help='interface minidlna_exporter will listen on',
        default='0.0.0.0')
    args = parser.parse_args()

    mde = minidlna_exporter(args.minidlna)
    mde.make_server(args.interface, args.port)


if __name__ == '__main__':
    main()
