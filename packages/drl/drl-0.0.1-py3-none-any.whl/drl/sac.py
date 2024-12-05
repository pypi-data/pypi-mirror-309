import numpy as np
import scipy.special
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

    class SACAgent:
        def __init__(self, env):
            self.action_n = env.action_space.n
            self.gamma = 0.99

            self.replayer = DQNReplayer(100000)

            self.alpha = 0.02

            # create actor
            def sac_loss(y_true, y_pred):
                """ y_true is Q(*, action_n), y_pred is pi(*, action_n) """
                qs = self.alpha * tf.math.xlogy(y_pred, y_pred) - y_pred * y_true
                return tf.reduce_sum(qs, axis=-1)
            self.actor_net = self.build_net(
                    hidden_sizes=[256, 256],
                    output_size=self.action_n, output_activation=nn.softmax,
                    loss=sac_loss)

            # create Q critic
            self.q0_net = self.build_net(
                    hidden_sizes=[256, 256],
                    output_size=self.action_n)
            self.q1_net = self.build_net(
                    hidden_sizes=[256, 256],
                    output_size=self.action_n)

            # create V critic
            self.v_evaluate_net = self.build_net(
                    hidden_sizes=[256, 256])
            self.v_target_net = models.clone_model(self.v_evaluate_net)

        def build_net(self, hidden_sizes, output_size=1,
                    activation=nn.relu, output_activation=None,
                    loss=losses.mse, learning_rate=0.0003):
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
                if len(self.trajectory) >= 8:
                    state, _, _, action, next_state, reward, terminated, _ = \
                            self.trajectory[-8:]
                    self.replayer.store(state, action, reward, next_state, terminated)
                if self.replayer.count >= 500:
                    self.learn()
            return action

        def close(self):
            pass

        def update_net(self, target_net, evaluate_net, learning_rate=0.005):
            average_weights = [(1. - learning_rate) * t + learning_rate * e for t, e
                    in zip(target_net.get_weights(), evaluate_net.get_weights())]
            target_net.set_weights(average_weights)

        def learn(self):
            states, actions, rewards, next_states, terminateds = \
                    self.replayer.sample(128)

            # update actor
            q0s = self.q0_net.predict(states, verbose=0)
            q1s = self.q1_net.predict(states, verbose=0)
            self.actor_net.fit(states, q0s, verbose=0)

            # update V critic
            q01s = np.minimum(q0s, q1s)
            pis = self.actor_net.predict(states, verbose=0)
            entropic_q01s = pis * q01s - self.alpha * \
                    scipy.special.xlogy(pis, pis)
            v_targets = entropic_q01s.sum(axis=-1)
            self.v_evaluate_net.fit(states, v_targets, verbose=0)

            # update Q critic
            next_vs = self.v_target_net.predict(next_states, verbose=0)
            q_targets = rewards[:, np.newaxis] + \
                    self.gamma * (1. - terminateds[:, np.newaxis]) * next_vs
            np.put_along_axis(q0s, actions.reshape(-1, 1), q_targets, -1)
            np.put_along_axis(q1s, actions.reshape(-1, 1), q_targets, -1)
            self.q0_net.fit(states, q0s, verbose=0)
            self.q1_net.fit(states, q1s, verbose=0)

            # update v network
            self.update_net(self.v_target_net, self.v_evaluate_net)
except:
    pass


