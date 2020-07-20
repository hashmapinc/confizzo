# confizzo

confizzo is a configuration management library. It is designed to contain many versions of configuration managed approaches into a single API.


## Multi-file Configurations

Multifile configurations, in confizzo terms, are configurations which are partitioned into multiple files. One assumption is that when one configuration contains configuration information of another entity, that that configuration is then stored in a separate configuration file and referenced by type corresponds to filename and the name of the configuration in the file.

### Examples:
Assume that we have an application called data_mover. Then for this application, running in local mode, the configuration will be stored at .data_mover at the $HOME path.

main.yml
````yaml
version: 1

system_1:
  param_1: something
  param_2: other
  _dependencies_:
    var_name: db_conn
    name: dev_pg
    type: database
````

database.yaml
```yaml
version: 1

dev_pg:
  user: user
  password: password
  host: 10.0.0.7
  database: root
```

The usage patter would be something like this:
main.py
```python
from utilities.management.object_factory import ObjectFactory


def main():
    system_1 = ObjectFactory.generate(key='system_1', config='system_1')
    system_1.run()
```

```python
from confizzo.multifile.parser import Parser


class System1:
    def __init__(self):
        self.__config = Parser(application="data_mover")

    def run(self):
        pass

    def __
```
