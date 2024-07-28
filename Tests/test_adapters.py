from typing import List
import unittest

import TagScriptEngine as tse
from TagScriptEngine import Interpreter, adapter, block


def dummy_function():
    return 500


class TestVerbParsing(unittest.TestCase):
    def setUp(self):
        self.blocks: List[tse.Block] = [block.StrictVariableGetterBlock()]
        self.engine: Interpreter = Interpreter(self.blocks)

    def tearDown(self):
        self.blocks: List[tse.Block] = None  # type: ignore
        self.engine: Interpreter = None  # type: ignore

    def test_string_adapter(self):
        # Basic string adapter get
        data = {"test": adapter.StringAdapter("Hello World, How are you")}
        result = self.engine.process("{test}", data).body  # type: ignore
        self.assertEqual(result, "Hello World, How are you")

        # Slice
        result = self.engine.process("{test(1)}", data).body  # type: ignore
        self.assertEqual(result, "Hello")

        # Plus
        result = self.engine.process("{test(3+)}", data).body  # type: ignore
        self.assertEqual(result, "How are you")

        # up to
        result = self.engine.process("{test(+2)}", data).body  # type: ignore
        self.assertEqual(result, "Hello World,")

    def test_function_adapter(self):
        # Basic string adapter get
        data = {"fn": adapter.FunctionAdapter(dummy_function)}  # type: ignore
        result = self.engine.process("{fn}", data).body  # type: ignore
        self.assertEqual(result, "500")
