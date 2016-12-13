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
from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class ElasticSearchProvides(RelationBase):
    # Every unit connecting will get the same information
    scope = scopes.GLOBAL

    auto_accessors = ['host', 'port']
    # Use some template magic to declare our relation(s)
    @hook('{provides:elasticsearch}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.available')

    @hook('{provides:elasticsearch}-relation-changed')
    def changed(self):
        self.set_state('{relation_name}.ready')

    @hook('{provides:elasticsearch}-relation-departed')
    def departed(self):
        self.remove_state('{relation_name}.ready')
        self.remove_state('{relation_name}.joined')

    def configure(self, port, cluster_name):
        conv = self.conversation()
        conv.set_remote(data={
            'port': port,
            'cluster_name': cluster_name,
            'host': hookenv.unit_get('private-address')
        })
