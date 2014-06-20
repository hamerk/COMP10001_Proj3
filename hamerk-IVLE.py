# Daifugo game
#
# 26/05/2014

card_rank = ['3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A', '2']


def swap_cards(hand, pid):
    sorted_hand = [[] for i in card_rank]
    cards_out = []
    count = 0
    while count in range(len(card_rank)):  # Sort cards
        for card in hand:
            if card[0] == card_rank[count]:
                sorted_hand[count].append(card)
        count += 1

    if pid == 0 or pid == 1:  # Select high card/s to swap
        cards_left = 1
        if pid == 0:
            cards_left = 2

        count = -1
        while cards_left > 0:  # While cards need to be swapped
            if count == -13:
                count = 0

            if 0 < len(sorted_hand[count]) <= cards_left:
                cards_out.append(sorted_hand[count][0])
                sorted_hand[count].pop(0)
                cards_left -= 1

            # If more cards at a value level than needed,
            # test if part of straight, and if so how long.
            elif len(sorted_hand[count]) > cards_left:
                straight_lengths = []
                for card in sorted_hand[count]:
                    suit = card[1]
                    straight_count = 1
                    psc = 0  # psc = Previous Straight Count
                    total_count = 0
                    length = []
                    while straight_count > psc:
                        psc = straight_count
                        for test_card in sorted_hand[count - straight_count]:
                            if test_card[1] == suit:
                                length.append(straight_count)
                                straight_count += 1

                    if length:
                        straight_lengths.append(max(length))
                    else:
                        straight_lengths.append(0)

                i = 0
                while i < len(straight_lengths):
                    if straight_lengths[i] == min(straight_lengths):
                        cards_out.append(sorted_hand[count][i])
                        sorted_hand[count].pop(i)
                        cards_left -= 1
                        break
                    else:
                        i += 1

            else:
                count -= 1
        return cards_out

    if pid == 2 or pid == 3:  # Select any card/s to swap
        cards_left = 1
        if pid == 3:
            cards_left = 2

        count = 0
        allowed_card_length = 1  # Max number of cards of same value
        do_not_use = []  # Cards part of straight
        straight_count = 1
        allowed_straight_length = 2  # Min straight length

        while cards_left > 0:
            if (count + straight_count) >= len(sorted_hand):
                allowed_card_length += 1
                straight_count = 1
                count = 0

            if allowed_card_length > 4:
                allowed_straight_length += 1
                allowed_card_length = 1
                do_not_use = []
                count = 0

            if allowed_straight_length > 13:
                cards_out.append(do_not_use[0])
                do_not_use.pop(0)
                cards_left -= 1

            if 0 < len(sorted_hand[count]) <= allowed_card_length:
                straight_lengths = []
                for card in sorted_hand[count]:
                    suit = card[1]
                    straight_count = 1
                    psc = 0
                    total_count = 0
                    length = []
                    while straight_count > psc and straight_count < 13:
                        psc = straight_count
                        for test_card in sorted_hand[count + straight_count]:
                            if test_card[1] == suit:
                                length.append(straight_count)
                                straight_count += 1

                    if length:
                        straight_lengths.append(max(length))
                    else:
                        straight_lengths.append(0)

                i = 0
                i_a = 0
                while i < len(straight_lengths):
                    if straight_lengths[i] >= allowed_straight_length:
                        while i_a in range(straight_lengths[i] + 1):
                            if (str(card_rank[count + i_a])
                               + suit) in do_not_use:
                                pass
                            else:
                                do_not_use.append(str(card_rank[count + i_a])
                                                  + suit)
                            i_a += 1

                        i += 1
                    else:
                        if sorted_hand[count][i] in do_not_use:
                            i += 1
                        else:
                            cards_out.append(sorted_hand[count][i])
                            sorted_hand[count].pop(i)
                            straight_lengths.pop(i)
                            cards_left -= 1
                            if cards_left == 0:  # Exit while loop if needed
                                return cards_out

                count += 1

            else:
                count += 1

    return cards_out


