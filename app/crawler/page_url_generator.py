from urllib import parse
import requests


class PageUrlGenerator:
    def __init__(self):
        self.source_encoded_url = ""
        self.source_decoded_url = ""
        self.target_decoded_url = ""
        self.target_encoded_url = ""
        self.i_in_list = 0
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
        splited[2] = str(self.i_in_list)
        splited[3] = str(self.offset)
        self.target_decoded_url = '|'.join(splited)

    def _create_target_encoded_url(self):
        self.target_encoded_url = parse.quote(self.target_decoded_url, safe='/:?=()&')

    def _update_target_url(self):
        self._update_target_decoded_url()
        self._create_target_encoded_url()

    def source_url(self, original_url):
        self.source_encoded_url = original_url
        
    def initialize(self):
        self._getting_total_count()
        self._set_source_decoded_url(self.source_encoded_url)
        self._update_target_url()

    def has_next(self):
        return self.total_count > self.i_in_list

    def next(self):
        if self.has_next():
            print(str(self.total_count) + " > " + str(self.i_in_list))
            self.i_in_list += self.offset
            self._update_target_url()
        return self.target_encoded_url

    def first_url(self):
        return self.next()
    

def test():
    pug = PageUrlGenerator()
    pug.source_url("http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.Manufacturer.%ED%98%84%EB%8C%80.)_.OfficeCityState.%EA%B2%BD%EA%B8%B0._.Trust.ExtendWarranty._.Options.%EB%B8%8C%EB%A0%88%EC%9D%B4%ED%81%AC+%EC%9E%A0%EA%B9%80+%EB%B0%A9%EC%A7%80(ABS_)._.Options.%ED%9B%84%EB%B0%A9+%EC%B9%B4%EB%A9%94%EB%9D%BC._.Options.%EC%A3%BC%EC%B0%A8%EA%B0%90%EC%A7%80%EC%84%BC%EC%84%9C(%EC%A0%84%EB%B0%A9_)._.Category.SUV.)&sr=%7CModifiedDate%7C0%7C3")
    pug.initialize()
    # print(pug)
    
# test()

    