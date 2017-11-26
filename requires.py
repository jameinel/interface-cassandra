# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=c0111,c0103,c0301

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class CassandraClient(RelationBase):
    # Existing cassandra client interface listed here:
    # ????
    scope = scopes.SERVICE
    auto_accessors = ['username', 'password', 'host', 'native_transport_port',
            'rpc_port', 'cluster_name', 'datacenter', 'rack']


    @hook('{requires:cassandra}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        conv = self.conversation()
        # The basic data we know that we will need
        if (conv.get_remote('rpc_port') and conv.get_remote('username') and
            conv.get_remote('password')):
            conv.set_state('{relation_name}.available')

    @hook('{requires:cassandra}-relation-{departed,broken}')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        conv.remove_state('{relation_name}.available')
        conv.set_state('{relation_name}.broken')

    def list_unit_data(self):
        ''' Iterate through all Cassandra conversations and return the data
        for each cached conversation. This allows us to build a cluster string
        directly from the relation data. eg:

        for unit in cassandra.list_unit_data():
            print(unit['cluster_name'])
        '''
        for conv in self.conversations():
            yield dict((key, conv.get_remote(key)) for key in self.auto_accessors)
