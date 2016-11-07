"""test define_subject modulue."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest
from wikipedia.exceptions import DisambiguationError


@pytest.mark.parametrize('func_input', ['', 'define'])
def test_multiple_input(func_input):
    """test with empty speech.

    it raise error because it don't have word 'define'.
    """
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.define_subject.tts') as m_tts:
            from melissa.actions import define_subject
            if func_input == '':
                with pytest.raises(ValueError):
                    define_subject.define_subject('')
            elif func_input == 'define':
                define_subject.define_subject(func_input)
                m_tts.assert_called_once_with(
                    'define requires subject words')


def test_word_define_define():
    """test word 'define define'."""
    func_input = 'define define'
    summary_result = (
        'A definition is a statement of the meaning of a term (a word, '
        'phrase, or other set of symbols). Definitions can be classified '
        'into two large categories, intensional definitions (which try to '
        'give the essence of a term) and extensional definitions (which '
        'proceed by listing the objects that a term describes).'
    )
    expected_tts_input = (
        'A definition is a statement of the meaning of a term . '
        'Definitions can be classified into two large categories, '
        'intensional definitions and extensional definitions .'
    )
    with mock.patch('melissa.actions.define_subject.tts') as m_tts, \
            mock.patch('melissa.actions.define_subject.wikipedia') \
            as m_wiki:
        m_wiki.summary.return_value = summary_result
        from melissa.actions import define_subject
        define_subject.define_subject(func_input)
        m_tts.assert_called_once_with(expected_tts_input)
        m_wiki.summary.assert_called_once_with('define', sentences=5)


def test_raise_wiki_disambiguation_error():
    """test word 'define define'."""
    # NOTE: the function still didn't DisambiguationError
    func_input = 'define define'
    m_err_title = 'mock_title'
    m_err_mrt = ['mock_option']  # mrt: may_refer_to
    with mock.patch('melissa.actions.define_subject.tts') as m_tts, \
            mock.patch('melissa.actions.define_subject.wikipedia') \
            as m_wiki:
        m_wiki.summary.side_effect = \
            DisambiguationError(
                m_err_title,
                m_err_mrt
            )
        from melissa.actions import define_subject
        with pytest.raises(DisambiguationError):
            define_subject.define_subject(func_input)
        m_tts.assert_not_called()
        m_wiki.summary.assert_called_once_with('define', sentences=5)
