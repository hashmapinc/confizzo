# confizzo

confizzo is a configuration management library. It is designed to contain many versions of configuration managed approaches into a single API.


## Multi-file Configurations

Multifile configurations, in confizzo terms, are configurations which are partitioned into multiple files. One assumption is that when one configuration contains configuration information of another entity, that that configuration is then stored in a separate configuration file and referenced by type corresponds to filename and the name of the configuration in the file.

### Examples:
Assume that we have an application called data_mover. Then for this application, running in local mode, the configuration will be stored at .data_mover at the $HOME path.

main.yml
```yaml
version: 1

system_1:
  obj_type: ClassA
  param_1: something
  param_2: other
  _dependencies_:
    - var_name: db_conn
      var_scope: secret
      name: dev_pg
      type: database
```

database.yaml
```yaml
version: 1

dev_pg:
  obj_type: PostgresDB
  user: user
  password: password
  host: 10.0.0.7
  database: root
```

The usage patter would be something like this:
main.py
```python
from pydyna.management.object_factory import ObjectFactory
from confizzo.multifile.config_manager import ConfigManager

def main():
    ConfigManager.config_root = '~/.data_mover/config.yml'

    system_1 = ObjectFactory.generate(config_name='system_1')
    system_1.run()
```

system_1.py
```python
from pydyna.management.object_factory import ObjectFactory
from confizzo.multifile.parser import Parser


class System1:
    def __init__(self, config_name: str):
        self.__config = Parser.get(config_name)
        
        self.__db_conn = ObjectFactory.generate(config_name=self.__config['_dependencies_'])

    def run(self):
        self.__db_conn.execute('SELECT 1')

```

postgres_db.py
```python
from confizzo.multifile.parser import Parser


class PostgresDB:
    
    def __init__(self, config_name: str):
        # Configuration contains secrets, so we don't want to expose this except when executing a query.
        self.__config_name = config_name 

    def execute(self, query: str):
        conf = Parser.get(self.__config_name)
        conn = self.__get_connection(conf)

        conn.cursor.execute(query)
        conn.close()
```
