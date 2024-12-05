import numpy as np
import pandas as pd
import scipy.signal as signal

class PPOReplayer:
    def __init__(self):
        self.fields = ['state', 'action', 'prob', 'advantage', 'return']
        self.memory = pd.DataFrame(columns=self.fields)

    def store(self, df):
        self.memory = pd.concat([self.memory, df[self.fields]], ignore_index=True)

    def sample(self, size):
        indices = np.random.choice(self.memory.shape[0], size=size)
        return (np.stack(self.memory.loc[indices, field]) for field in
                self.fields)


try:
    import tensorflow.compat.v2 as tf
    from tensorflow import keras
    from tensorflow import nn
    from tensorflow import optimizers
    from tensorflow import losses
    from tensorflow.keras import layers


    class PPOAgent:
        def __init__(self, env):
            self.action_n = env.action_space.n
            self.gamma = 0.99

            self.replayer = PPOReplayer()

            self.actor_net = self.build_net(hidden_sizes=[100,],
                    output_size=self.action_n, output_activation=nn.softmax,
                    learning_rate=0.001)
            self.critic_net = self.build_net(hidden_sizes=[100,],
                    learning_rate=0.002)

        def build_net(self, input_size=None, hidden_sizes=None, output_size=1,
                    activation=nn.relu, output_activation=None,
                    loss=losses.mse, learning_rate=0.001):
            model = keras.Sequential()
            for hidden_size in hidden_sizes:
                model.add(layers.Dense(units=hidden_size,
                        activation=activation))
            model.add(layers.Dense(units=output_size,
                    activation=output_activation))
            optimizer = optimizers.Adam(learning_rate)
            model.compile(optimizer=optimizer, loss=loss)
            return model

        def reset(self, mode=None):
            self.mode = mode
            if self.mode == 'train':
                self.trajectory = []

        def step(self, observation, reward, terminated):
            probs = self.actor_net.predict(observation[np.newaxis], verbose=0)[0]
            action = np.random.choice(self.action_n, p=probs)
            if self.mode == 'train':
                self.trajectory += [observation, reward, terminated, action]
            return action

        def close(self):
            if self.mode == 'train':
                self.save_trajectory_to_replayer()
                if len(self.replayer.memory) >= 1000:
                    for batch in range(5):  # learn multiple times
                        self.learn()
                    self.replayer = PPOReplayer()
                            # reset replayer after the agent changes itself

        def save_trajectory_to_replayer(self):
            df = pd.DataFrame(
                    np.array(self.trajectory, dtype=object).reshape(-1, 4),
                    columns=['state', 'reward', 'terminated', 'action'], dtype=object)
            states = np.stack(df['state'])
            df['v'] = self.critic_net.predict(states, verbose=0)
            pis = self.actor_net.predict(states, verbose=0)
            df['prob'] = [pi[action] for pi, action in zip(pis, df['action'])]
            df['next_v'] = df['v'].shift(-1).fillna(0.)
            df['u'] = df['reward'] + self.gamma * df['next_v']
            df['delta'] = df['u'] - df['v']
            df['advantage'] = signal.lfilter([1.,], [1., -self.gamma],
                    df['delta'][::-1])[::-1]
            df['return'] = signal.lfilter([1.,], [1., -self.gamma],
                    df['reward'][::-1])[::-1]
            self.replayer.store(df)

        def learn(self):
            states, actions, old_pis, advantages, returns = \
                    self.replayer.sample(size=64)
            state_tensor = tf.convert_to_tensor(states, dtype=tf.float32)
            action_tensor = tf.convert_to_tensor(actions, dtype=tf.int32)
            old_pi_tensor = tf.convert_to_tensor(old_pis, dtype=tf.float32)
            advantage_tensor = tf.convert_to_tensor(advantages, dtype=tf.float32)

            # update actor
            with tf.GradientTape() as tape:
                all_pi_tensor = self.actor_net(state_tensor)
                pi_tensor = tf.gather(all_pi_tensor, action_tensor, batch_dims=1)
                surrogate_advantage_tensor = (pi_tensor / old_pi_tensor) * \
                        advantage_tensor
                clip_times_advantage_tensor = 0.1 * surrogate_advantage_tensor
                max_surrogate_advantage_tensor = advantage_tensor + \
                        tf.where(advantage_tensor > 0.,
                        clip_times_advantage_tensor, -clip_times_advantage_tensor)
                clipped_surrogate_advantage_tensor = tf.minimum(
                        surrogate_advantage_tensor, max_surrogate_advantage_tensor)
                loss_tensor = -tf.reduce_mean(clipped_surrogate_advantage_tensor)
            actor_grads = tape.gradient(loss_tensor, self.actor_net.variables)
            self.actor_net.optimizer.apply_gradients(
                    zip(actor_grads, self.actor_net.variables))

            # update critic
            self.critic_net.fit(states, returns, verbose=0)
