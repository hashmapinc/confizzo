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

from confizzo.ConfizzoError import ConfizzoError


class ConfigManager:
    """
    Configuration manager class for multifile configuration config registration. Not that no actual configuration information is stored in the registry, only
    the configuration name and the file in which it is located.
    """
    __registry: dict = {}
    __config_root: str = None
    __config_dir: str = None

    @classmethod
    def set_config_root(cls, root_path: str) -> None:
        cls.__config_root = os.path.abspath(root_path)

        cls.__generate_registry()

    @classmethod
    def __register(cls, key: str, value: str) -> None:
        """
        Register configuration entry given key and value
        Args:
            key: name of configuration value
            value: filename that will be registered

        """
        if key not in cls.__registry.keys():
            cls.__registry[key] = value

    @classmethod
    def __generate_registry(cls) -> None:
        """
        Generate a registry of configurations given the root configuration.
        Returns:

        Raises:
            ValueError: When the path for the configuration root file is not a valid file.
        """
        if not os.path.isfile(cls.__config_root) and not os.path.splitext(cls.__config_root)[1].lower() in ['.yml', '.yaml']:
            raise ValueError('Path specified in config_root is not a valid file')

        # Get the directory name for the registry
        cls.__config_dir = os.path.dirname(cls.__config_root)

        next_entries = cls.__get_next_and_register_current(path=cls.__config_root)

        # A root configuration can point to additional configurations.
        while len(next_entries) > 0:
            new_next_entries = []

            # Iterate over all configuration entries. Additional entries will be added if there are _dependencies_ fields located in the configuration.
            # Otherwise only the configurations are added to the registry
            _ = [
                new_next_entries.extend(
                    cls.__get_next_and_register_current(path=cls.__find_file(os.path.join(cls.__config_dir, entry['conf_type'])))
                )
                for entry in next_entries
                if cls.__validate_entry(entry)
            ]

            next_entries = new_next_entries

    @classmethod
    def __validate_entry(cls, entry: dict) -> bool:

        errors = []
        if 'conf_type' not in entry.keys():
            errors.append("conf_type not found in entry.")

        if 'var_name' not in entry.keys():
            errors.append("var_name not found in entry.")

        if 'name' not in entry.keys():
            errors.append("name not found in entry.")

        if len(errors) > 0:
            raise ConfizzoError(f"The following error were identified:/n{'/n'.join(errors)}")

        return True

    @classmethod
    def __find_file(cls, file_base_name: str) -> str:
        """
        Identify the file that matches a base filename (without an extension).

        Args:
            file_base_name: Name of file sought after without extension, but with directory.

        Returns:

        Raises:
            ConfizzoError: When file sought are not found within appropriate constraint.

        """

        directory = os.path.dirname(file_base_name)
        file_base = os.path.basename(file_base_name)

        # Identify all files in the directory.
        files = [
            os.path.join(directory, entry)
            for entry in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, entry))
        ]

        # Find all files which match the base file name pattern.
        potential_matches = [
            file
            for file in files
            if file_base == os.path.splitext(os.path.basename(file))[0]
        ]

        # Filter to only files which match allowed extension patterns
        potential_matches = [
            file
            for file in potential_matches
            if os.path.splitext(file)[1].lower() in ['.yml', '.yaml']
        ]

        # Oops - looks like we have more than one file that matches the pattern,
        if len(potential_matches) > 1:
            raise ConfizzoError(f"More than one file with name {file_base} (absent extension) was found.")

        # Yikes - we seem to have not identified the configuration.
        if len(potential_matches) == 0:
            raise ConfizzoError(f"No configuration files for {file_base} were found.")

        return potential_matches[0]

    @classmethod
    def __get_next_and_register_current(cls, path: str) -> list:
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
            conf.pop('version')

        # Create new registy entires for all newly read configurations
        _ = [cls.__register(key, path) for key, value in conf.items()]

        # File all of the entries due to dependencies.
        next_entries = []

        _ = [next_entries.extend(conf[key]['_dependencies_']) for key in conf.keys() if '_dependencies_' in conf[key].keys()]

        return next_entries

    @classmethod
    def get(cls, key: str) -> str:
        """
        Retrieve configuration from the registry.

        Args:
            key: key to the configuration.

        Returns: name of file where the registry entry will be found.

        Raises:
            ConfizzoError: When the key is not present in the registry.

        """
        if key not in cls.__registry.keys():
            raise ConfizzoError(f"{key} not present in configuration registry.")

        return cls.__registry[key]
