import pytest

from src.modules.rules.board import Board as Bd


class TestBoard(object):
    def test_init_error_0(self):
        with pytest.raises(ValueError):
            b = Bd(turn=0)

    def test_init_error_1(self):
        with pytest.raises(ValueError):
            b = Bd(turn=1)

    def test_init_error_2(self):
        with pytest.raises(ValueError):
            b = Bd(turn=2)
