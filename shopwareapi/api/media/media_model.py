import mimetypes
import os
import uuid
from pathlib import Path
from urllib.parse import urlparse
import io

import requests

from shopwareapi import fields
from shopwareapi.core.model import Model


class File:

    def __init__(self, binary, content_type, path=None, full_filename=None, filename=None, extension=None):
        self._bin = binary
        self._content_type = content_type

        if path is not None:
            p = Path(path)

        if full_filename is not None:
            p = Path(full_filename)

        self._path = path
        self._filename = filename or p.name.split(".")[0]
        self._extension = extension or p.suffix.split(".")[1]

    def get_binary(self):
        return self._bin

    def get_content_type(self):
        return self._content_type

    def get_file_extension(self):
        return self._extension

    def get_filename(self):
        return self._filename


class MediaModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    mediaFolder = fields.ForeignKey("media.media_folder_model.MediaFolderModel")
    fileName = fields.CharField(read_only=True)
    fileExtension = fields.CharField(read_only=True)
    hasFile = fields.BooleanField(default=False)
    position = fields.NumberField(null=True)
    customFields = fields.DictField(null=True)

    class Meta:
        api_endpoint = "media"
        api_type = "media"

    def upload(self, file):
        if not (hasattr(self, "id") and isinstance(self.id, uuid.UUID)):
            raise AttributeError("Missing id attribute")

        if not (hasattr(self, "_meta") and hasattr(self._meta, "swapi_client")):
            raise AttributeError("Missing swapi client")

        if not isinstance(file, File):
            raise ValueError("file must be an instance of shopwareapi.api.media.File")
        swapi_client = self._meta.swapi_client

        swapi_client.post(url={
                "model": ("_action", "media", self.id.hex, "upload"),
                "extension": file.get_file_extension(),
                "fileName": file.get_filename(),
            },
            data=file.get_binary(),
            headers={
                "Content-Type": str(file.get_content_type())
        })

    def upload_from_path(self, path, **kwargs):
        file_kwargs = {
            "content_type": mimetypes.guess_type(path),
            "path": path
        }
        file_kwargs.update(kwargs)
        with open(path, "rb") as fobj:
            f = File(fobj, **file_kwargs)
        return self.upload(f)

    def upload_from_url(self, url, **kwargs):
        o = urlparse(url)
        image_src = requests.get(o.geturl(), stream=True)
        image_data = io.BytesIO(image_src.content)
        content_type = image_src.headers.get("Content-Type") or mimetypes.guess_type(o.path)

        file_kwargs = {
            "content_type": content_type,
            "path": o.path
        }
        file_kwargs.update(**kwargs)
        f = File(image_data, **file_kwargs)
        return self.upload(f)