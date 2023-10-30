import os, sys, io

from unittest import TestCase
from unittest.mock import Mock, patch

from envclass import EnvClass


class TestEnvClassFeatures(TestCase):
    @patch.dict(os.environ, {'A': 'False', 'B': 'True', 'C': '3'})
    def test_attribute_as_env_representation(self):
        class Repl(EnvClass):
            A: str
            B: bool
            C: int

        env_repl_expected = '\n'.join([
            "A='False'",
            "B=True",
            "C=3",
        ])
        saved_stdout = sys.stdout

        try:
            out = io.StringIO()
            sys.stdout = out
            print(Repl)
            output = out.getvalue().strip()
            self.assertEqual(output, env_repl_expected)
        finally:
            sys.stdout = saved_stdout

    @patch.dict(os.environ, {'READ_ONLY': 'True'})
    def test_attribute_is_read_only(self):
        class Vault(EnvClass):
            READ_ONLY: bool

        with self.assertRaises(AttributeError):
            Vault.READ_ONLY = False

    @patch.dict(os.environ, {'A': '1', 'B': '2', 'C': '3'})
    def test_attribute_1_letter(self):
        class OneLetter(EnvClass):
            A: int
            B: int
            C: int

        self.assertEqual(OneLetter.A, 1)
        self.assertEqual(OneLetter.B, 2)
        self.assertEqual(OneLetter.C, 3)

    @patch.dict(os.environ, {'DB_CONNECTION': 'ok'})
    def test_attribute_prefix(self):
        class DataBase(EnvClass):
            _prefix = 'DB'

            CONNECTION: str

        self.assertEqual(DataBase.CONNECTION, 'ok')

    def test_load_env_file(self):
        env_content = '\n'.join((
            'TESTING=true',
            '',
            '# 1 + 1 = 2',
            'HOST=localhost',
            'PORT=1234',
            'NONE='
        ))

        with open('.env', 'w') as dotenv:
            dotenv.write(env_content)

        class LoadEnv(EnvClass):
            _env_file = '.env'

            TESTING: bool

            HOST: str
            PORT: int

            NONE: None

        self.assertEqual(LoadEnv.TESTING, True)
        self.assertEqual(LoadEnv.HOST, 'localhost')
        self.assertEqual(LoadEnv.PORT, 1234)
        self.assertEqual(LoadEnv.NONE, None)

        os.remove('.env')

    @patch('envclass.metaclass.MetaClass.parse_env')
    def test_env_file_not_set(self, mock_open: Mock):
        class EnvFileNotSet(EnvClass):
            KEY: str = '123'

        mock_open.assert_not_called()

    def test_attribute_strict_false(self):
        class MyEnv(EnvClass):
            _strict = False

            ATTRIBUTE_NOT_EXISTS: bool

        self.assertEqual(MyEnv.ATTRIBUTE_NOT_EXISTS, None)

    def test_attribute_strict_true(self):
        with self.assertRaises(KeyError):
            class MyEnv(EnvClass):
                ATTRIBUTE_NOT_EXISTS: bool

    def test_attribute_default(self):
        class MyEnv(EnvClass):
            DEFAULT_STR: str = 'env_test' 
            DEFAULT_INT: int = 1 
            DEFAULT_FLOAT: float = 1.5 
            DEFAULT_BOOL: bool = True

        self.assertEqual(MyEnv.DEFAULT_STR, 'env_test')
        self.assertEqual(MyEnv.DEFAULT_INT, 1)
        self.assertEqual(MyEnv.DEFAULT_FLOAT, 1.5)
        self.assertEqual(MyEnv.DEFAULT_BOOL, True)


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
            STR0: str
            STR1: str

        self.assertEqual(MyEnv.STR0, None)
        self.assertEqual(MyEnv.STR1, 'env_test')

    def test_attribute_int(self):
        class MyEnv(EnvClass):
            INT0: int 
            INT1: int 
            INT2: int 
            INT3: int 
            INT4: int 

        self.assertEqual(MyEnv.INT0, None)
        self.assertEqual(MyEnv.INT1, 0)
        self.assertEqual(MyEnv.INT2, -1)
        self.assertEqual(MyEnv.INT3, 2)
        self.assertEqual(MyEnv.INT4, 134)

    def test_attribute_float(self):
        class MyEnv(EnvClass):
            FLOAT0: float 
            FLOAT1: float 
            FLOAT2: float 
            FLOAT3: float 
            FLOAT4: float 

        self.assertEqual(MyEnv.FLOAT0, None)
        self.assertEqual(MyEnv.FLOAT1, 2.0)
        self.assertEqual(MyEnv.FLOAT2, 0)
        self.assertEqual(MyEnv.FLOAT3, .4)
        self.assertEqual(MyEnv.FLOAT4, 134.60)

    def test_attribute_bool(self):
        class MyEnv(EnvClass):
            BOOL0: bool
            BOOL1: bool
            BOOL2: bool 
            BOOL3: bool 
            BOOL4: bool 

        self.assertEqual(MyEnv.BOOL0, None)
        self.assertEqual(MyEnv.BOOL1, False)
        self.assertEqual(MyEnv.BOOL2, True)
        self.assertEqual(MyEnv.BOOL3, False)
        self.assertEqual(MyEnv.BOOL4, True)
