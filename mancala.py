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

    def nth_neighbor(self, n):
        if n > 0:
            return self.neighbor.nth_neighbor(n-1)
        return self

    def take_and_pass(self, seeds):
        self.seeds += 1
        if seeds > 1:
            self.neighbor.pass_along(seeds-1)
        else:
            self.final_act()

    def pass_along(self, seeds):
        raise NotImplementedError("This method has not been implemented")

    def final_act(self):
        raise NotImplementedError("This method has not been implemented")


class House(Pit):

    DEFAULT_INITIAL_SEEDS = [[4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0]]

    def __init__(self, initial_seeds=None, owner=None, first_house=None):
        if initial_seeds is None:
            initial_seeds = self.DEFAULT_INITIAL_SEEDS
        if owner is None:
            owner = Player()
        if first_house is None:
            first_house = self

        seeds = initial_seeds[0].pop(0)
        if len(initial_seeds[0]) == 1:
            neighbor = Store(initial_seeds, owner, first_house)
        else:
            neighbor = House(initial_seeds, owner, first_house)
        super().__init__(seeds, owner, neighbor)

    def sow(self):
        seeds = self.seeds
        self.seeds = 0
        self.neighbor.pass_along(seeds)

    def pass_along(self, seeds):
        self.take_and_pass(seeds)

    def final_act(self):
        if self.seeds == 1:
            opposite_house = self.get_opposite()
            if opposite_house.seeds:
                self.capture_seeds(opposite_house)

        self.owner.end_turn()

    def get_opposite(self, store_distance=0):
        return self.neighbor.get_opposite(store_distance + 1)

    def move_to_store(self, seeds):
        self.neighbor.move_to_store(seeds)

    def capture_seeds(self, target):
        seeds = self.seeds+target.seeds
        target.seeds = 0
        self.seeds = 0
        self.move_to_store(seeds)


class Store(Pit):

    def __init__(self, initial_seeds, owner, first_house):
        seeds = initial_seeds[0].pop()
        initial_seeds.pop(0)
        if initial_seeds:
            neighbor = House(initial_seeds, owner.opponent, first_house)
        else:
            neighbor = first_house
        super().__init__(seeds, owner, neighbor)

    def pass_along(self, seeds):
        if self.owner.has_turn:
            self.take_and_pass(seeds)
        else:
            self.neighbor.take_and_pass(seeds)

    def final_act(self):
        pass

    def get_opposite(self, store_distance):
        return self.nth_neighbor(store_distance)

    def move_to_store(self, seeds):
        self.seeds += seeds
