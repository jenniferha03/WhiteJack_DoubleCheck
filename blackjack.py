"""
Blackjack (a.k.a 21)
The player attempts to beat the dealer by getting a
hand value as close to 21 as possible, without going over 21.

Khue (Jennifer) Ha
"""
import random
import time
import cards

# Constants to identify winner of hand
TIE = 0
DEALER = 1
PLAYER = 2

# Dealer stands at 17
DEALER_MAX = 17

# The game max value for a hand
MAX = 21

# Player enters one of these two values when prompted.
HIT = 'h'
STAND = 's'


class BlackjackException(Exception):
    """Raise this exception when appropriate"""


def create_card_deck():
    """
    Creates a standard deck of cards.
    Each of the 4 suits has 13 cards.
    Use nested FOR loops to create the cards using cards.SUITS and cards.RANKS.
    (see cards.py)

    :return: a standard deck of 52 cards
    :rtype: list
    """
    card_deck = []

    for suit in cards.SUITS:
        for rank in cards.RANKS:
            card_deck.append(cards.Card(suit, rank))

    return card_deck


def get_hand_value(hand):
    """
    Computes the value of a hand using ``card.value``.
    If an Ace (worth 11 by default) is present and the total hand value
    exceeds the MAX, then count the Ace as 1 instead of 11.

    :param hand: the cards that are held by the player or dealer
    :type hand: list
    :return: the value of the hand
    :rtype: int
    """
    number_aces = 0
    hand_value_without_aces = 0
    for card in hand:
        if card.value != 11:
            hand_value_without_aces += card.value
        else:
            number_aces += 1

    hand_value = 0
    if number_aces == 0:
        hand_value = hand_value_without_aces
    elif number_aces > 0:
        if hand_value_without_aces < 11 - number_aces:
            hand_value = hand_value_without_aces + 10 + number_aces
        elif hand_value_without_aces == 11 - number_aces:
            hand_value = 21
        else:
            hand_value = hand_value_without_aces + number_aces

    return hand_value


def get_player_choice():
    """
    :return: the player's decision to hit or stand.
    :rtype: str
    """
    user_decision = input("Do you want to hit or stand? (h/s) ").lower()
    while user_decision not in (HIT, STAND):
        user_decision = input("Do you want to hit or stand? (h/s) ").lower()
    return user_decision


def deal_cards(deck: list, dealer_hand: list, player_hand: list):
    """
    Each player is dealt two cards. Player gets the first card.
    Alternate dealing between player and dealer until each has two cards.
    The dealers first card needs to be dealt face down.

    :param deck: the deck of cards to deal from
    :param dealer_hand: an empty list representing the dealer's hand
    :param player_hand: an empty list representing the player's hand
    :rtype: None
    """
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    cards.display_cards(player_hand)
    dealer_hand[1].face_down()


def dealer_turn(dealer_hand, deck, player_hand_value, delay=1):
    """
    Dealer receives cards if player has not busted.
    Dealer must stand at 17. Dealer must draw cards at 16 and under.
    Display the value of the hand display all the dealer's cards on
    after each card is dealt.

    :param dealer_hand: the cards held by the dealer
    :type dealer_hand: list
    :param deck: the deck of cards to deal from
    :type deck: list
    :param player_hand_value: the value of the player's hand
    :type player_hand_value: int
    :param delay: a delay for visual affect
    :type delay: int
    :return: the value of the dealer's hand
    :rtype: int
    """

    hand_value = get_hand_value(dealer_hand)
    print('Dealer:', hand_value)

    dealer_hand[1].face_up()
    cards.display_cards(dealer_hand)
    time.sleep(delay)

    while player_hand_value <= MAX and hand_value < DEALER_MAX:
        if len(deck) != 0:
            dealer_hand.append(deck.pop())
            hand_value = get_hand_value(dealer_hand)
            print('Dealer: ', hand_value)
            cards.display_cards(dealer_hand)
        else:
            break
    return hand_value


def player_turn(player_hand, deck):
    """
    Allow the player to draw a card (hit or stand).
    Return the value of the player's hand.

    :param player_hand: the cards held by the player
    :type player_hand: list
    :param deck: the deck of cards to deal from
    :type deck: list
    :return: the value of the players hand
    :rtype: int
    """
    hand_value = get_hand_value(player_hand)
    print('Player:', hand_value)
    cards.display_cards(player_hand)
    choice = None
    if hand_value < MAX:
        choice = get_player_choice()

    while choice == HIT:
        if len(deck) != 0:
            player_hand.append(deck.pop())
            hand_value = get_hand_value(player_hand)
            print('Player:', hand_value)
        else:
            break

        if hand_value <= MAX:
            cards.display_cards(player_hand)
            choice = get_player_choice()
        elif hand_value > MAX:
            cards.display_cards(player_hand)
            print('BUSTED!')
            break

    return hand_value


def determine_winner(dealer_hand_value, player_hand_value):
    """
    Returns the winner of the round based on hand value

    :param dealer_hand_value: dealer's hand value
    :type dealer_hand_value: int
    :param player_hand_value: player's hand value
    :type player_hand_value: int
    :return: either TIE, DEALER or PLAYER
    :rtype: int
    """
    winner = None
    if dealer_hand_value > MAX and player_hand_value > MAX:
        raise BlackjackException
    elif player_hand_value == MAX or dealer_hand_value > MAX:
        winner = PLAYER
    elif dealer_hand_value == MAX or player_hand_value > MAX:
        winner = DEALER
    elif player_hand_value == dealer_hand_value:
        winner = TIE
    elif dealer_hand_value < MAX and player_hand_value < MAX:
        if dealer_hand_value < player_hand_value:
            winner = PLAYER
        else:
            winner = DEALER
    return winner


def main():
    """ Controls the process of playing Blackjack """
    deck = create_card_deck()

    random.shuffle(deck)

    play_again = 'y'
    while play_again == 'y':
        # This list holds the cards that will be dealt to the dealer
        dealer_hand = []
        # This list holds the cards that will be dealt to the player
        player_hand = []
        try:
            # to the dealer and player
            deal_cards(deck, dealer_hand, player_hand)  # display the deal cards function

            print('Dealer: ??')
            cards.display_cards(dealer_hand)
            player_hand_value = get_hand_value(player_hand)
            dealer_hand_value = get_hand_value(dealer_hand)
            player_turn(player_hand, deck)
            dealer_turn(dealer_hand, deck, player_hand_value)
            player_hand_value = get_hand_value(player_hand)
            dealer_hand_value = get_hand_value(dealer_hand)
            winner = determine_winner(dealer_hand_value, player_hand_value)
            if winner == DEALER:
                print("Dealer wins!")
            elif winner == PLAYER:
                print("Player wins!")
            elif winner == TIE:
                print("Tie!")
            play_again = input('\nPlay again (y/n)? ')
            print()
        except IndexError:
            print('Deck is empty. Starting over!\n')
            input('Press any key to continue...')


if __name__ == '__main__':
    main()