def generate_plays(hand):
    sorted_hand = [[] for i in card_rank]
    possible_plays = []
    count = 0
    while count in range(len(card_rank)):  # Sort cards
        for card in hand:
            if card[0] == card_rank[count]:
                sorted_hand[count].append(card)
        count += 1

    # Find all straights
    count = 0
    allowed_straight_length = 13
    while allowed_straight_length > 1:
        for card in sorted_hand[count]:
            suit = card[1]
            straight_lengths = []
            straight_count = 1
            psc = 0
            total_count = 0
            length = []
            while straight_count > psc and count + straight_count < 13:
                psc = straight_count
                for test_card in sorted_hand[count + straight_count]:
                    if test_card[1] == suit:
                        length.append(straight_count)
                        straight_count += 1
            if length:
                straight_lengths.append(max(length))
            else:
                straight_lengths.append(0)

            i = 0
            i_a = 0
            straight = []
            while i < len(straight_lengths):
                if straight_lengths[i] >= allowed_straight_length:
                    while i_a in range(allowed_straight_length + 1):
                        straight.append(str(card_rank[count + i_a]) + suit)
                        i_a += 1
                    possible_plays.append(straight)

                i += 1
        count += 1

        if count == 13:
            count = 0
            allowed_straight_length -= 1

    # Find 4 of a kind, then 3 of a kind etc.
    value_count = 4
    while value_count > 0:
        for value in sorted_hand:
            if len(value) == value_count:
                possible_plays.append(value)

            if len(value) > value_count:  # Variation of nCr code
                n = len(value)
                indices = range(value_count)
                possible_plays.append(list(value[i] for i in indices))
                while True:
                    for i in reversed(range(value_count)):
                        if indices[i] != i + n - value_count:
                            break
                    else:
                        break
                    indices[i] += 1
                    for j in range(i+1, value_count):
                        indices[j] = indices[j-1] + 1
                    possible_plays.append(list(value[i] for i in indices))
        value_count -= 1

    return possible_plays


def is_valid_play(play, rnd):
    if rnd == []:
        if play is None:
            return False
        else:
            return True

    if play is None:  # As long as rnd != [], None is always valid
        return True

    none_count = 0  # Number of Nones
    for prev_play in rnd:
        if prev_play is None:
            none_count += 1

    # Find last play that was not None
    count = 1
    while True:
        if rnd[-1 * count] is None:
            count += 1
        else:
            break

    # If cards in last play have same value 
    if rnd[-1 * count][0][0] == rnd[-1 * count][-1][0]:
        # Check Suit if 2 non-None singleton plays made
        if len(rnd) - none_count >= 2 and len(rnd[0]) == 1:
            i = 1
            while True:
                if rnd[i] is None:  # 2nd non-None play made
                    i += 1
                else:
                    if (rnd[0][0][1] == rnd[i][0][1] and
                       rnd[0][0][1] == play[0][1]):
                        break
                    elif rnd[0][0][1] != rnd[i][0][1]:
                        break
                    else:
                        return False

        if len(rnd[0]) != len(play):
            return False

        if play[0][0] != play[-1][0]:
            return False

        if (card_rank.index(play[-1][0]) >
           card_rank.index(rnd[-1 * count][-1][0])):
            return True
        else:
            return False

    else:  # Is straight
        # Sort so cards in order (low to high)
        p = []
        for card in play:
            p.append(card_rank.index(card[0]))

        p.sort()

        s_play = []
        for item in p:
            s_play.append(card_rank[item]+play[0][1])

        s_rnd = []
        for item in rnd:
            if item is None:
                s_rnd.append(None)
                continue
            else:
                r = []
                mini_list = []
                for card in item:
                    r.append(card_rank.index(card[0]))
                r.sort()
                for rank in r:
                    mini_list.append(card_rank[rank]+item[0][1])
                s_rnd.append(mini_list)

        if s_play[0][0] == s_play[-1][0]:  # If s_play is not straight
            return False
        else:
            if len(s_rnd) - none_count >= 2:  # Check Suit
                i = 1
                while True:
                    if s_rnd[i] is None:
                        i += 1
                    else:
                        if (s_rnd[0][0][1] == s_rnd[i][0][1] and
                           s_rnd[0][0][1] == s_play[0][1]):
                            break
                        elif s_rnd[0][0][1] != s_rnd[i][0][1]:
                            break
                        else:
                            return False

            # Play ranked higher than last play
            if card_rank.index(s_play[-1][0]) > card_rank.index(
               s_rnd[-1 * count][-1][0]):
                return True
            else:
                return False


def play(rnd, hand, discard, holding, generate=generate_plays,
         valid=is_valid_play):
    possible_plays = []
    straights = [[] for i in range(11)]
    oak = [[] for i in range(4)]  # Of a kind

    # Sort plays into order,
    # Long straights then Short straight then (4-1) of a kind,
    # Low card before high card
    for play in generate(hand):
        if play[0][0] != play[-1][0]:  # If straight
            suit = play[0][1]
            p = []
            for card in play:
                p.append([card_rank.index(card[0]), suit])

            p.sort()

            straights[(len(play) - 3)].append(p)

        else:  # Is x of a kind
            p = []
            for card in play:
                p.append([card_rank.index(card[0]), card[1]])
            oak[(len(play) - 1)].append(p)

    for rank in reversed(straights):
        rank.sort()
        for hand in rank:
            p = []
            for card in hand:
                    p.append(card_rank[card[0]] + card[1])
            possible_plays.append(p)

    for rank in reversed(oak):
        rank.sort()
        for hand in rank:
            p = []
            for card in hand:
                    p.append(card_rank[card[0]] + card[1])
            possible_plays.append(p)

    for play in possible_plays:
        if valid(play, rnd):
            return play

    return None
