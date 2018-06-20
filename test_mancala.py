from mancala import House, Store


def test_setup():
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
    house1 = House([[0, 0, 0, 0, 9, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
    house5 = house1.nth_neighbor(4)
    house6 = house5.neighbor
    store1 = house6.neighbor
    house7 = store1.neighbor
    store2 = house7.nth_neighbor(6)
    house5.sow()

    assert house5.seeds == 0, "House should have no seeds after sowing."
    assert house6.seeds == 1, "Sowing should leave a seed in next house."
    assert store1.seeds == 1, "Sowing should leave a seed in own store."
    assert house7.seeds == 1, "Sowing should leave a seed in opponent's house."
    assert store2.seeds == 0, "Seeds should not be sown in opponent's store."
    assert house1.seeds == 1, "Sowing should skip over opponent's store."
    assert not house1.owner.has_turn, "Sowing should end player's turn."
    assert house1.owner.opponent.has_turn, "Sowing should pass turn to opponent."


def test_get_opposing():
    house1 = House([[4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0]])
    house6 = house1.nth_neighbor(5)
    house7 = house6.nth_neighbor(2)
    house12 = house7.nth_neighbor(5)

    assert house1.get_opposing() is house12, "The first house should be opposed by the twelfth house."
    assert house6.get_opposing() is house7, "The sixth house should be opposed by the seventh house."
    assert house7.get_opposing() is house6, "The seventh house should be opposed by the sixth house."




# def test_capture():
#     house1 = House([[2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0]])
#     house3 = house1.nth_neighbor(2)
#     store1 = house3.nth_neighbor(4)
#     house10 = house3.nth_neighbor(4)
#     house1.sow()
#
#     assert store1.seeds == 5
#     assert house3.seeds == 0
#     assert house10.seeds == 0
