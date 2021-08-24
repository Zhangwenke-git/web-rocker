from utils.pubulic.logger import Logger
from utils.pubulic.Ua import *
from retrying import retry
import requests
import cchardet

logger = Logger("requests")


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
def downloader(url, method=None, headers=None, timeout=None, binary=False, **kwargs):
    logger.info("Scraping: {}".format(url))
    _header = {"User-Agent": ua()}
    _maxTimeout = timeout if timeout else 5
    _headers = headers if headers else _header
    _method = method if method else "GET"
    try:
        response = requests.request(method=_method, url=url, headers=_headers, **kwargs)
        encoding = cchardet.detect(response.content)["encoding"]
        if response.status_code == 200:
            return response.content if binary else response.content.decode(encoding)
        elif 200 < response.status_code < 400:
            logger.info("Redirect_URL: {}".format(response.url))
        logger.error(
            'Get invalid status code {status_code} while scraping {url}'.format(status_code=response.status_code,
                                                                                url=url))
    except Exception as e:
        logger.error("Error occurred while scraping {url}, Msg: {e}".format(url=url, e=e))


if __name__ == "__main__":
    print(downloader(url="http://www.baidu.com", method="GET"))
