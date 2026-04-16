from env import SnakeEnv, UP, DOWN, LEFT, RIGHT
from agent import Agent
import torch


def get_direction(action):
    if action == 0:
        return UP
    elif action == 1:
        return DOWN
    elif action == 2:
        return LEFT
    elif action == 3:
        return RIGHT


def train():
    agent = Agent()
    env = SnakeEnv()
    lawan = SnakeEnv()
    record = 0

    while True:
        state_old = env.get_state(lawan)

        action = agent.get_action(state_old)

        direction = get_direction(action)

        state_new, reward, done = env.step(direction, lawan)

        agent.train_short(state_old, action, reward, state_new, done)
        agent.remember(state_old, action, reward, state_new, done)

        if done:
            score = env.score

            env.reset()
            lawan.reset()
            agent.n_games += 1

            agent.train_long()

            if score >= record:
                record = score
                torch.save(agent.model.state_dict(), "model.pth")

            print(f"Game {agent.n_games} | Score: {score} | Record: {record}")


if __name__ == "__main__":
    train()