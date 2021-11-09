#!/usr/bin/env python3

import beer30
import unittest

from typing import Union

class TestLight(unittest.TestCase):
    def setUp(self):
        self.light = beer30.Light(name='test')

    def test_init(self):
        self.assertEqual(self.light.name, 'test', 'name is set')
        self.assertEqual(self.light.state, 'red', 'state is set')

    def test_state_setter(self):
        def test_valid_state(self):
            # Change the state
            self._light.state = 'green'
            self.assertEqual(self._light.state, 'green', 'state is properly set')

        # With invalid states
        with self.assertRaises(TypeError, msg='denies setting state to list'):
            self.light.state = ['list']
        with self.assertRaises(TypeError, msg='denies setting state to dict'):
            self.light.state = {'dict': 'value'}

if __name__ == '__main__':
    unittest.main()