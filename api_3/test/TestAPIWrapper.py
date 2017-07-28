'''
Created on Jul 26, 2017

@author: michael
'''
'''
Created on Jul 19, 2017

@author: michael
'''
# BUGBUG: after testing on dev, remove this file, not for general deployment
import endpoints
from protorpc import messages, remote

from api_3.isb_cgc_api.isb_cgc_api_helpers import ISB_CGC_Endpoints

class Output(messages.Message):
    id = messages.StringField(1)
    echo = messages.StringField(2)

class InputNestedOne(messages.Message):
    cases = messages.StringField(1, repeated=True)
    case_count = messages.IntegerField(2, variant=messages.Variant.INT32)

class InputNestedTwo(messages.Message):
    samples = messages.StringField(1, repeated=True)
    sample_count = messages.IntegerField(2, variant=messages.Variant.INT32)

class InputNestedThree(messages.Message):
    str_one = messages.StringField(1, repeated=True)
    int_one = messages.IntegerField(2, variant=messages.Variant.INT32)
    str_two = messages.StringField(3, repeated=True)
    int_two = messages.IntegerField(4, variant=messages.Variant.INT32)
    
class InputWrapper(messages.Message):
    one = messages.MessageField(InputNestedOne, 1)
    two = messages.MessageField(InputNestedTwo, 2)
    three = messages.MessageField(InputNestedThree, 3)

@ISB_CGC_Endpoints.api_class(resource_name='isb_cgc_test')
class ISB_CGC_Test(remote.Service):
    POST_RESOURCE = endpoints.ResourceContainer(InputWrapper, name=messages.StringField(2, required=True))

    @endpoints.method(POST_RESOURCE, Output, path='test', http_method='POST')
    def api_test(self, request):
        """
        Test input that consists of a message with nested messages, how it appears in the api explorer and 
        how the values are passed along
        """
        query_dict = {
            k.name: request.get_assigned_value(k.name)
            for k in request.all_fields()
            if k.name is not 'name'
        }
        echo = 'input:\n\t{}'.format('\n\t'.join(('{}: {}'.format(key, value) for key, value in query_dict.iteritems())))
        return Output(id = 'id', echo = echo)
