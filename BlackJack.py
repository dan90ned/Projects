"""This is a Black Jack game. Player and Computer has 500 credit each.
The game will not end by itself whe the credit is 0 for one of them
Have fun!"""

import random
import sys
import os
import time

# create a deck dictionary with key and values
deck = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# real deck list
deck_list = 4 * [i for i in deck.keys()]


# the deck
class Deck:
    def __init__(self):
        self.deck = deck_list

    # print the deck. used just to verify
    def __str__(self):
        return str(self.deck)

    # make iterable Deck
    def __iter__(self):
        return iter(self.deck)

    # cards shuffling
    def shuffle_deck(self):
        random.shuffle(self.deck)
        return list(self.deck)


a = Deck()
used_deck = a.shuffle_deck()  # the shuffled deck used in game


class Player:  # used to define players
    def __init__(self, name, balance):
        self.hand = []
        self.name = name
        self.balance = balance

    def __str__(self):  # can print name
        return str(self.hand)

    def __iter__(self):  # make iterable
        return iter(self.hand)

    def __contains__(self, item):  # check if contains ... X
        self.item = item

    def __len__(self):  # length
        return len(self.hand)

    def f_deal(self):  # first deal
        for i in range(1, 3):
            i_card = random.choice(used_deck)
            self.hand.append(i_card)
            used_deck.remove(i_card)

    def next_deal(self):  # the others deals
        i_card = random.choice(used_deck)
        self.hand.append(i_card)
        used_deck.remove(i_card)

    def clear_cards(self):  # clear cards at the end
        self.hand = []

    def loose(self, b_amount):  # loose money func
        self.balance -= b_amount

    def gain(self, g_amount):  # win money func
        self.balance += g_amount


def check_bj(hand):  # check BJ
    sum_hand = sum(deck[i] for i in hand)

    if sum_hand == 21:
        output_handle(f'Black Jack! {hand.name} wins!')
        play = False
    else:
        play = True
    return sum_hand, play


def check_cards(hand, play):  # check total cards
    if 'A' in list(hand):
        if check_a(hand)[1] > 21:
            play = False

        elif check_a(hand)[1] <= 21:
            if check_a(hand)[0] == 1:
                play = True

            if check_a(hand)[0] == 2:
                play = True

    elif check_under21(hand):
        play = True

    elif check_over21(hand):
        play = False

    return play, check_a(hand)[1], check_a(hand)[2], check_under21(hand)[1], check_under21(hand)[1]


def check_a(hand):  # check if player has A in hand
    case = 0
    sum_hand_small = 0
    sum_hand = sum(deck[i] for i in hand)

    if check_over21(hand)[0]:
        for i in range(len(hand)):
            if sum_hand > 21:
                if list(hand)[i] == 'A':
                    sum_hand -= 10
        sum_hand_small = sum_hand - 10
        case = 1  # case -A sum<21

    elif check_under21(hand)[0]:
        sum_hand_small = sum_hand - 10
        case = 2

    return case, sum_hand, sum_hand_small


def check_under21(hand):
    sum_hand = sum(deck[i] for i in hand)
    if sum_hand < 21:
        return True, sum_hand
    else:
        return False, sum_hand


def check_over21(hand):
    sum_hand = sum(deck[i] for i in hand)
    if sum_hand > 21:
        return True, sum_hand
    else:
        return False, sum_hand


def print_sum_cards(hand):  # print sum card w or w/o A in hand
    try:
        if check_a(hand)[0] == 2 and 'A' in list(hand):
            output_handle(f'{hand.name} Total: {check_cards(hand, True)[1]} / {check_cards(hand, True)[2]}')
        else:
            output_handle(f'{hand.name} Total: {check_cards(hand, True)[1]}')
    except ValueError:
        output_handle(f'{hand.name} Total: {check_cards(hand, True)[1]}')


def check_winner(player_hand, pc_hand):  # check the winner (to be payed later)
    global winner
    if check_cards(player_hand, True)[1] > check_cards(pc_hand, True)[1]:
        winner = 1
        output_handle(f'{player_hand.name} wins!')
    elif check_cards(player_hand, True)[1] < check_cards(pc_hand, True)[1]:
        output_handle(f'{pc_hand.name} wins!')
        winner = 2
    elif check_cards(player_hand, True)[1] == check_cards(pc_hand, True)[1]:
        output_handle('Deuce!')


def hit_stand_in():  # check if player wants to hit or to stand
    while True:
        try:
            choose = input_handle('Please choose: Hit(H) or Stand(S): ').strip().upper()
            if choose == 'H':
                player1.next_deal()
                player_hit = True
                break

            elif choose == 'S':
                player_hit = False
                break

        except TypeError:
            pass

    return player_hit


