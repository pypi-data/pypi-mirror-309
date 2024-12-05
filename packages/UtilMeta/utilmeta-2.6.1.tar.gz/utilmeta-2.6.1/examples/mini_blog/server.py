from utilmeta import UtilMeta
from utilmeta.core import api
from config import configure
import fastapi

service = UtilMeta(
    __name__,
    name='blog',
    backend=fastapi,
    asynchronous=True,
    port=8002
)
configure(service)
# should import API after setup
from blog.api import ArticleAPI


@service.mount
class RootAPI(api.API):
    article: ArticleAPI


if __name__ == '__main__':
    service.run()
