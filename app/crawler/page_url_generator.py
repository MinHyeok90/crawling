from urllib import parse
import requests


class PageUrlGenerator:
    def __init__(self):
        self.source_encoded_url = ""
        self.source_decoded_url = ""
        self.target_decoded_url = ""
        self.target_encoded_url = ""
        self.cur_page = 0
        self.offset = 400
        self.total_count = 0

    def _extract_total_count_from_source_url(self):
        res = requests.get(self.source_encoded_url)
        included_total_data = res.json()
        return included_total_data['Count']

    def _getting_total_count(self):
        self.total_count = self._extract_total_count_from_source_url()

    def _set_source_decoded_url(self, encoded_url):
        self.source_decoded_url = parse.unquote(self.source_encoded_url)

    def _update_target_decoded_url(self):
        splited = self.source_decoded_url.split('|')
        splited[2] = self.cur_page
        splited[3] = self.offset
        self.target_decoded_url = '|'.join(splited)

    def _create_target_encoded_url(self):
        self.target_encoded_url = quote(self.target_decoded_url)

    def _update_target_url(self):
        self._update_target_decoded_url()
        self._create_target_encoded_url()

    def source_url(self, original_url):
        self.source_encoded_url = original_url
        
    def initialize(self):
        self._getting_total_count()
        self._set_source_decoded_url(self.encoded_url)
        self._update_target_url()

    def has_next(self):
        return self.total_count > (self.cur_page * self.offset)

    def next(self):
        if has_next():
            self.cur_page = self.cur_page + 1
            self._update_target_url()
        return target_encoded_url

    def first_url():
        return next()