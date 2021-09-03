#!/bin/python

import requests
import wget
from bs4 import BeautifulSoup
from argparse import ArgumentParser


class GetArch:

    def __init__(self, source_link):
        self.source_link = source_link

    def mk_request(self):
        try:
            with requests.get(f'{self.source_link}/releng/releases') as response:
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.HTTPError as httperr:
            print(f'Something went wrong! {httperr}')

    def download(self):
        soup = GetArch(self.source_link).mk_request()
        
        torrents = []
        for content in soup.findAll('tr'):
            for tlink in content.findAll('a'):
                if tlink['href'].endswith('/torrent/'):
                    torrents.append(tlink['href'])

        if args.all:
            i = len(torrents)
            for torrent in torrents:
                print(f"\n[*] Downloading: {torrent.split('/')[-3]}")
                wget.download(f'{self.source_link}{torrent}')
                i -= 1
                print(f'\n{i} To go...')
        
        if args.latest:
            print(f"[*] Downloading latest release: {torrents[0].split('/')[-3]}\n")
            wget.download(f"{self.source_link}{torrents[0]}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Downloads Arch iso torrents")
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help="Downloads all iso torrents")

    parser.add_argument('-l', '--latest',
                        action='store_true',
                        help="Downloads latest iso torrent")

    args = parser.parse_args()
    GetArch('https://archlinux.org').download()
