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
import yaml

from confizzo.ConfizzoError import ConfizzoError
from confizzo.multifile.config_manager import ConfigManager


class Parser:

    @classmethod
    def __read_config(cls, configuration_name: str) -> dict:
        """
        Retrieve configuration given the name of the configuration.

        Args:
            configuration_name: Name of configuration to use as reference.

        Returns: Configuration dictionary.

        """

        filename = ConfigManager.get(configuration_name)
        with open(filename, 'r') as stream:
            config = yaml.safe_load(stream)

        return config[configuration_name]

    @classmethod
    def get(cls, configuration_name: str) -> dict:
        """
        Obtain a configuration
        Args:
            configuration_name:

        Returns: Configuration as dict.

        Raises:
            ConfizzoError: When the configuration required values are not present.

        """

        returnable_config = cls.__read_config(configuration_name)

        if 'conf' not in returnable_config.keys():
            raise ConfizzoError("conf not present in configuration, but is required.")

        if 'type' not in returnable_config.keys():
            raise ConfizzoError('type not present in configuration, but is required.')

        return returnable_config
