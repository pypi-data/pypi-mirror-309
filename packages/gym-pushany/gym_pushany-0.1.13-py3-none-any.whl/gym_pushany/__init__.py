from gymnasium.envs.registration import register
OBJECT_NAME_LIST = [
    't',
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'ellipse',
    'rectangle',
    'reg3',
    'reg4',
    'reg5',
    'reg6',
    'reg7',
    'reg8',
    'reg9',
    'reg10'
]

register(
    id='gym_pushany/PushAny-v0',
    entry_point='gym_pushany.envs:PushAnyEnv',
    max_episode_steps=300
)
