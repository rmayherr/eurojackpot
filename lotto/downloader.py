from configparser import ConfigParser
import requests
import os
import sys
from datetime import datetime


def get_from_config(name):
    """Gain a specific value from config.txt """
    cfg = ConfigParser()
    base_path = os.path.dirname(os.path.abspath(__file__))
    cfg.read("/".join([base_path, 'config.txt']))
    return cfg['default'][name]


def download(url):
    """Download csv file"""
    try:
        """Send a get request"""
        r = requests.get(url, allow_redirects=True, timeout=10)
        try:
            """Download the header and see when the csv file was modified"""
            if os.path.exists(get_from_config('csv_file_name')) and \
                r.headers['Last-Modified'][5:16] >= \
                    datetime.fromtimestamp(
                        os.stat(get_from_config('csv_file_name'))
                            .st_ctime).strftime('%d %b %Y'):
                print(f'File is the newest copy, downloading is unnecessary.')
                return 0
            else:
                """
                Download csv file, display its size and
                put content to data.csv file
                """
                print(f"Downloading file {url.split('/')[-1]} with size"
                      f"{int(r.headers['Content-Length']) / 1024 : .2f}"
                      f"kbyte...")
                r = requests.get(url, allow_redirects=True, timeout=10)
                f = open(get_from_config('csv_file_name'), 'w')
                f.write(r.text)
                f.close()
                print(f'Done.')
                return 0
        except Exception as e:
            print(f"Error occured while writing to file! \n\t{e}")
            return 1
    except Exception as e:
        print(f'Error occured! \n\t{e}')
        return 1
