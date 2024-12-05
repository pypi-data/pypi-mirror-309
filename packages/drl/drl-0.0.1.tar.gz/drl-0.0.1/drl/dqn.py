import numpy as np
import pandas as pd


class DQNReplayer:
    def __init__(self, capacity):
        self.memory = pd.DataFrame(index=range(capacity),
                columns=['state', 'action', 'reward', 'next_state', 'terminated'])
        self.i = 0
        self.count = 0
        self.capacity = capacity

    def store(self, *args):
        self.memory.loc[self.i] = np.asarray(args, dtype=object)
        self.i = (self.i + 1) % self.capacity
        self.count = min(self.count + 1, self.capacity)

    def sample(self, size):
        indices = np.random.choice(self.count, size=size)
        return (np.stack(self.memory.loc[indices, field]) for field in
                self.memory.columns)


try:
    import tensorflow.compat.v2 as tf
    from tensorflow import nn
    from tensorflow import losses
    from tensorflow import optimizers
    from tensorflow import keras
    from tensorflow.keras import layers
    from tensorflow.keras import models
    
    class DQNAgent:
        def __init__(self, env):
            self.action_n = env.action_space.n
            self.gamma = 0.99

            self.replayer = DQNReplayer(10000)

            self.evaluate_net = self.build_net(
                    input_size=env.observation_space.shape[0],
                    hidden_sizes=[64, 64], output_size=self.action_n)
            self.target_net = models.clone_model(self.evaluate_net)

        def build_net(self, input_size, hidden_sizes, output_size):
            model = keras.Sequential()
            for layer, hidden_size in enumerate(hidden_sizes):
                kwargs = dict(input_shape=(input_size,)) if not layer else {}
                model.add(layers.Dense(units=hidden_size,
                        activation=nn.relu, **kwargs))
            model.add(layers.Dense(units=output_size))
            optimizer = optimizers.Adam(0.001)
            model.compile(loss=losses.mse, optimizer=optimizer)
            return model

        def reset(self, mode=None):
            self.mode = mode
            if self.mode == 'train':
                self.trajectory = []
                self.target_net.set_weights(self.evaluate_net.get_weights())

        def step(self, observation, reward, terminated):
            if self.mode == 'train' and np.random.rand() < 0.001:
                # epsilon-greedy policy in train mode
                action = np.random.randint(self.action_n)
            else:
                qs = self.evaluate_net.predict(observation[np.newaxis], verbose=0)
                action = np.argmax(qs)
            if self.mode == 'train':
                self.trajectory += [observation, reward, terminated, action]
                if len(self.trajectory) >= 8:
                    state, _, _, act, next_state, reward, terminated, _ = \
                            self.trajectory[-8:]
                    self.replayer.store(state, act, reward, next_state, terminated)
                if self.replayer.count >= self.replayer.capacity * 0.95:
                        # skip first few episodes for speed
                    self.learn()
            return action

        def close(self):
            pass

        def learn(self):
            # replay
            states, actions, rewards, next_states, terminateds = \
                    self.replayer.sample(1024)

            # update value net
            next_qs = self.target_net.predict(next_states, verbose=0)
            next_max_qs = next_qs.max(axis=-1)
            us = rewards + self.gamma * (1. - terminateds) * next_max_qs
            targets = self.evaluate_net.predict(states, verbose=0)
            targets[np.arange(us.shape[0]), actions] = us
            self.evaluate_net.fit(states, targets, verbose=0)
except:
    pass

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    
    class DQNAgent:
        def __init__(self, env):
            self.action_n = env.action_space.n
            self.gamma = 0.99

            self.replayer = DQNReplayer(10000)

            self.evaluate_net = self.build_net(
                    input_size=env.observation_space.shape[0],
                    hidden_sizes=[64, 64], output_size=self.action_n)
            self.optimizer = optim.Adam(self.evaluate_net.parameters(), lr=0.001)
            self.loss = nn.MSELoss()

        def build_net(self, input_size, hidden_sizes, output_size):
            layers = []
            for input_size, output_size in zip(
                    [input_size,] + hidden_sizes, hidden_sizes + [output_size,]):
                layers.append(nn.Linear(input_size, output_size))
                layers.append(nn.ReLU())
            layers = layers[:-1]
            model = nn.Sequential(*layers)
            return model

        def reset(self, mode=None):
            self.mode = mode
            if self.mode == 'train':
                self.trajectory = []
                self.target_net = copy.deepcopy(self.evaluate_net)

        def step(self, observation, reward, terminated):
            if self.mode == 'train' and np.random.rand() < 0.001:
                # epsilon-greedy policy in train mode
                action = np.random.randint(self.action_n)
            else:
                state_tensor = torch.as_tensor(observation,
                        dtype=torch.float).squeeze(0)
                q_tensor = self.evaluate_net(state_tensor)
                action_tensor = torch.argmax(q_tensor)
                action = action_tensor.item()
            if self.mode == 'train':
                self.trajectory += [observation, reward, terminated, action]
                if len(self.trajectory) >= 8:
                    state, _, _, act, next_state, reward, terminated, _ = \
                            self.trajectory[-8:]
                    self.replayer.store(state, act, reward, next_state, terminated)
                if self.replayer.count >= self.replayer.capacity * 0.95:
                        # skip first few episodes for speed
                    self.learn()
            return action

        def close(self):
            pass

        def learn(self):
            # replay
            states, actions, rewards, next_states, terminateds = \
                    self.replayer.sample(1024)
            state_tensor = torch.as_tensor(states, dtype=torch.float)
            action_tensor = torch.as_tensor(actions, dtype=torch.long)
            reward_tensor = torch.as_tensor(rewards, dtype=torch.float)
            next_state_tensor = torch.as_tensor(next_states, dtype=torch.float)
            terminated_tensor = torch.as_tensor(terminateds, dtype=torch.float)

            # update value net
            next_q_tensor = self.target_net(next_state_tensor)
            next_max_q_tensor, _ = next_q_tensor.max(axis=-1)
            target_tensor = reward_tensor + self.gamma * \
                    (1. - terminated_tensor) * next_max_q_tensor
            pred_tensor = self.evaluate_net(state_tensor)
            q_tensor = pred_tensor.gather(1, action_tensor.unsqueeze(1)).squeeze(1)
            loss_tensor = self.loss(target_tensor, q_tensor)
            self.optimizer.zero_grad()
            loss_tensor.backward()
            self.optimizer.step()
