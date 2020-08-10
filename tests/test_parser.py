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
from unittest import TestCase
import os, json

from confizzo.ConfizzoError import ConfizzoError
from confizzo.multifile.config_manager import ConfigManager
from confizzo.multifile.parser import Parser


class TestParser(TestCase):
    def setUp(self) -> None:
        self.__this_dir = os.path.dirname(__file__)

    def test_parse(self):
        ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/main.yml'))
        conf = Parser.get(configuration_name='system_1')
        expect = {
            "type": "ClassA",
            "conf": {
                "param_1": "something",
                "param_2": "other",
            },
            "_dependencies_": [
                {
                    "var_name": "db_conn",
                    "name": "dev_pg",
                    "conf_type": "database"
                }
            ]
        }

        self.assertDictEqual(expect, conf)

    def test_parse_fail(self):
        ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/main.yml'))
        with self.assertRaises(ConfizzoError):
            Parser.get(configuration_name='system_2')

    def test_parse_no_conf(self):
        ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/main_no_conf.yml'))
        with self.assertRaises(ConfizzoError):
            Parser.get(configuration_name='system_2')

    def test_parse_no_type(self):
        ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/main_no_type.yml'))
        with self.assertRaises(ConfizzoError):
            Parser.get(configuration_name='system_3')
