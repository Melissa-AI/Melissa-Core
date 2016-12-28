"""test general_conversations modulue."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


M_USER_NAME = 'm_user_name'
M_VA_NAME = 'm_va_name'
CHOICE_RETVAL = mock.Mock()


@pytest.mark.parametrize(
    'arg, tts_arg',
    [
        ('undefined', 'I dont know what that means!'),
        ('marry_me',
            'I have been receiving a lot of marriage proposals recently.'),
        ('love_you', CHOICE_RETVAL),
        ('are_you_up', 'For you sir, always.'),
        ('how_are_you', 'I am fine, thank you.'),
        ('where_born',
            'I was created by a magician named Tanay, in India, '
            'the magical land of himalayas.'),
        ('who_am_i',
            'You are {}, a brilliant person. '
            'I love you!'.format(M_USER_NAME)),
        ('how_am_i', CHOICE_RETVAL),
        ('toss_coin', CHOICE_RETVAL),
        ('who_are_you', CHOICE_RETVAL),
    ]
)
def test_general_conversation(arg, tts_arg):
    """test undefined."""
    m_text = mock.Mock()
    toss_coin_result = 'heads'
    va_name = M_VA_NAME
    with mock.patch('melissa.profile_loader.load_profile'):
        with mock.patch('melissa.actions.general_conversations.tts') \
                as m_tts, \
                mock.patch('melissa.actions.general_conversations.random') \
                as m_random:
            # run
            from melissa.actions import general_conversations
            if arg == 'toss_coin':
                general_conversations.random.choice.return_value = \
                    toss_coin_result
            elif tts_arg == CHOICE_RETVAL:
                general_conversations.random.choice.return_value = \
                    CHOICE_RETVAL
            if arg == 'who_am_i':
                general_conversations.profile.data = {
                    'name': M_USER_NAME}
            elif arg == 'who_are_you':
                general_conversations.profile.data = {
                    'va_name': M_VA_NAME}
            exec_dict = {
                'undefined': general_conversations.undefined,
                'marry_me': general_conversations.marry_me,
                'love_you': general_conversations.love_you,
                'are_you_up': general_conversations.are_you_up,
                'how_are_you': general_conversations.how_are_you,
                'where_born': general_conversations.where_born,
                'who_am_i': general_conversations.who_am_i,
                'how_am_i': general_conversations.how_am_i,
                'toss_coin': general_conversations.toss_coin,
                'who_are_you': general_conversations.who_are_you,
            }
            exec_dict[arg](m_text)
            # test
            if arg == 'toss_coin':
                m_tts.assert_called_once_with(
                    'I just flipped a coin. It shows ' + toss_coin_result
                )
            else:
                m_tts.assert_called_once_with(tts_arg)
            choice_args_dict = {
                'love_you': [
                    'I love you too.',
                    'You are looking for love in the wrong place.'
                ],
                'tell_joke': [
                    'What happens to a frogs car when it breaks down? '
                    'It gets toad away.',
                    'Why was six scared of seven? Because seven ate nine.',
                    'Why are mountains so funny? Because they are hill areas.',
                    'Have you ever tried to eat a clock?'
                    'I hear it is very time consuming.',
                    'What happened when the wheel was invented? A revolution.',
                    'What do you call a fake noodle? An impasta!',
                    'Did you hear about that new broom? '
                    'It is sweeping the nation!',
                    'What is heavy forward but not backward? Ton.',
                    'No, I always forget the punch line.'
                ],
                'how_am_i': [
                    'You are goddamn handsome!',
                    'My knees go weak when I see you.',
                    'You are sexy!',
                    'You look like the kindest person that I have met.'
                ],
                'toss_coin': ['heads', 'tails'],
                'who_are_you':  [
                    'I am ' + va_name + ', your lovely personal assistant.',
                    va_name + ', didnt I tell you before?',
                    'You ask that so many times! I am ' + va_name
                ]
            }
            if arg in choice_args_dict:
                m_random.choice.assert_called_once_with(
                    choice_args_dict[arg])
