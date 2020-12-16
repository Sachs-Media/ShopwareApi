import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class MediaFolderModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4, aliases=("mediaFolderId"))
    configuration = fields.ForeignKey("media.media_folder_configuration_model.MediaFolderConfigurationModel", related_name="configurationId")
    parent = fields.CharField()# ForeignKey("self")
    name = fields.CharField()

    class Meta:
        api_endpoint = "media-folder"
        api_type = "media_folder"
