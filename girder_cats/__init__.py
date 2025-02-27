from girder import plugin

from girder.api import access
from girder.constants import AccessType, registerAccessFlag
from girder.api.describe import Description, autoDescribeRoute
from girder.api.rest import Resource

from girder_cats.models.cat_model import CatModel

class CatResource(Resource):
    def __init__(self):
        super(CatResource, self).__init__()
        self.resourceName = 'cat'

        self.route('GET', (), self.findCat)
        self.route('GET', (':id',), self.getCat)
        self.route('POST', (), self.createCat)
        self.route('PUT', (':id',), self.updateCat)
        self.route('DELETE', (':id',), self.deleteCat)
        self.route('PUT', (':id', 'feed'), self.feedCat)

    @access.public
    @autoDescribeRoute(
    Description('Find a cat'))
    def findCat(self, params):
        print('findCat() was called!')
        print('params is', params)

    @access.public
    @autoDescribeRoute(
    Description('Get a cat')
    .modelParam('id', 'The cat ID', model=CatModel, level=AccessType.READ))
    def getCat(self, params):
        print('getCat() was called!')
        print('id is', id)
        print('params is', params)

    @access.public
    @autoDescribeRoute(
    Description('Create a cat'))
    def createCat(self, params):
        document = {}
        catModel = CatModel().save(document)
        return catModel

    @access.public
    @autoDescribeRoute(
    Description('Update a cat')
    .modelParam('id', 'The cat ID', model=CatModel, level=AccessType.WRITE))
    def updateCat(self, params):
        print("params is", params)
        if 'cat_model' not in params:
            print("Error: no cat model in the parameter!")
            return

        catModel = params['cat_model']
        if '_id' not in catModel:
            print("Error: missing id from catModel!")
            return

        id = catModel['_id']

        print("id is", id)
        print('updateCat() was called!')

    @access.public
    @autoDescribeRoute(
    Description('Delete a cat')
    .modelParam('id', 'The cat ID', model=CatModel, level=AccessType.WRITE,
                destName='doc'))
    def deleteCat(self, doc, params):
        print('doc is', doc)
        print('params is', params)
        print('deleteCat() was called!')
        CatModel().remove(doc)

    registerAccessFlag(key='cat.feed', name='Feed a cat',
                       description='Allows users to feed a cat')

    @access.user
    @autoDescribeRoute(
    Description('Feed a cat')
    .modelParam('id', 'The cat ID', model=CatModel, plugin='cats',
                 level=AccessType.WRITE, requiredFlags='cat.feed',
                 destName='doc'))
    def feedCat(self, doc, params):
        print('doc is', doc)
        print('params is', params)

        # Feed the cat
        return CatModel().feed(doc)


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Cats in Girder'
    CLIENT_SOURCE_PATH = 'web_client'

    def load(self, info):
        info['apiRoot'].cat = CatResource()
