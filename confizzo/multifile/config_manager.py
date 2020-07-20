# Modifications © 2020 Hashmap, Inc
#
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
import os

import yaml


class ConfigManager:
    """
    Configuration manager class for multifile configuration config registration. Not that no actual configuration information is stored in the registry, only
    the configuration name and the file in which it is located.
    """
    registry: dict = {}
    config_root: str = None
    __config_dir: str = None

    @classmethod
    def __register(cls, key: str, value: str) -> None:
        """
        Register configuration entry given key and value
        Args:
            key: name of configuration value
            value: filename that will be registered

        Raises:
            ValueError: When the registration is invalid.

        """
        if key not in cls.registry.keys():
            cls.registry[key] = value
        else:
            raise ValueError('Configuration with value % already exists, duplication registrations are not allowed.', key)

    @classmethod
    def __generate_registry(cls) -> None:
        """
        Generate a registry of configurations given the root configuration.
        Returns:

        Raises:
            ValueError: When the path for the configuration root file is not a valid file.
        """
        if not os.path.isfile(cls.config_root) and not os.path.splitext(cls.config_root)[1].lower() in ['.yml', '.yaml']:
            raise ValueError('Path specified in config_root is not a valid file')

        # Get the directory name for the registry
        cls.__config_dir = os.path.dirname(cls.config_root)

        next_entries = cls.__get_next_entries_and_registry_configurations(path=cls.config_root)

        # A root configuration can point to additional configurations.
        while len(next_entries) > 0:
            new_next_entries = []

            # Itereate over all configuration entries. Additional entries will be added if there are _dependendenices_ fields located in the configuration.
            # Otherwise only the configurations are added to the registry
            _ = [new_next_entries.extend(cls.__get_next_entries_and_registry_configurations(path=os.path.join(cls.__config_dir, entry['type'])))
                 for entry in next_entries
                 ]

            next_entries = new_next_entries

    @classmethod
    def __get_next_entries_and_registry_configurations(cls, path: str) -> list:
        """
        Get next configuration entries given a path to a configuration file. The configuration contents are captured and the dependencies are extracted so that
        they can be registered as well.

        Args:
            path: path to a configuration file

        Returns: list of configuration dependencies

        """
        with open(path, 'r') as stream:
            conf = yaml.safe_load(stream)

        #  We are not dealing with versions at this time.
        if 'version' in conf.keys():
            conf.remove('version')

        # Create new registy entires for all newly read configurations
        _ = [cls.__register(key, path) for key, value in conf.items()]

        # File all of the entries due to dependencies.
        next_entries = []
        _ = [next_entries.extend(entry['_dependencies_']) for _, entry in conf if '_dependencies_' in entry.keys()]

        return next_entries

    @classmethod
    def get(cls, key: str) -> str:
        """
        Retrieve configuration from the registry.

        Args:
            key: key to the configuration.

        Returns: name of file where the registry entry will be found.

        Raises:
            AttributeError: When the config_root has not been set.

        """
        if not cls.registry:
            if not cls.config_root:
                raise AttributeError('In class ConfigManager class variable config_root has not been set.')
            cls.__generate_registry()

        return cls.registry[key]
