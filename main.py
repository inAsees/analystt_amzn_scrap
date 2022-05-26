from src.scrap import Scraper

if __name__ == "__main__":
    headers = {
        'cookie': 'session-id=258-3723382-3489961; i18n-prefs=EUR; lc-acbde=en_GB; sp-cdn="L5Z9:IN"; ubid-acbde=259-'
                  '4780058-9673219; session-token="UdJ+3NvMuV2KSFtdn+uiKR1/EPEBmI7h606fWB6fn3xUGbuqfhkxO5KjFeD9CgF'
                  'pprhbJo''yTBf89mwZf8Kq6HjA1gvnLMKrxuHyLN4pXD9neWvKGc7/uULzI87zCpqT//RtnrCF00JTaAXccxiksrzPXCCc02Xa'
                  'FNEOycrDKjDN2N''R6vgePKxPMibGD+So7JjR233qRqXZCGBYsZ1Ua6BA=="; csm-hit=tb:WW50E5C0RWP61M11AQ8Q+s-WW5'
                  '0E5C0RWP61M11A''Q8Q|1''653399106140&t:1653399106140&adb:adblk_no; session-id-time=2082754801l; i18n-'
                  'prefs=INR; session-id''=258''-3723382-3489961; session-id-time=2082787201l; session-token="AjhmKGtU3'
                  'g3SfesatM5S1VyYP0fUNwDQv7F''vf95j''PfgD7t+J2mCArZ7ekHlFqfq3ADQryr/NVLHjzpF5aiYk805daEBkT+VyOnf383q//'
                  'Ug28o1zrTK54+Z8hvj9TSHACRH9bww+''xazxdsc''kZ9mZrmBcQzu0Cyow9ENbeL2m9YZk/yo1MDNnrG5O3/WmSEu+4ZPGRbkBp'
                  'uTRmJbYsZ8P2w==";'' ubid-acbin=259-4780058-9673219',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/101.0.4951.67 Safari/537.36',
    }
    scraper = Scraper(headers)
    scraper.scrap_all_pages()
    scraper.inject_info_in_product_overview()
    scraper.dump()
