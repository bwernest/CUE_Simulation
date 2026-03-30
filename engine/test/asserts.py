"""___Modules___________________________________________________________________________________"""

# Python
from numpy import ndarray, round
from numpy import int64
from typing import Any, Dict, Iterable, List, Optional, Tuple

"""___Classes___________________________________________________________________________________"""


class Assert():

    def _analyseError(self, *args) -> str:
        error_msg = "\n"
        for a, arg in enumerate(args):
            error_msg += f"argument {a + 1} :\n{arg}\n"
        return error_msg

    def assertEqual(self, expected: Any, result: Any, rounder: Optional[int] = None):
        rounder = 64 if rounder is None else rounder
        self.assertIsInstance(result, type(expected), "The two arguments must be of the same type")
        assert_method = {
            type(None): self._assertNoneEqual,
            bool: self._assertBoolEqual,
            int: self._assertValueEqual,
            float: self._assertValueEqual,
            str: self._assertTextEqual,
            tuple: self._assertListEqual,
            list: self._assertListEqual,
            type({}.keys()): self._assertListEqual,
            type({}.values()): self._assertListEqual,
            type({}.items()): self._assertListEqual,
            dict: self._assertDictEqual,
            ndarray: self._assertArrayEqual,
        }
        try:
            return assert_method[type(expected)](expected, result, rounder=rounder)
        except KeyError:
            assert expected == result, self._analyseError(expected, result)

    def _assertNoneEqual(self, a: None, b: None, rounder: Optional[int] = None) -> None:
        assert a is None and b is None, self._analyseError(a, b)

    def _assertBoolEqual(self, a: bool, b: bool, rounder: Optional[int] = None) -> None:
        assert a is b, self._analyseError(a, b)

    def _assertValueEqual(self, a: int | float, b: int | float, rounder: int) -> None:
        assert round(a, rounder) == round(b, rounder), self._analyseError(a, b)

    def _assertTextEqual(self, text1: str, text2: str, **kwargs) -> None:
        assert text1 == text2, self._analyseError(text1, text2)

    def _assertListEqual(self, list1: List | Tuple, list2: List | Tuple, rounder: int) -> None:
        self.assertEqual(len(list1), len(list2))
        for item1, item2 in zip(list1, list2):
            self.assertEqual(item1, item2, rounder)

    def _assertDictEqual(self, dict1: Dict, dict2: Dict, rounder: int) -> None:
        self.assertEqual(len(list(dict1.keys())), len(list(dict2.keys())))
        for key, value in dict1.items():
            self.assertIn(key, dict2)
            self.assertEqual(value, dict2[key], rounder)

    def _assertArrayEqual(self, array1: ndarray, array2: ndarray, rounder: int) -> None:
        array1 = round(array1, rounder)
        array2 = round(array2, rounder)
        assert (array1 == array2).all()

    def assertIsInstance(self, obj: Any, _type: type, error_msg: Optional[str] = None) -> None:
        error_msg = f"L'objet {obj} n'est pas de classe {_type} mais {type(obj)}"
        for duo in self.same_types:
            if type(obj) in duo and _type in duo:
                return
        assert isinstance(obj, _type), error_msg

    def assertIsNotInstance(self, obj: Any, _type: type, error_msg: Optional[str] = None) -> None:
        error_msg = f"L'objet {obj} est bien de type {_type}"
        assert not isinstance(obj, _type)

    @property
    def same_types(self) -> List[List[type]]:
        return [
            [int, int64]
        ]

    def assertIn(self, obj: Any, iterable: Iterable) -> None:
        assert obj in iterable, self._analyseError(obj, iterable)

    def assertNotIn(self, obj: Any, iterable: Iterable) -> None:
        assert not obj in iterable
