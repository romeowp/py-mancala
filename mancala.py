class Player:

    def __init__(self, opponent=None):
        if opponent is None:
            self.has_turn = True
            self.opponent = Player(self)
        else:
            self.has_turn = False
            self.opponent = opponent

    def end_turn(self):
        self.has_turn = False
        self.opponent.has_turn = True


class Pit:

    def __init__(self, seeds, owner, neighbor):
        self.seeds = seeds
        self.owner = owner
        self.neighbor = neighbor

    def empty(self):
        self.seeds = 0

    def add(self):
        self.seeds += 1

    def nth_neighbor(self, n):
        if n > 0:
            return self.neighbor.nth_neighbor(n-1)
        return self

    def take_and_pass(self, seeds):
        self.add()
        if seeds > 1:
            self.neighbor.pass_along(seeds-1)
        else:
            self.final_act()

    def pass_along(self):
        raise NotImplementedError("This method has not been implemented")

    def final_act(self):
        raise NotImplementedError("This method has not been implemented")


class House(Pit):

    PITS_PER_PLAYER = 7
    DEFAULT_INITIAL_SEEDS = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    def __init__(self, initial_seeds=None, owner=None, first_house=None):
        if initial_seeds is None:
            initial_seeds = self.DEFAULT_INITIAL_SEEDS
            owner = Player()
            first_house = self
        if not initial_seeds:
            neighbor = first_house
        if len(initial_seeds)-1 % self.PITS_PER_PLAYER:
            neighbor = House()
        super().__init__(seeds, owner, neighbor)

    def initialize(self, initial_seeds=None, owner=None, first_house=None):
        if initial_seeds is None:
            initial_seeds = self.DEFAULT_INITIAL_SEEDS
            owner = Player()
            first_house = self
        if not initial_seeds:
            neighbor = first_house
        if len(initial_seeds)-1 % self.PITS_PER_PLAYER:
            neighbor = House()


        super().__init__(initial_seeds[0], owner)





    def pass_along(self):
        raise NotImplementedError("This method has not been implemented")

    def final_act(self):
        raise NotImplementedError("This method has not been implemented")
