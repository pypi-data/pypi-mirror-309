# from https://github.com/pypa/sampleproject/

import unittest

import example_package_sean.example as example


class TestExample(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(example.hello('world'), 'hello world')


if __name__ == '__main__':
    unittest.main()
