import logging
import shopwareapi.exception as exception
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.utils.queryset import Queryset
from shopwareapi.exception import MissingOption
import json
from shopwareapi.core.basemodel import DictMode

log = logging.getLogger(__name__)


class BaseController:
    """
        This class manages the datastructures and URLs for a Model
    """
    def __init__(self, model):
        """
            Constructor. adds model as Attribute
            :param model: The model who use this controller
            :type model: BaseModel
        """
        self.model = model

    def get_client(self):
        if not self.model.get_client():
            raise exception.NotConnectedToClient(
                "Please link this to ShopwareClient object. Using client.send(<thisobject>)")
        return self.model.get_client()

    def create(self, *args, **kwargs):
        """
            Creates a new Object at API
            by default it uses the linked model for informations.
            Yo can overwrite the request parameters it via kwargs
            :param kwargs: Arguments which should be overwritten
            :return request: The orginal requests response
        """
        options = {}
        request_url = self.get_client().build_url(model=self.api_model)
        data = self.model.get_dict(mode=DictMode.WRITE)
        if "options" in kwargs:
            options = kwargs.get("options")
            kwargs.pop("options")

        data.update(kwargs)
        try:
            response = self.get_client().post(request_url, data)
        except json.decoder.JSONDecodeError:
            pass

        if "identifierName" in options:
            id_name = options.get("identifierName")
            res = self.find(getattr(self.model, id_name), matches_field=id_name)
            return res.first()

        return True

    def find(self, term, matches_field=None, caseSensitive=True, **kwargs):
        """
            Find a Object which matches by given kwargs
            :param kwargs: Search Query (names defined at Model.Structure
            :return BaseModel: Model object from the found object
        """
        
        search_data = {}
        
        includes = ["id", "uuid"]
        
        if matches_field is not None:
            includes.append(matches_field)
        
        search_data = {
            "term": term,
            "includes": {
                self.api_model: includes
            }
        }
        request_url = self.get_client().build_url(model="search/{}".format(self.api_model))
        response = self.get_client().post(request_url, search_data)

        result_uuid = []
        for item in response["data"]:
            if item["type"] == self.api_model.replace("-", "_"):
                
                if matches_field is not None:
                    item_term = item["attributes"].get(matches_field)
                    if not caseSensitive:
                        item_term = str(item_term).lower().strip()
                        term = str(term).lower().strip()
                    if item_term == term:
                        result_uuid.append(item["id"])
                else:
                    result_uuid.append(item["id"])
        
        result_list = []
        for uuid in result_uuid:
            result_list.append(self.get(uuid))
        return Queryset(self.model.__class__, *result_list)
        
    def get(self, uuid, **kwargs):
        """
            Requests all Information for a specific product uuid
        """
        
        request_url = self.get_client().build_url(model=self.api_model+"/"+uuid)
        response = self.get_client().get(request_url)

        model = self.model.__class__(options={"client": self.get_client()})
        helper_dict = response["data"]
        helper_dict.update(response["data"]["attributes"])
        model.map_attributes(helper_dict)
        
        return model

    def update(self, *args, **kwargs):
        if "options" in kwargs:
            kwargs.pop("options")
        request_url = self.get_client().build_url(model=self.api_model+"/"+self.model.id)
        data = self.model.get_dict(mode=DictMode.WRITE)
        data.update(kwargs)
        response = self.get_client().patch(request_url, data)

        return response

    def get_or_create(self, **kwargs):
        if "options" in kwargs:
            options = kwargs.get("options")

            if "identifierName" in options:
                id_name = options.get("identifierName")
                result = self.find(getattr(self.model, id_name), matches_field=id_name)
                if len(result.all()) > 0:
                    return result.first()
                return self.create(**kwargs)
        raise MissingOption("Please define identifierName as option")
