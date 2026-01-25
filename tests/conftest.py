import pytest
from pytest import fixture


@fixture()
def numbers():
    return [1, 2, 3, 4]


@pytest.mark.parametrize('word, correct', [('шалаш', True),
                                           ('привет', False),
                                           ('казак', True),
                                           ('ура', False)])
def test_is_palindrom(word, correct):
    assert is_palindrom(word) == correct


def test_error_is_palindrom():
    with pytest.raises(TypeError):
        is_palindrom(1)