try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.distributions as distributions


    class SACAgent:
        def __init__(self, env):
            state_dim = env.observation_space.shape[0]
            self.action_n = env.action_space.n
            self.gamma = 0.99
            self.replayer = DQNReplayer(10000)

            self.alpha = 0.02

            # create actor
            self.actor_net = self.build_net(input_size=state_dim,
                    hidden_sizes=[256, 256],
                    output_size=self.action_n, output_activator=nn.Softmax(-1))
            self.actor_optimizer = optim.Adam(self.actor_net.parameters(), lr=3e-4)

            # create V critic
            self.v_evaluate_net = self.build_net(input_size=state_dim,
                    hidden_sizes=[256, 256])
            self.v_target_net = copy.deepcopy(self.v_evaluate_net)
            self.v_optimizer = optim.Adam(self.v_evaluate_net.parameters(), lr=3e-4)
            self.v_loss = nn.MSELoss()

            # create Q critic
            self.q0_net = self.build_net(input_size=state_dim,
                    hidden_sizes=[256, 256], output_size=self.action_n)
            self.q1_net = self.build_net(input_size=state_dim,
                    hidden_sizes=[256, 256], output_size=self.action_n)
            self.q0_loss = nn.MSELoss()
            self.q1_loss = nn.MSELoss()
            self.q0_optimizer = optim.Adam(self.q0_net.parameters(), lr=3e-4)
            self.q1_optimizer = optim.Adam(self.q1_net.parameters(), lr=3e-4)

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
                if len(self.trajectory) >= 8:
                    state, _, _, action, next_state, reward, terminated, _ = \
                            self.trajectory[-8:]
                    self.replayer.store(state, action, reward, next_state, terminated)
                if self.replayer.count >= 500:
                    self.learn()
            return action

        def close(self):
            pass

        def update_net(self, target_net, evaluate_net, learning_rate=0.0025):
            for target_param, evaluate_param in zip(
                    target_net.parameters(), evaluate_net.parameters()):
                target_param.data.copy_(learning_rate * evaluate_param.data
                        + (1 - learning_rate) * target_param.data)

        def learn(self):
            states, actions, rewards, next_states, terminateds = \
                    self.replayer.sample(128)
            state_tensor = torch.as_tensor(states, dtype=torch.float)
            action_tensor = torch.as_tensor(actions, dtype=torch.long)
            reward_tensor = torch.as_tensor(rewards, dtype=torch.float)
            next_state_tensor = torch.as_tensor(next_states, dtype=torch.float)
            terminated_tensor = torch.as_tensor(terminateds, dtype=torch.float)

            # update Q critic
            next_v_tensor = self.v_target_net(next_state_tensor)
            q_target_tensor = reward_tensor.unsqueeze(1) + self.gamma * \
                    (1. - terminated_tensor.unsqueeze(1)) * next_v_tensor

            all_q0_pred_tensor = self.q0_net(state_tensor)
            q0_pred_tensor = torch.gather(all_q0_pred_tensor, 1,
                    action_tensor.unsqueeze(1))
            q0_loss_tensor = self.q0_loss(q0_pred_tensor, q_target_tensor.detach())
            self.q0_optimizer.zero_grad()
            q0_loss_tensor.backward()
            self.q0_optimizer.step()

            all_q1_pred_tensor = self.q1_net(state_tensor)
            q1_pred_tensor = torch.gather(all_q1_pred_tensor, 1,
                    action_tensor.unsqueeze(1))
            q1_loss_tensor = self.q1_loss(q1_pred_tensor, q_target_tensor.detach())
            self.q1_optimizer.zero_grad()
            q1_loss_tensor.backward()
            self.q1_optimizer.step()

            # update V critic
            q0_tensor = self.q0_net(state_tensor)
            q1_tensor = self.q1_net(state_tensor)
            q01_tensor = torch.min(q0_tensor, q1_tensor)
            prob_tensor = self.actor_net(state_tensor)
            ln_prob_tensor = torch.log(prob_tensor.clamp(1e-6, 1.))
            entropic_q01_tensor = prob_tensor * (q01_tensor -
                    self.alpha * ln_prob_tensor)
            # OR entropic_q01_tensor = prob_tensor * (q01_tensor - \
            #         self.alpha * torch.xlogy(prob_tensor, prob_tensor)
            v_target_tensor = torch.sum(entropic_q01_tensor, dim=-1, keepdim=True)
            v_pred_tensor = self.v_evaluate_net(state_tensor)
            v_loss_tensor = self.v_loss(v_pred_tensor, v_target_tensor.detach())
            self.v_optimizer.zero_grad()
            v_loss_tensor.backward()
            self.v_optimizer.step()

            self.update_net(self.v_target_net, self.v_evaluate_net)

            # update actor
            prob_q_tensor = prob_tensor * (self.alpha * ln_prob_tensor - q0_tensor)
            actor_loss_tensor = prob_q_tensor.sum(axis=-1).mean()
            self.actor_optimizer.zero_grad()
            actor_loss_tensor.backward()
            self.actor_optimizer.step()
except:
    pass
