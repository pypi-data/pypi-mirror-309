import requests
import time
from dataclasses import dataclass
from typing import Optional, Any

class UrlPathBuilder:
    def __init__(self, root_url: str):
        self._url = root_url
        self._segments = []

    def segment(self, seg: str) -> "UrlPathBuilder":
        self._segments.append(seg)
        return self

    def url(self) -> str:
        return self._url + self.path()
    def path(self) -> str:
        return "/" + "/".join(str(s) for s in self._segments)

    def __getattr__(self, name):
        self.segment(name)
        def url_seg(*args):
            for arg in args:
                self.segment(arg)
            return self
        return url_seg

class TbaUrl(UrlPathBuilder):
    def __init__(self, owner: "Tba", root_url: str):
        super().__init__(root_url)
        self._owner = owner

    def req(self):
        return self._owner.request(self.path())

@dataclass
class ResultCacheEntry:
    prev_version: str
    timeout: int
    data: Any

class Tba:
    key: str
    root_url: str
    result_cache: dict[str, ResultCacheEntry]
    def __init__(self, key: str, root_url: str = "http://www.thebluealliance.com/api/v3", user_agent: str = None):
        self.key = key
        self.root_url = root_url
        self.result_cache = {}

    def url(self) -> TbaUrl:
        return TbaUrl(self, self.root_url)

    def request(self, path: str) -> Optional[Any]:
        headers = {
            "X-TBA-Auth-Key": self.key,
            "User-Agent": "TBA-api-python/0.1"
        }
        url = self.root_url + path
        last = self.result_cache.get(path)
        if last is not None:
            print(f"Seen {path} before")
            if time.time() < last.timeout:
                print(f"Using cached version for {path}")
                return last.data

            headers["If-None-Match"] = last.prev_version

        resp = requests.get(url, headers=headers)

        if not resp.ok:
            return None

        if resp.status_code == 304:
            if last is not None:
                self._update_cache(path, resp, last.data, last.etag)
                return last.data
            else:
                # This option doesn't make a whole lot of sense, but it should be here just in case
                # Think of it as a kind of error steamroller. Worst case is we have redundant requests
                return None

        data = resp.json()
        self._update_cache(path, resp, data)
        return data

    def _update_cache(self, path, resp, data, etag = None):
        cache_ctl = resp.headers.get("Cache-Control")
        max_age = 0
        if cache_ctl is not None and "max-age" in cache_ctl:
            for entry in cache_ctl.split(", "):
                parts = entry.split("=")
                if len(parts) != 2:
                    continue
                if parts[0] == "max-age":
                    max_age = int(parts[1])

        if etag is None:
            etag = resp.headers["ETag"]
        
        entry = ResultCacheEntry(etag, time.time() + max_age, data)
        self.result_cache[path] = entry



