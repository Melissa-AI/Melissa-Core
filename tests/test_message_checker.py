"""test for message_checker module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest

from melissa.message_checker import message_checker


def test_mock_input():
    """test using mock input.

    Error is raised because mock_input is nto itterable.
    """
    mock_message = mock.Mock()
    mock_words = mock.Mock()
    with pytest.raises(TypeError):
        message_checker(mock_message, mock_words)


def test_subset_word():
    """test subset word."""
    message = 'hello world'
    words = ['hello']
    assert message_checker(message, words)


def test_not_subset_word():
    """test not subtest word."""
    message = 'hello world'
    words = ['test']
    assert not message_checker(message, words)

    message = 'hello world;'
    words = [';']
    assert not message_checker(message, words)

    message = 'hello world.'
    words = ['.']
    assert not message_checker(message, words)

    message = 'hello world.'
    words = ['world']
    assert not message_checker(message, words)
