import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class MediaFolderModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4, aliases=("mediaFolderId"))
    configuration = fields.ForeignKey("media.Configuration")
    parent = fields.ForeignKey("media.MediaFolder")
    name = fields.CharField()

    class Meta:
        api_endpoint = "media-folder"
        api_type = "media_folder"
