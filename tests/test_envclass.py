from os import environ

from unittest import TestCase
from unittest.mock import patch

from envclass import EnvClass

env = {
    'STR0': 'env_test',

    'INT1': '0',
    'INT2': '-1',
    'INT3': '2',
    'INT3': '134',

    'FLOAT1': '2.0',
    'FLOAT2': '0',
    'FLOAT3': '.4',
    'FLOAT4': '134.60',

    'BOOL1': 'False',
    'BOOL2': 'false',
    'BOOL3': '0',
    'BOOL4': '1',
}


class TestEnvClass(TestCase):
    @patch.dict(environ, env)
    def test_attribute_default(self):
        class MyEnv(EnvClass):
            default: str = 'env_test' 
            str0: str 

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.str0, 'env_test')
        self.assertEqual(my_env.default, 'env_test')


    @patch.dict(environ, env)
    def test_attribute_str(self):
        class MyEnv(EnvClass):
            str0: str

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.str0, 'env_test')


    @patch.dict(environ, env)
    def test_attribute_int(self):
        class MyEnv(EnvClass):
            int1: int 
            int2: int 
            int3: int 
            int4: int 

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.int1, 0)
        self.assertEqual(my_env.int2, -1)
        self.assertEqual(my_env.int3, 2)
        self.assertEqual(my_env.int4, 134)

    @patch.dict(environ, env)
    def test_attribute_bool(self):
        class MyEnv(EnvClass):
            bool1: int 
            bool2: int 
            bool3: int 
            bool4: int 

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.bool1, False)
        self.assertEqual(my_env.bool2, False)
        self.assertEqual(my_env.bool3, False)
        self.assertEqual(my_env.bool4, True)
