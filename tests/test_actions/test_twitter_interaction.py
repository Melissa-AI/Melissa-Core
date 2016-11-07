"""test module."""
from StringIO import StringIO
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


@pytest.mark.parametrize('use_default_profile', [True, False])
def test_post_tweet(use_default_profile):
    """test func."""
    def_val = 'xxxx'
    default_profile = {
        'twitter': {
            'consumer_key': def_val,
            'consumer_secret': def_val,
            'access_token': def_val,
            'access_token_secret': def_val
        }
    }
    new_profile = {
        'twitter': {
            'consumer_key': 'consumer_key',
            'consumer_secret': 'consumer_secret',
            'access_token': 'access_token',
            'access_token_secret': 'access_token_secret'
        }
    }
    def_profile_error_msg = (
        'Twitter requires a consumer key and secret, '
        'and an access token and token secret.')
    m_text = mock.Mock()
    words_of_message = ['tweet', 'some', 'message']
    exp_cleaned_message = 'Some message'
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('sys.stdout', new_callable=StringIO) \
                as m_stdout, \
                mock.patch('melissa.actions.twitter_interaction.tweepy') \
                as m_tweepy, \
                mock.patch('melissa.actions.twitter_interaction.tts') \
                as m_tts:
            # pre run
            from melissa.actions import twitter_interaction
            if use_default_profile:
                twitter_interaction.profile.data = default_profile
            else:
                twitter_interaction.profile.data = new_profile
                m_text.split.return_value = words_of_message
            # run
            twitter_interaction.post_tweet(m_text)
            # test
            if use_default_profile:
                m_tts.assert_called_once_with(def_profile_error_msg)
                assert def_profile_error_msg in m_stdout.getvalue()
            else:
                m_tts.assert_called_once_with('Your tweet has been posted')
                assert not m_stdout.getvalue()
                m_text.split.assert_called_once_with()
                m_tweepy.assert_has_calls([
                    mock.call.OAuthHandler('consumer_key', 'consumer_secret'),
                    mock.call.OAuthHandler().set_access_token(
                        'access_token', 'access_token_secret'),
                    mock.call.API(m_tweepy.OAuthHandler.return_value),
                    mock.call.API().update_status(status=exp_cleaned_message)
                ])
