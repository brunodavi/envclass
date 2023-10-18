import os

from unittest import TestCase
from unittest.mock import Mock, patch

from tempfile import NamedTemporaryFile

from envclass import EnvClass


class TestEnvClassFeatures(TestCase):
    @patch.dict(os.environ, {'A': '1', 'B': '2', 'C': '3'})
    def test_attribute_1_letter(self):
        class OneLetter(EnvClass):
            a: int = 1
            b: int = 2
            c: int = 3

        one_letter = OneLetter()

        self.assertEqual(one_letter.a, 1)
        self.assertEqual(one_letter.b, 2)
        self.assertEqual(one_letter.c, 3)

    @patch.dict(os.environ, {'DB_CONNECTION': 'ok'})
    def test_attribute_prefix(self):
        class DataBase(EnvClass):
            _prefix = 'DB'

            connection: str

        db = DataBase()
        self.assertEqual(db.connection, 'ok')

    @patch.dict(os.environ, {'DB__KEY': '123'})
    def test_attribute_joiner(self):
        class DataBase(EnvClass):
            _prefix = 'DB'
            _joiner = '__'

            key: str

        db = DataBase()
        self.assertEqual(db.key, '123')

    @patch.dict(os.environ, {'SERVICE_API_KEY': 'token'})
    def test_attribute_class_prefix(self):
        class ServiceApi(EnvClass):
            _class_as_prefix = True

            key: str

        api = ServiceApi()
        self.assertEqual(api.key, 'token')

    @patch.dict(os.environ, {'SERVICE_API_ADMIN': 'False'})
    def test_prefix_collision(self):
        class CloudService(EnvClass):
            _class_as_prefix = True
            _prefix = 'SERVICE_API'

            admin: bool

        api = CloudService()
        self.assertEqual(api.admin, False)


    def test_load_env(self):
        class LoadEnv(EnvClass):
            testing: bool

            host: str
            port: int

            none: None

        with NamedTemporaryFile(delete=False) as tmp:
            env_content = '\n'.join((
                'TESTING=true',
                '',
                '# 1 + 1 = 2',
                'HOST=localhost',
                'PORT=1234',
                'NONE='
            )).encode()

            tmp.write(env_content)

        load_env = LoadEnv(tmp.name)

        self.assertEqual(load_env.testing, True)
        self.assertEqual(load_env.host, 'localhost')
        self.assertEqual(load_env.port, 1234)
        self.assertEqual(load_env.none, None)

        os.remove(tmp.name)

    @patch('envclass.EnvClass.parse_env')
    def test_load_env_false(self, mock_open: Mock):
        class LoadEnvFalse(EnvClass):
            _load_env = False

            key: str = '123'

        LoadEnvFalse()
        mock_open.assert_not_called()

    def test_attribute_strict_false(self):
        class MyEnv(EnvClass):
            _strict = False

            attribute_not_exists: bool

        my_env = MyEnv()
        self.assertEqual(my_env.attribute_not_exists, None)

    def test_attribute_strict_true(self):
        class MyEnv(EnvClass):
            attribute_not_exists: bool

        with self.assertRaises(KeyError):
            MyEnv()


    def test_attribute_default(self):
        class MyEnv(EnvClass):
            default_str: str = 'env_test' 
            default_int: int = 1 
            default_float: float = 1.5 
            default_bool: bool = True

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.default_str, 'env_test')
        self.assertEqual(my_env.default_int, 1)
        self.assertEqual(my_env.default_float, 1.5)
        self.assertEqual(my_env.default_bool, True)


class TestEnvClassTypes(TestCase):
    def setUp(self):
        env = {
            'STR0': '',
            'STR1': 'env_test',

            'INT0': '',
            'INT1': '0',
            'INT2': '-1',
            'INT3': '2',
            'INT4': '134',

            'FLOAT0': '',
            'FLOAT1': '2.0',
            'FLOAT2': '0',
            'FLOAT3': '.4',
            'FLOAT4': '134.60',

            'BOOL0': '',
            'BOOL1': 'False',
            'BOOL2': 'True',
            'BOOL3': '0',
            'BOOL4': '1',
        }

        self.patcher = patch.dict(os.environ, env)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()


    def test_attribute_str(self):
        class MyEnv(EnvClass):
            str0: str
            str1: str

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.str0, None)
        self.assertEqual(my_env.str1, 'env_test')

    def test_attribute_int(self):
        class MyEnv(EnvClass):
            int0: int 
            int1: int 
            int2: int 
            int3: int 
            int4: int 

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.int0, None)
        self.assertEqual(my_env.int1, 0)
        self.assertEqual(my_env.int2, -1)
        self.assertEqual(my_env.int3, 2)
        self.assertEqual(my_env.int4, 134)

    def test_attribute_float(self):
        class MyEnv(EnvClass):
            float0: float 
            float1: float 
            float2: float 
            float3: float 
            float4: float 

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.float0, None)
        self.assertEqual(my_env.float1, 2.0)
        self.assertEqual(my_env.float2, 0)
        self.assertEqual(my_env.float3, .4)
        self.assertEqual(my_env.float4, 134.60)

    def test_attribute_bool(self):
        class MyEnv(EnvClass):
            bool0: bool
            bool1: bool
            bool2: bool 
            bool3: bool 
            bool4: bool 

        my_env = MyEnv(env_file='.env')

        self.assertEqual(my_env.bool0, None)
        self.assertEqual(my_env.bool1, False)
        self.assertEqual(my_env.bool2, True)
        self.assertEqual(my_env.bool3, False)
        self.assertEqual(my_env.bool4, True)
