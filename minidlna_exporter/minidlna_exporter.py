#!/usr/bin/env python3

#   MIT License
#
#   Copyright (c) 2018 Daniel Schmitz
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

import argparse
import socket
import urllib.request
from bs4 import BeautifulSoup
from prometheus_metrics import exporter, generate_latest


class minidlna_exporter(exporter):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.client_stats = dict()
        self.metrics_handler.add_metric_label('minidlna_files', 'type')
        self.metrics_handler.add_metric_labels(
            'minidlna_clients',
            ['type', 'ip_address', 'hostname', 'hw_address'])
        self.update_metrics()

    def parse_data_files(self, table):
        tds = [row.findAll('td') for row in table.findAll('tr')]
        results = dict()
        for td in tds:
            results[td[0].string.lower().replace(' ',
                                                 '_')] = td[1].string.lower()
        return results

    def parse_data_clients(self, table):
        tds = [row.findAll('td') for row in table.findAll('tr')]
        results = dict()
        title = tds[0]
        for td in tds[1:]:
            client = dict()
            col = 0
            while col < len(td):
                client[title[col].string.lower().replace(
                    ' ', '_')] = td[col].string.lower()
                if col < len(td):
                    col += 1
            client['active'] = True

            client['hostname'] = socket.getfqdn(client['ip_address'])
            if 'in-addr.arp' in client['hostname']:
                client['hostname'] = client['ip_address']

            results[client['hw_address']] = client

        return results

    def update_metrics(self):
        response = urllib.request.urlopen('http://%s' % self.url)
        data = response.read()
        soup = BeautifulSoup(data, 'html.parser')
        tables = soup.find_all('table')
        file_stats = self.parse_data_files(tables[0])
        client_stats = self.parse_data_clients(tables[1])

        self.metrics_handler.update_metric('minidlna_files', file_stats)

        clients = list()
        for i in client_stats:
            c = client_stats[i]
            active = 0
            if c['active']:
                active = 1
            client = [
                c['type'], c['ip_address'], c['hostname'], c['hw_address'],
                active
            ]
            clients.append(client)
        self.metrics_handler.update_metric('minidlna_clients', clients)
        return generate_latest()

    def make_wsgi_app(self):
        def prometheus_app(environ, start_response):
            output = self.update_metrics()
            status = str('200 OK')
            headers = [(str('Content-type'), str('text/plain'))]
            start_response(status, headers)
            return [output]

        return prometheus_app


def main():

    parser = argparse.ArgumentParser(description='minidlna_exporter')
    parser.add_argument(
        '-m', '--minidlna', help='minidlna adress', default='localhost:8200')
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        help='port minidlna_exporter is listening on',
        default=9312)
    parser.add_argument(
        '-i',
        '--interface',
        help='interface minidlna_exporter will listen on',
        default='0.0.0.0')
    args = parser.parse_args()

    mde = minidlna_exporter(args.minidlna)
    mde.make_server(args.interface, args.port)


if __name__ == '__main__':
    main()
