from mancala import House, Store


def setup_pits(initial_seeds):
    n_pits = sum(map(len, initial_seeds))
    pits = [House(initial_seeds)]
    for _ in range(n_pits-1):
        pits.append(pits[-1].neighbor)
    return pits


def test_initialization():
    house1 = House([[4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0]])
    neighbor6 = house1.nth_neighbor(6)
    neighbor7 = house1.nth_neighbor(7)
    neighbor14 = house1.nth_neighbor(14)

    assert house1.seeds == 4, "First house should have 4 seeds."
    assert neighbor6.seeds == 0, "Sixth neighbor should have 0 seeds."
    assert isinstance(neighbor6, Store), "Sixth neighbor should be a store."
    assert house1.owner is neighbor6.owner, "First house and sixth neighbor should be owned by same player."
    assert neighbor7.seeds == 4, "Seventh neighbor should have 4 seeds."
    assert isinstance(neighbor7, House), "Seventh neighbor should be a house."
    assert house1.owner is not neighbor7.owner, "First house and seventh neighbor should not be owned by same player."
    assert neighbor14 is house1, "First house should be its own fourteenth neighbor."


def test_sow():
    pits = setup_pits([[3, 3, 3, 3, 9, 3, 0], [4, 4, 4, 4, 4, 4, 0]])
    h11, h12, h13, h14, h15, h16, s1, h21, h22, h23, h24, h25, h26, s2 = pits
    h15.sow()

    assert h15.seeds == 0, "House should have no seeds after sowing."
    assert h16.seeds == 4, "Sowing should leave a seed in next house."
    assert s1.seeds == 1, "Sowing may leave a seed in own store."
    assert h21.seeds == 5, "Sowing may leave a seed in opponent's house."
    assert s2.seeds == 0, "Seeds should not be sown in opponent's store."
    assert h11.seeds == 4, "Sowing should skip over opponent's store."
    assert h12.seeds == 3, "Sowing should end when all seeds from the sowing house are used"
    assert not h11.owner.has_turn, "Sowing should end player's turn."
    assert h11.owner.opponent.has_turn, "Sowing should pass turn to opponent."


def test_get_opposite():
    pits = setup_pits([[4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0]])
    h11, h12, h13, h14, h15, h16, s1, h21, h22, h23, h24, h25, h26, s2 = pits

    assert h11.get_opposite() is h26, "First house should be opposite to opponent's sixth house."
    assert h16.get_opposite() is h21, "Sixth house should be opposite to opponent's first house."
    assert h21.get_opposite() is h16, "Opponent's first house should be opposite to sixth house."


def test_capture():
    pits = setup_pits([[2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0]])
    h11, h12, h13, h14, h15, h16, s1, h21, h22, h23, h24, h25, h26, s2 = pits
    h11.sow()

    assert s1.seeds == 5, "Captured seeds should be moved to the capturing player's store."
    assert h13.seeds == 0, "Capturing house should be empty after capture."
    assert h24.seeds == 0, "Opposite house should be empty after capture."

    pits = setup_pits([[2, 0, 1, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0]])
    h11, h12, h13, h14, h15, h16, s1, h21, h22, h23, h24, h25, h26, s2 = pits
    h11.sow()

    assert s1.seeds == 0 and h13.seeds == 2 and h24.seeds == 4, \
        "Capture should not occur unless the last seed is sown in an empty house."

    pits = setup_pits([[2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
    h11, h12, h13, h14, h15, h16, s1, h21, h22, h23, h24, h25, h26, s2 = pits
    h11.sow()

    assert s1.seeds == 0 and h13.seeds == 1 and h24.seeds == 0, "Capture should not occur if opposite house is empty."