def check_total(hand):  # check cards total and return cases of game
    case = 0
    sum_hand = sum(deck[i] for i in hand)
    if check_under21(hand)[0]:
        case = 1
    elif check_over21(hand)[0] and 'A' in list(hand) and sum_hand - 10 * (list(hand).count('A')) < 21:
        case = 1

    elif sum_hand == 21 or sum_hand - 10 * (list(hand).count('A')) == 21:
        case = 3

    elif check_over21(hand)[0]:
        case = 2
    return case


def check_play_again():  # check if player want to play again
    while True:
        try:
            choose = input_handle('Do you want to play again? (Y/N): ').strip().upper()
            if choose == 'Y':
                play_again = True
                break

            elif choose == 'N':
                play_again = False
                break

        except TypeError:
            pass

    return play_again


bet_amount = 0


def bet(balance):  # bet func
    global bet_amount
    while True:
        try:
            bet_amount = int(input_handle('Please place your bet: ').strip().upper())

            if balance >= bet_amount > 0:
                return bet_amount
            else:
                bet(balance)
            break
        except ValueError:
            pass
    return bet_amount


def pay_winner():  # pay winner func after the game is end
    if winner == 1:
        player1.gain(bet_amount)
        pc.loose(bet_amount)
    elif winner == 2:
        pc.gain(bet_amount)
        player1.loose(bet_amount)


def output_handle(printed_arg):
    sys.stdout.write(printed_arg + '\n')


def input_handle(prompt):
    sys.stdout.write(prompt + '\n')
    return sys.stdin.readline()


def print_first_hand():
    return f'{player1.name} cards:   {player1} \n' \
           f'{pc.name} cards: [ {list(pc)[0]},   --] \n' \
           '\n'


def print_credit():  # print credit func
    return '\n' \
           '$$$$$$$$$$$$$$$$$$$$$ \n' \
           f'{player1.name} credit: {player1.balance} \n' \
           f'{pc.name} credit: {pc.balance} \n' \
           '$$$$$$$$$$$$$$$$$$$$$ \n' \
           '\n'


def clear_screen():
    os.system('cls')


if __name__ == '__main__':
    with open('cfg.txt') as f:
        d = {}
        for line in f:
            k, v = line.split(':')
            d[k] = int(v)
    k_list = [k for k in d]

    # set players
    player1 = Player(k_list[0], d[k_list[0]])
    pc = Player(k_list[1], d[k_list[1]])

    # execution

    while True:  # game loop (play again func)
        if len(used_deck) >= 10:  # shuffle deck if card are less then 10
            pass
        else:
            used_deck = a.shuffle_deck()

        # game start
        winner = 0
        clear_screen()
        output_handle(print_credit())
        bet(player1.balance)

        player1.f_deal()  # deal cards
        pc.f_deal()

        output_handle(print_first_hand())

        # start check player cards
        if len(player1) == 2:
            if check_bj(player1)[1]:
                pass
            else:
                winner = 1

        print_sum_cards(player1)

        while check_total(player1) == 1:  # loop for hit/stand
            if hit_stand_in():

                output_handle(f'---------------------- \n'
                              f'{player1.name} cards:   {player1}\n'
                              f'{pc.name} cards: [ {list(pc)[0]},   --]\n')

                print_sum_cards(player1)

                if check_total(player1) == 1:
                    pass

                elif check_total(player1) == 2:
                    winner = 2
                    output_handle('Bust! You lost!')
                    break

                elif check_total(player1) == 3:
                    break
            else:
                break

        if check_total(player1) in (1, 3) and check_bj(player1)[1]:  # computer loop
            output_handle(f'----------------------\n'
                          f'{pc.name} cards: {pc}\n')
            check_bj(pc)
            print_sum_cards(pc)
            while check_a(pc)[1] < 17:
                output_handle('----------------------')
                time.sleep(2)
                pc.next_deal()
                output_handle(f'{pc.name} cards: {pc}')

                print_sum_cards(pc)

            else:
                if check_a(pc)[1] > 21:
                    winner = 1
                    output_handle(f'{pc.name} Bust! \n'
                                  f'{player1.name} wins!')
                else:
                    print_sum_cards(player1)
                    check_winner(player1, pc)

        pay_winner()

        output_handle(print_credit())

        if check_play_again():
            clear_screen()
            player1.clear_cards()
            pc.clear_cards()
        else:
            break
