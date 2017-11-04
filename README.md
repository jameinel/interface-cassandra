# Cassandra Interface

 This is a Juju charm interface layer. This interface is used for
 connecting to an Cassandra unit.

### Examples

#### Requires

If your charm needs to connect to Cassandra:

  `metadata.yaml`

```yaml
requires:
  cassandra:
    interface: cassandra
```

  `layer.yaml`

```yaml
includes: ['interface:cassandra']
```  

  `reactive/code.py`

```python
@when('cassandra.available')
def connect_to_cassandra(cassandra):
    print(cassandra.host())
    print(cassandra.port())
    print(cassandra.cluster_name())

```


#### Provides

If your charm needs to provide Cassandra connection details:

  `metadata.yaml`

```yaml
provides:
  cassandra:
    interface: cassandra
```

  `layer.yaml`

```yaml
includes: ['interface:cassandra']
```

  `reactive/code.py`

```python
@when('client.connected')
def connect_to_client(client):
    conf = config()
    cluster_name = conf['cluster-name']
    port = conf['port']
    client.configure(port,cluster_name)
    for c in client.list_connected_clients_data():
        host_ip = c.get_remote_ip()
```

### States

**{relation_name}.connected** - Denotes that the client has connected to the
Cassandra node(s), but has not yet received the data to configure the
connection.

**{relation_name}.available** - Denotes that the client has connected and
received all the information from the provider to make the connection.

**{relation_name}.departed** - Denotes that the unit has departed from the
Cassandra relationship, and should be removed from any configuration
files, etc.

### Data

- **host** - The units private address
- **port** - TCP Port to use
- **cluster_name** - The Cassandra clusters' name

## Maintainers

 - John Arbash Meinel &lt;john@arbash-meinel.com&gt;
