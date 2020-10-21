import hashlib
import requests


class HelloFresh:
    def __init__(self, username, password):
        self.empty_card_hash = '25be36350064bffae8ebdedf4b915af4'
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.token = None
        self._login(self.username, self.password)

    def _login(self, username, password):
        # open the login page to initialise the cookies
        self.session.get('https://www.hellofresh.co.uk/login')

        # post login details
        r = self.session.post(
            url="https://www.hellofresh.co.uk/gw/login?country=gb&locale=en-GB",
            json={"username": username,
                  "password": password}
        )

        # check HTTP status
        if r.status_code != 200:
            raise Exception("Authentication status is not 200")

        # check if auth is successful
        self.token = r.json().get('access_token', None)
        if self.token is None:
            raise ValueError("access_token is not found, check credentials")

        return True

    def get_recipes(self):
        if self.token is None:
            raise ValueError("Token is not set")

        def get_recipe_page(_offset, _limit):
            r = self.session.get(
                url="https://gw.hellofresh.com/api/recipes/search"
                    f"?offset={_offset}"
                    f"&limit={_limit}"
                    f"&locale=en-GB"
                    f"&country=gb"
                    f"&min-rating=0",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            result = r.json()
            return result

        offset = 0
        limit = 250
        total = offset + limit

        while offset < total:
            page = get_recipe_page(offset, limit)
            total = page['total']
            offset = offset + limit

            for item in page['items']:
                yield item

    def download_card(self, url):
        if url is None:
            return False
        result = self.session.get(url, stream=True)
        if result.status_code != 200:
            return False
        file_md5 = hashlib.md5(result.content).hexdigest()
        return False if file_md5 == self.empty_card_hash else result.content



