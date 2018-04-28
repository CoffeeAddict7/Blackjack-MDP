from blackjackEnv import BlackjackEnv
import random


def policy_with_caution(state, env):
    hand_limit = env.hand_limit
    max_card = env.cards
    valueCardsInHand = state["valueCardsInHand"]
    nextCardIndex = state["nextCardIndex"]
    deckCardsCount = state["deckCardsCount"]
    if (nextCardIndex != max_card):  # there is a peeked card
        if (valueCardsInHand + nextCardIndex+1) <= hand_limit:
            # the peeked card + valueCardsInHand is less or equal than the limit
            action = 0
        else:
            # the peeked card + valueCardsInHand is bigger than the limit, better quit
            action = 2
    elif valueCardsInHand + max_card < hand_limit:
        # if the bigger card of the game is drawn, it is still under the limit so there is no need to check
        action = 0
    else:
        # the next card may cause valueCardsInHand to be over the limit, better check
        action = 1

    return action


def policy_always_take(state, env):
    return 0


def policy_random(state, env):
    return random.choice([0, 1, 2])


def policy_runner(strategy, env, render=False):
    done = False
    state = env.reset()
    reward = 0
    while (not(done)):
        if (render):
            env.render()
        action = strategy(state, env)
        state, new_reward, done, _ = env.step(action)
        reward += new_reward

    return reward


def main():
    for strategy in [
        # add your policies here
        policy_random,
        policy_with_caution,
        policy_always_take
    ]:
        reward_sum = 0
        for i in range(10):
            env = BlackjackEnv()
            env.seed(i)
            reward = policy_runner(strategy, env)
            print(reward, strategy.__name__)
            reward_sum += reward
        print("Total", reward_sum, strategy.__name__)
        print()


if __name__ == "__main__":
    # execute only if run as a script
    main()