except:
    pass


try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.distributions as distributions

    class PPOAgent:
        def __init__(self, env):
            self.gamma = 0.99

            self.replayer = PPOReplayer()

            self.actor_net = self.build_net(
                    input_size=env.observation_space.shape[0],
                    hidden_sizes=[100,],
                    output_size=env.action_space.n, output_activator=nn.Softmax(1))
            self.actor_optimizer = optim.Adam(self.actor_net.parameters(), 0.001)
            self.critic_net = self.build_net(
                    input_size=env.observation_space.shape[0],
                    hidden_sizes=[100,])
            self.critic_optimizer = optim.Adam(self.critic_net.parameters(), 0.002)
            self.critic_loss = nn.MSELoss()

        def build_net(self, input_size, hidden_sizes, output_size=1,
                output_activator=None):
            layers = []
            for input_size, output_size in zip(
                    [input_size,] + hidden_sizes, hidden_sizes + [output_size,]):
                layers.append(nn.Linear(input_size, output_size))
                layers.append(nn.ReLU())
            layers = layers[:-1]
            if output_activator:
                layers.append(output_activator)
            net = nn.Sequential(*layers)
            return net

        def reset(self, mode=None):
            self.mode = mode
            if self.mode == 'train':
                self.trajectory = []

        def step(self, observation, reward, terminated):
            state_tensor = torch.as_tensor(observation, dtype=torch.float).unsqueeze(0)
            prob_tensor = self.actor_net(state_tensor)
            action_tensor = distributions.Categorical(prob_tensor).sample()
            action = action_tensor.numpy()[0]
            if self.mode == 'train':
                self.trajectory += [observation, reward, terminated, action]
            return action

        def close(self):
            if self.mode == 'train':
                self.save_trajectory_to_replayer()
                if len(self.replayer.memory) >= 1000:
                    for batch in range(5):  # learn multiple times
                        self.learn()
                    self.replayer = PPOReplayer()
                            # reset replayer after the agent changes itself

        def save_trajectory_to_replayer(self):
            df = pd.DataFrame(
                    np.array(self.trajectory, dtype=object).reshape(-1, 4),
                    columns=['state', 'reward', 'terminated', 'action'])
            state_tensor = torch.as_tensor(np.stack(df['state']), dtype=torch.float)
            action_tensor = torch.as_tensor(df['action'], dtype=torch.long)
            v_tensor = self.critic_net(state_tensor)
            df['v'] = v_tensor.detach().numpy()
            prob_tensor = self.actor_net(state_tensor)
            pi_tensor = prob_tensor.gather(-1, action_tensor.unsqueeze(1)).squeeze(1)
            df['prob'] = pi_tensor.detach().numpy()
            df['next_v'] = df['v'].shift(-1).fillna(0.)
            df['u'] = df['reward'] + self.gamma * df['next_v']
            df['delta'] = df['u'] - df['v']
            df['advantage'] = signal.lfilter([1.,], [1., -self.gamma],
                    df['delta'][::-1])[::-1]
            df['return'] = signal.lfilter([1.,], [1., -self.gamma],
                    df['reward'][::-1])[::-1]
            self.replayer.store(df)

        def learn(self):
            states, actions, old_pis, advantages, returns = \
                    self.replayer.sample(size=64)
            state_tensor = torch.as_tensor(states, dtype=torch.float)
            action_tensor = torch.as_tensor(actions, dtype=torch.long)
            old_pi_tensor = torch.as_tensor(old_pis, dtype=torch.float)
            advantage_tensor = torch.as_tensor(advantages, dtype=torch.float)
            return_tensor = torch.as_tensor(returns, dtype=torch.float).unsqueeze(1)

            # update actor
            all_pi_tensor = self.actor_net(state_tensor)
            pi_tensor = all_pi_tensor.gather(1, action_tensor.unsqueeze(1)).squeeze(1)
            surrogate_advantage_tensor = (pi_tensor / old_pi_tensor) * \
                    advantage_tensor
            clip_times_advantage_tensor = 0.1 * surrogate_advantage_tensor
            max_surrogate_advantage_tensor = advantage_tensor + \
                    torch.where(advantage_tensor > 0.,
                    clip_times_advantage_tensor, -clip_times_advantage_tensor)
            clipped_surrogate_advantage_tensor = torch.min(
                    surrogate_advantage_tensor, max_surrogate_advantage_tensor)
            actor_loss_tensor = -clipped_surrogate_advantage_tensor.mean()
            self.actor_optimizer.zero_grad()
            actor_loss_tensor.backward()
            self.actor_optimizer.step()

            # update critic
            pred_tensor = self.critic_net(state_tensor)
            critic_loss_tensor = self.critic_loss(pred_tensor, return_tensor)
            self.critic_optimizer.zero_grad()
            critic_loss_tensor.backward()
            self.critic_optimizer.step()
except:
    pass
