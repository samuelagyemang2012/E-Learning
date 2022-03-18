from migrations.resource_migration import Resource
from models.resource_model import ResourceModel
from sqlalchemy import or_, and_


class ResourceController:

    def __int__(self):
        pass

    def upload(self, user_id, name, resource_id, description):
        resource = Resource(user_id, name, resource_id, description)
        resource_model = ResourceModel()
        res = resource_model.create(resource)

        return res

    def get_resources(self):
        resource_model = ResourceModel()
        resources = resource_model.get_resources()
        return resources

    def update_downloads(self, rid, new_downloads):
        resource_model = ResourceModel()
        resource_model.update_downloads(rid, new_downloads)
        return True
