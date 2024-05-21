from opensearchpy import AsyncOpenSearch
from settings import settings
import asyncio

INDEX_ITEMS_VIEWS = "items_views"
INDEX_REQUESTS = "requests"

if settings.OPENSEARCH_HOST:
    client: AsyncOpenSearch = AsyncOpenSearch(
        hosts = [{'host': settings.OPENSEARCH_HOST, 'port': settings.OPENSEARCH_PORT}],
        http_auth = (settings.OPENSEARCH_LOGIN, settings.OPENSEARCH_PASSWORD),
        use_ssl = True,
        verify_certs = False,
        ssl_show_warn = False
    )
else:
    client = None