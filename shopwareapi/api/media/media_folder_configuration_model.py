from shopwareapi import fields
from shopwareapi.core.model import Model


class MediaFolderConfigurationModel(Model):
    id = fields.UUIDField(primary_key=True, aliases=("mediaFolderId"))
    createThumbnails = fields.BooleanField(default=False)
    private = fields.BooleanField(default=False)
    thumbnailQuality = fields.IntegerField(null=True)
    keepAspectRatio = fields.BooleanField(default=False)
    private = fields.BooleanField(default=False)
    noAssociation = fields.BooleanField(null=True)

    class Meta:
        api_endpoint = "media-folder-configuration"
        api_type = "media_folder_configuration"
