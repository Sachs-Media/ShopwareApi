import uuid

from shopwareapi import fields
from shopwareapi.core.model import Model


class MediaFolderModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4, aliases=("mediaFolderId"))
    useParentConfiguration = fields.BooleanField(default=True)
    configuration = fields.ForeignKey("media.media_folder_configuration_model.MediaFolderConfigurationModel", related_name="configurationId")
    parent = fields.ForeignKey("self", related_name="parentId", null=True)
    name = fields.CharField()

    class Meta:
        api_endpoint = "media-folder"
        api_type = "media_folder"
