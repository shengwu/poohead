from poohead import game


def test_valid_play_mismatched_played_cards():
    SOME_PILE = [game.Card(12, 'S')]
    assert not game.valid_play(SOME_PILE, [game.Card(5, 'H'), game.Card(6, 'H')])
    assert not game.valid_play(SOME_PILE, [game.Card(5, 'S'), game.Card(6, 'H')])


def test_valid_play_no_pile():
    assert game.valid_play([], [game.Card(5, 'H')])
    assert game.valid_play([], [game.Card(5, 'H'), game.Card(5, 'S')])


def test_valid_play_same_number():
    assert game.valid_play([game.Card(5, 'D')], [game.Card(5, 'H')])
    assert game.valid_play([game.Card(5, 'D')], [game.Card(5, 'H'), game.Card(5, 'S')])


def test_valid_play_higher_number():
    assert game.valid_play([game.Card(10, 'D')], [game.Card(11, 'H')])
    assert game.valid_play([game.Card(10, 'D')], [game.Card(12, 'H')])
    assert game.valid_play([game.Card(10, 'D')], [game.Card(13, 'H')])
    assert game.valid_play([game.Card(10, 'D')], [game.Card(1, 'H')])
    assert not game.valid_play([game.Card(10, 'D')], [game.Card(4, 'H')])


def test_valid_play_special_cards():
    assert game.valid_play([game.Card(5, 'D')], [game.Card(2, 'H')])
    assert game.valid_play([game.Card(5, 'D')], [game.Card(3, 'H')])
    assert game.valid_play([game.Card(5, 'D')], [game.Card(10, 'H')])


def test_valid_play_seven():
    assert game.valid_play([game.Card(7, 'D')], [game.Card(4, 'H')])
    assert game.valid_play([game.Card(7, 'D')], [game.Card(5, 'H')])
    assert game.valid_play([game.Card(7, 'D')], [game.Card(6, 'H')])
    assert game.valid_play([game.Card(7, 'D')], [game.Card(7, 'H')])
    assert not game.valid_play([game.Card(7, 'D')], [game.Card(11, 'H')])
    assert not game.valid_play([game.Card(7, 'D')], [game.Card(1, 'H')])

    assert game.valid_play([game.Card(7, 'D')], [game.Card(2, 'H')])
    assert game.valid_play([game.Card(7, 'D')], [game.Card(3, 'H')])
    assert game.valid_play([game.Card(7, 'D')], [game.Card(10, 'H')])
