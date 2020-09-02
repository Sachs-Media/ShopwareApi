import logging
import shopwareapi.exception as exception
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.client import ShopwareClient
from shopwareapi.utils.queryset import Queryset


log = logging.getLogger("basecontroller")



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
        """
            Getter for deliver the SevDeskClient object
            :return SevDeskClient:
        """

        if not self.model.get_client():
            raise exception.NotConnectedToClient("Please link this to ShopwareClient object. Using client.send(<thisobject>) ")
        return self.model.get_client()

        
    def create(self, *args, **kwargs):
        """
            Creates a new Object at API
            by default it uses the linked model for informations.
            Yo can overwrite the request parameters it via kwargs
            :param kwargs: Arguments which should be overwritten
            :return request: The orginal requests response
        """
        request_url = self.get_client().build_url(model=self.api_model)
        data = self.model.get_dict()
        data.update(kwargs)
        response = self.get_client().post(request_url, data)
        #self.model.map_attributes(response["objects"])

        return response

    def find(self, term, matches_field=None):
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
            if item["type"] == self.api_model:
                
                if matches_field is not None:
                    item_term = item["attributes"].get(matches_field)

                    if item_term == term:
                        result_uuid.append(item["id"])

                else:
                    result_uuid.append(item["id"])
        
        result_product_list = []
        for uuid in result_uuid:
            result_product_list.append(self.get(uuid))
        return Queryset(self.model.__class__, *result_product_list)
        
    def get(self, uuid):
        """
            Requests all Information for a specific product uuid
        """
        
        request_url = self.get_client().build_url(model="product/"+uuid)
        response = self.get_client().get(request_url)
        
        
        model = self.model.__class__(options={"client": self.get_client()})

        model.map_attributes(response["data"]["attributes"])
        
        return model

        
        #model_list = []
        
        #for item in response["objects"]:
        #    model = self.model.__class__(options={"sevdesk_client": self.get_sevdesk_client()})
        #    model.map_attributes(item)
        #    model_list.append(model)

        #return model_list

    # def get_or_create(self, **kwargs):
    #     """
    #         Searches a Value, if no result creates a new one with the same
    #         Values
    #         :return tuple(object: BaseModel, created: bool): object contains the (existing) api object, created is a boolean if the data
    #         was new created or already exist
    #     """
    #     result = self.find(**kwargs)
    #     if len(result) <= 0:
    #         self.create(**kwargs)
    #         created = True
    #     elif len(result) > 1:
    #         log.info([ item.name for item in result ])
    #         raise ValueError("too many results")
    #     else:
    #         self.model.map_attributes(result[0].get_dict())
    #         created = False

    #     return self.model, created
