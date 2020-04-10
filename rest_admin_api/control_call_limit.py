import logging as log  # for verbose output
import time

import urllib3

http = urllib3.PoolManager()


def safe_rest_api_request(method, url, custom_headers):
    response = http.request(method, url, headers=custom_headers)
    if response is not None and response.headers is not None and 'X-Shopify-Shop-Api-Call-Limit' in response.headers:
        limit = response.headers['X-Shopify-Shop-Api-Call-Limit'].split('/')
        if len(limit) == 2 and int(limit[0]) > 25:
            log.info("Taking a 5s nap")
            time.sleep(5)
        else:
            time.sleep(0.5)
    else:
        time.sleep(0.5)
    if response.data is None:
        log.info("Taking a 5s nap and repeating a request")
        time.sleep(5)
        return safe_rest_api_request(method, url, custom_headers)
    return response


def main():
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")


if __name__ == "__main__":
    main()
