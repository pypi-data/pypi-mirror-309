## Install Anypush
```python
pip install gym-pushany
```

## Example
```python
import gymnasium as gym
import gym_pushany

# OBJECT_NAME_LIST = [
#     't',
#     '0',
#     '1',
#     '2',
#     '3',
#     '4',
#     '5',
#     '6',
#     '7',
#     '8',
#     '9',
#     'ellipse',
#     'rectangle',
#     'reg3',
#     'reg4',
#     'reg5',
#     'reg6',
#     'reg7',
#     'reg8',
#     'reg9',
#     'reg10'
# ]

object_name = 'ellipse'  
use_obstacles = True     
env = gym.make("pushany/PushAny-v0", object_name=object_name, use_obstacles=use_obstacles)
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    image = env.render()

    print(f'terminated: {terminated}, truncated: {truncated}')
    if terminated or truncated:
        observation, info = env.reset()

env.close()
```
