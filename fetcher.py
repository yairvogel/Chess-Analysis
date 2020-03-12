import requests
import pandas as pd
import os.path as path

class Fetcher:
    DOMAIN = 'https://api.chess.com'
    def __init__(self, path=None):
        if path:
            if self.DOMAIN in path:
                self.url = path
            else:
                self.url = self._join(self.DOMAIN, path)
        else:
            self.url = self.DOMAIN
        
    def _fetch(self, path=None):
        url = self._join(self.url, path) if path else self.url
        if path and self.DOMAIN in path:
            url = path
        res = requests.get(url)
        if not res.ok:
            return None
        return res
    
    def fetch_json(self, path=None):
        res = self._fetch(path)
        if res:
            return res.json()
    
    def fetch_df(self, path=None):
        res = self.fetch_json(path)
        if not res:
            return
        
        while len(res) == 1:
            if type(res) == dict:
                res = res.popitem()[1]
            elif type(res) == list:
                res = res[0]
            else:
                break
        return pd.DataFrame(res)
    
    def create_child(self, path=None):
        if not path:
            return Fetcher(self.url)
        child_path = self._join(self.url, path)
        return Fetcher(child_path)
    
    @staticmethod
    def _join(*args):
        elems = [elem.strip('/') for elem in args]
        return '/'.join(elems)
