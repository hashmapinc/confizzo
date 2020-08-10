[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgitlab.com%2Fhashmapinc%2Fctso%2Futilities%2Fconfizzo.svg?type=shield)](https://app.fossa.com/projects/git%2Bgitlab.com%2Fhashmapinc%2Fctso%2Futilities%2Fconfizzo?ref=badge_shield)
[![codecov](https://codecov.io/gl/hashmapinc:ctso:utilities/confizzo/branch/%5Cx646576656c6f706d656e74/graph/badge.svg?token=ITYIXT92BE)](https://codecov.io/gl/hashmapinc:ctso:utilities/confizzo)
# confizzo

confizzo is a configuration management library. It is designed to contain many versions of configuration managed approaches into a single API.

## Multi-file Configurations

Multifile configurations, in confizzo terms, are configurations which are partitioned into multiple files. One assumption is that when one configuration contains configuration information of another entity, that that configuration is then stored in a separate configuration file and referenced by type corresponds to filename and the name of the configuration in the file.

### Specifications

Here the configuration is parsed into one or more files. When a configuration has a dependency on another object - via composition - the configuration for such 
objects will be stored in separate files. ALl objects of similar type - save the entry point objects, will be stored in files denoted by name the kind of class 
(via vase class) for which they will configure. In the 'main.yml' - the entrypoint configuration - the configurations will be 

````yaml
object:
  type: class_type
  conf: SOME CONFIGURATION DICTIONARY
  _dependencies_:
    - List of dependency descriptions
````

The list of dependency descriptions will have objects as follows
```yaml
  var_name: NAME OF THE VARIABLE (COMPOSED OBJECT) THIS CONFIGURATION WILL BELONG TO
  name: NAME OF CONFIGURATION FROM THE CONF_TYPE LOCATION
  conf_type: IDENTIFIES THE KIND OF CONFIGURATION - WHERE THEY WILL BE STORED.
```

The \_dependencies\_ section is used to
1. Help populate the configuration repository
1. Used to identify the references to the Class that can be dynamically injected and to reference the right configuration

The pattern aimed to be used here is to
1. Create an object from it's configuration (non-injectable objects)
1. From \_dependencies\_ find the Class that will be constructed and the name (as a passable conf value) of the key used to reference that objects configuration.

### Examples
Assume that we have an application called data_mover. Then for this application, running in local mode, the configuration will be stored at .data_mover at the $HOME path.

main.yml
```yaml
version: 1

system_1:
  type: ClassA
  conf:
    param_1: something
    param_2: other
  _dependencies_:
    - var_name: db_conn
      name: dev_pg
      conf_type: database
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
from providah.factories.package_factory import PackageFactory
from confizzo.multifile.config_manager import ConfigManager
from confizzo.multifile.parser import Parser

def main():
    ConfigManager.config_root = '~/.data_mover/config.yml'
    
    conf_key = 'ClassA' 
    config = Parser.get(conf_key)
    obj_type = config.pop('type')

    system_1 = PackageFactory.create(key=obj_type, **{'conf_key': conf_key})
    system_1.run()
```

system_1.py
```python
from providah.factories.package_factory import PackageFactory
from confizzo.multifile.parser import Parser


class System1:
    def __init__(self, conf_key: str):
        self.__config = Parser.get(conf_key)
        
        dependencies = self.__config['_dependencies_']
        conf_for_db_conn_ref = [dep for dep in dependencies if dep['var_name'] == 'db_conn']
        self.__db_conn = PackageFactory.create(key=Parser.get(conf_for_db_conn_ref['type']), 
                                               **{'conf_key': conf_for_db_conn_ref['name']})

    def run(self):
        self.__db_conn.execute('SELECT 1')

```

postgres_db.py
```python
from confizzo.multifile.parser import Parser


class PostgresDB:
    
    def __init__(self, conf_key: str):
        # Configuration contains secrets, so we don't want to expose this except when executing a query.
        self.__config_name = conf_key 

    def execute(self, query: str) -> None:
        conf = Parser.get(self.__config_name)['conf']
        conn = self.__get_connection(conf)

        conn.cursor.execute(query)
        conn.close()

    def __get_connection(self, conf: str) -> Connection:
        pass
```

## TODO
There are a number of feature that could be added
1. Simpler reference of dependencies from configuration using library and avoiding bespoke solution and 
1. Additional filtering when referencing configurations
1. Additional configuration that ties to providah package (maybe)