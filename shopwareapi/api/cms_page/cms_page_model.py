import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class CmsPageModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)

    class Meta:
        api_endpoint = "cms-page"
        api_type = "cms_page"
