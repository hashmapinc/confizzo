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
from unittest import TestCase

from confizzo.ConfizzoError import ConfizzoError
from confizzo.multifile.config_manager import ConfigManager


class TestConfigManager(TestCase):

    def setUp(self) -> None:
        self.__this_dir = os.path.dirname(__file__)
        ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/main.yml'))

    def test_configure(self):

        pass

    def test_read_root(self):
        expected_result = "/Users/johnaven/accelerators/confizzo/tests/multi_file/main.yml"
        root_conf = ConfigManager.get(key='system_1')
        self.assertEqual(expected_result, root_conf)

    def test_config_path(self):
        with self.assertRaises(ValueError):
            ConfigManager.set_config_root('some_bad_path')

    def test_no_conf_type(self):
        with self.assertRaises(ConfizzoError):
            ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/bad_main_1.yml'))

    def test_no_var_name(self):
        with self.assertRaises(ConfizzoError):
            ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/bad_main_4.yml'))

    def test_no_name(self):
        with self.assertRaises(ConfizzoError):
            ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/bad_main_2.yml'))

    def test_multiple_config_files_with_same_name(self):
        with self.assertRaises(ConfizzoError):
            ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/bad_main_5.yml'))

    def test_multiple_config_files_doesnt_exist(self):
        with self.assertRaises(ConfizzoError):
            ConfigManager.set_config_root(os.path.join(self.__this_dir, 'multi_file/bad_main_6.yml'))
