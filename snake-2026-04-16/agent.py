import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque


class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.net(x)


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9

        self.memory = deque(maxlen=100_000)

        # ⚠️ FIXED
        self.model = DQN(12, 128, 4)

        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

    def get_action(self, state):
        self.epsilon = max(80 - self.n_games, 5)

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        return move

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short(self, state, action, reward, next_state, done):
        self._train_step(state, action, reward, next_state, done)

    def train_long(self):
        if len(self.memory) > 1000:
            batch = random.sample(self.memory, 1000)
        else:
            batch = self.memory

        states, actions, rewards, next_states, dones = zip(*batch)

        self._train_step(states, actions, rewards, next_states, dones)

    def _train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = action.unsqueeze(0)
            reward = reward.unsqueeze(0)
            done = (done,)

        pred = self.model(state)

        target = pred.clone()

        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][action[idx]] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()