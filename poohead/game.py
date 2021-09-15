import random
from typing import TypeVar, Optional, Union, NamedTuple


class Card(NamedTuple):
    number: int
    suit: str


Cards = list[Card]


def shuffled_deck() -> Cards:
    # clubs, spades, hearts, diamonds
    suits = 'CSHD'
    # 11 = jack, 12 = queen, 13 = king
    numbers = tuple(range(1, 14))
    cards = [Card(number, suit) for suit in suits for number in numbers]
    random.shuffle(cards)
    return cards


X = TypeVar('X')


def popn(lst: list[X], n: int) -> list[X]:
    result = []
    for _ in range(n):
        result.append(lst.pop())
    return result


# standard rules = ace is high
def gte(a: int, b: int) -> bool:
    if a == 1:
        return True
    return a >= b


PLAYABLE_ANYTIME = (2, 3, 10)
PILE_CLEARING_CARDS = (3, 10)


def valid_play(pile: Cards, played_cards: Cards) -> bool:
    if played_cards == []:
        return False
    # all cards in a move must match
    if len(set(card.number for card in played_cards)) > 1:
        return False
    if pile == []:
        return True
    played_number = played_cards[0].number
    if played_number in PLAYABLE_ANYTIME:
        return True
    topmost_card = pile[-1]
    if topmost_card.number == 7:
        return played_number in (4, 5, 6, 7)
    return gte(played_number, topmost_card.number)


class Game(object):
    def __init__(self, num_players: int = 2):
        self.deck = shuffled_deck()
        self.players = []
        for _ in range(num_players):
            self.players.append(
                Player(self, popn(self.deck, 3), popn(self.deck, 3), popn(self.deck, 3))
            )
        self.pile: Cards = []
        # NOTE: not necessary, but for sanity checking at the end of the game
        self.discard: Cards = []
        # index into self.players
        self.whose_turn = 0

    def get_pile(self) -> Cards:
        return self.pile

    def get_deck(self) -> Cards:
        return self.deck

    def draw_from_deck(self, n: int) -> Cards:
        return popn(self.deck, n)

    def is_over(self) -> bool:
        # TODO
        return False

    def discard_pile_if_necessary(self) -> None:
        if len(self.pile) > 0 and self.pile[-1].number in PILE_CLEARING_CARDS:
            if self.pile[-1].number == 3:
                # remove all the 3s from the top of the pile - cause 3s get discarded once played
                while len(self.pile) > 0 and self.pile[-1].number == 3:
                    self.discard.append(self.pile.pop())
                # rest of pile added to next player's hand
                next_player_index = (self.whose_turn + 1) % len(self.players)
                self.players[next_player_index].hand.extend(self.pile)
            else:
                self.discard.extend(self.pile)
            self.pile = []

    def tick(self):
        # detect whether the game is over
        # get turn from the current player
        # detect terminal conditions e.g. 4 of a kind on top of the pile, or a 10 or 3 was played
        # TODO: handle interrupts where any player can complete a set of 4 and sweep the pile
        # then, sometimes it's the same player's turn
        for i, player in enumerate(self.players):
            # NOTE: "whose_turn" is kind of a confusing global variable. consider passing it as a param into discard_pile_if_necessary, which is the only use site so far
            self.whose_turn = i
            played_cards = player.play_cards()
            self.pile.extend(played_cards)
            player.draw()
            self.discard_pile_if_necessary()


# TODO: how to handle the case of 3/7/10?
# i think each of those has to be a separate turn
TurnResult = Optional[Cards]


def valid_cards_this_turn(pile: Cards, cards_in_hand: Cards) -> Cards:
    return list(filter(lambda card: valid_play(pile, [card]), cards_in_hand))


class Player(object):
    def __init__(
        self, game: Game, hidden_cards: Cards, faceup_cards: Cards, hand: Cards
    ):
        self.game = game
        self.hidden_cards = hidden_cards
        self.faceup_cards = faceup_cards
        self.hand = hand

    def out_of_cards(self) -> bool:
        return self.hidden_cards == [] and self.faceup_cards == [] and self.hand == []

    def draw(self) -> None:
        if self.game.get_deck() == []:
            return
        if len(self.hand) >= 3:
            return
        self.hand.extend(self.game.draw_from_deck(3 - len(self.hand)))

    def play_cards(self) -> Cards:
        # i think we want to start with a decent default strategy (strategy-as-code)
        # eventually we can check for "self.strategy" (strategy-as-data)
        #
        # to start - randomly play any single valid card
        playable_cards = valid_cards_this_turn(self.game.pile, self.hand)
        if playable_cards == []:
            return []
        random_card = random.choice(playable_cards)
        self.hand.remove(random_card)
        return [random_card]
