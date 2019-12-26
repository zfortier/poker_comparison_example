from collections import Counter, namedtuple

SUITS = ['d', 'h', 's', 'c']
RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
Card = namedtuple('card', ['suit', 'rank'])

class Hand:
    def __init__(self, hand):
        self.hand = hand
        self.catg = None
        self.high_cards = None
        self.hand.sort(key=(lambda c: c.rank), reverse=True)
        self.rank_list = [c.rank for c in self.hand]
        self.rank_freq = list(Counter(card.rank for card in self.hand).values())
        self.suit_freq = list(Counter(card.suit for card in self.hand).values())
        self.rank_freq.sort()
        self.suit_freq.sort()
        self._classify_hand()

    def __eq__(self, x_hand):
        return self._comp_hand(x_hand) == 'EQ'

    def __lt__(self, x_hand):
        return self._comp_hand(x_hand) == 'LT'

    def __gt__(self, x_hand):
        return self._comp_hand(x_hand) == 'GT'

    def __repr__(self):
        hand_ranks = self.rank_list.copy()
        face_cards = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        for idx, val in enumerate(hand_ranks):
            if val in face_cards:
                hand_ranks[idx] = face_cards[val]
        repr_str = (str(hand_ranks[0]) + self.hand[0].suit + ' '
                    + str(hand_ranks[1]) + self.hand[1].suit + ' '
                    + str(hand_ranks[2]) + self.hand[2].suit + ' '
                    + str(hand_ranks[3]) + self.hand[3].suit + ' '
                    + str(hand_ranks[4]) + self.hand[4].suit)
        return repr_str

    def _classify_hand(self):
        # Setting `self.high_cards` takes advantage of the hand being pre-sorted
        if self._is_straight_flush():
            self.catg = 'SF'
            self.high_cards = self.rank_list
        elif self._is_four_of_a_kind():
            self.catg = '4K'
            self.high_cards = [self.hand[2].rank,
                               (self.hand[0].rank
                                if self.hand[0].rank != self.hand[2].rank
                                else self.hand[4].rank)]
        elif self._is_full_house():
            self.catg = 'FH'
            self.high_cards = [self.hand[2].rank,
                               (self.hand[3].rank
                                if self.hand[3].rank != self.hand[2].rank
                                else self.hand[1].rank)]
        elif self._is_flush():
            self.catg = 'F'
            self.high_cards = self.rank_list
        elif self._is_straight():
            self.catg = 'S'
            self.high_cards = self.rank_list
        elif self._is_three_of_a_kind():
            self.catg = '3K'
            self.high_cards = [self.hand[4].rank, self.hand[0].rank]
            self.high_cards.append(self.hand[3].rank
                                   if self.hand[1].rank in self.high_cards
                                   else self.hand[1].rank)
        elif self._is_two_pair():
            self.catg = '2K2'
            self.high_cards = [self.hand[0].rank,
                               self.hand[2].rank,
                               self.hand[4].rank]
        elif self._is_one_pair():
            self.catg = '2K'
            self.high_cards = list(set(self.rank_list))
        else:
            self.catg = None
            self.high_cards = self.rank_list

    def _is_straight_flush(self):
        return self._is_straight() and self._is_flush()

    def _is_flush(self):
        return self.suit_freq[0] == 5

    def _is_straight(self):
        # Note: The second OR'ed condition allows for low aces
        return ((False not in [(self.hand[n].rank == self.hand[n+1].rank - 1)
                               for n in (0, 1, 2, 3)])
                or (self.rank_list == [2, 3, 4, 5, 14]))

    def _is_four_of_a_kind(self):
        return self.rank_freq[1] == 4

    def _is_full_house(self):
        return self.rank_freq[1] == 3

    def _is_two_pair(self):
        return self.rank_freq[2] == 2

    def _is_three_of_a_kind(self):
        return self.rank_freq[2] == 3

    def _is_one_pair(self):
        return self.rank_freq[3] == 2 and self.rank_freq[2] == 1

    def _comp_hand(self, comp_hand):
        ret_val = 'EQ'
        catg_order = ['SF', '4K', 'FH', 'F', 'S', '3K', '2K2', '2K', None]
        if catg_order.index(self.catg) > catg_order.index(comp_hand.catg):
            ret_val = 'GT'
        elif catg_order.index(self.catg) < catg_order.index(comp_hand.catg):
            ret_val = 'LT'
        else:
            for k in range(0, len(self.hand)):
                if self.hand[k].rank == comp_hand[k].rank:
                    continue
                elif self.hand[k].rank > self.hand[k].rank:
                    ret_val = 'GT'
                    break
                else:
                    ret_val = 'LT'
                    break
        return ret_val
