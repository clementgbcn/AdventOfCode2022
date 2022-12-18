from Day import Day


class Rock:
    def __init__(self, ite, sx, sy):
        self.shape = ite % 5
        if ite % 5 == 0:
            self.pos = [(sx + i, sy) for i in range(4)]
            self.left = sx
            self.right = sx + 3
            self.up = sy
        elif ite % 5 == 1:
            self.pos = [(sx + 1, sy), (sx + 1, sy + 2)]
            self.pos += [(sx + i, sy + 1) for i in range(3)]
            self.left = sx
            self.right = sx + 2
            self.up = sy + 2
        elif ite % 5 == 2:
            self.pos = [(sx + i, sy) for i in range(3)]
            self.pos += [(sx + 2, sy + i) for i in range(1, 3)]
            self.left = sx
            self.right = sx + 2
            self.up = sy + 2
        elif ite % 5 == 3:
            self.pos = [(sx, sy + i) for i in range(4)]
            self.left = sx
            self.right = sx
            self.up = sy + 3
        elif ite % 5 == 4:
            self.pos = [(sx, sy + i) for i in range(2)]
            self.pos += [(sx + 1, sy + i) for i in range(2)]
            self.left = sx
            self.right = sx + 1
            self.up = sy + 1

    def move(self, direction, current_pos, current_min, nb_fall):
        if nb_fall < 3:
            if direction == "<" and self.left > 0:
                self.pos = list(map(lambda x: (x[0] - 1, x[1]), self.pos))
                self.left -= 1
                self.right -= 1
            if direction == ">" and self.right < 6:
                self.pos = list(map(lambda x: (x[0] + 1, x[1]), self.pos))
                self.left += 1
                self.right += 1
            # Going down
            self.pos = list(map(lambda x: (x[0], x[1] - 1), self.pos))
            self.up -= 1
            return True
        else:
            if direction == "<" and self.left > 0:
                new_pos = list(map(lambda x: (x[0] - 1, x[1]), self.pos))
                if all(
                    map(lambda x: x[0] not in current_pos.get(x[1], set()), new_pos)
                ):
                    self.pos = new_pos
                    self.left -= 1
                    self.right -= 1
            if direction == ">" and self.right < 6:
                new_pos = list(map(lambda x: (x[0] + 1, x[1]), self.pos))
                if all(
                    map(lambda x: x[0] not in current_pos.get(x[1], set()), new_pos)
                ):
                    self.pos = new_pos
                    self.left += 1
                    self.right += 1
            # Going down
            new_pos = list(map(lambda x: (x[0], x[1] - 1), self.pos))
            if all(
                map(
                    lambda x: x[0] not in current_pos.get(x[1], set())
                    and x[1] > current_min,
                    new_pos,
                )
            ):
                self.pos = new_pos
                self.up -= 1
                return True
            return False


class Chamber:
    def __init__(self, hot_airs):
        self.rocks = {}
        self.current_max = -1
        self.current_min = -1
        self.directions = next(hot_airs)
        self.nb_flux = len(self.directions[:])

    def fall_old(self, maxi):
        ite = 0
        ite_flux = 0
        while ite < maxi:
            rock = Rock(ite, 2, self.current_max + 4)
            nb_fall = 0
            while rock.move(
                self.directions[ite_flux % self.nb_flux],
                self.rocks,
                self.current_min,
                nb_fall,
            ):
                ite_flux += 1
                nb_fall += 1
            # print(rock.pos)
            self.current_max = max(self.current_max, rock.up)
            prev_min = self.current_min
            for r in rock.pos:
                if r[0] in self.rocks.get(r[1] - 1, set()):
                    self.rocks[r[1] - 1].remove(r[0])
                    if len(self.rocks[r[1] - 1]) == 0:
                        del self.rocks[r[1] - 1]
            for r in rock.pos:
                if r[1] in self.rocks:
                    self.rocks[r[1]].add(r[0])
                else:
                    self.rocks[r[1]] = set([r[0]])
                if len(self.rocks[r[1]]) == 7:
                    self.current_min = max(self.current_min, r[1] - 1)
                elif (
                    ite % 5 == 0
                    and r[1] - 1 in self.rocks
                    and len(self.rocks[r[1]]) > 5
                ):
                    tmp = set([i for i in range(7)])
                    tmp.difference_update(self.rocks[r[1]])
                    if tmp.issubset(self.rocks[r[1] - 1]):
                        self.current_min = max(self.current_min, r[1] - 1)
            for i in range(prev_min, self.current_min):
                if i in self.rocks:
                    del self.rocks[i]
            ite += 1
            ite_flux += 1
            new_dict = {}
            if ite % 5 == 0 and ite > 0:
                # Previous piece was flat
                new_dict[rock.up] = set([i for i in range(rock.left, rock.right + 1)])
            tmp = set([i for i in range(7)])
            tmp.difference_update(new_dict[rock.up])
            for i in tmp:
                y = rock.up
                while i not in self.rocks[y] and y >= 0:
                    y -= 1
                if y != -1:
                    if y in new_dict:
                        new_dict[y].add(i)
                    else:
                        new_dict[y] = {i}
            return self.current_max + 1

    def fall(self, maxi):
        ite = 0
        ite_flux = 0
        while ite < maxi:
            rock = Rock(ite, 2, self.current_max + 4)
            nb_fall = 0
            while rock.move(
                self.directions[ite_flux % self.nb_flux],
                self.rocks,
                self.current_min,
                nb_fall,
            ):
                ite_flux += 1
                nb_fall += 1
            # print(rock.pos)
            self.current_max = max(self.current_max, rock.up)
            for r in rock.pos:
                if r[1] in self.rocks:
                    self.rocks[r[1]].add(r[0])
                else:
                    self.rocks[r[1]] = set([r[0]])
            ite += 1
            ite_flux += 1
            new_dict = {}
            if ite % 5 == 1 and ite > 1:
                # Previous piece was flat
                new_min = rock.up
                new_dict[rock.up] = set([i for i in range(rock.left, rock.right + 1)])
                tmp = set([i for i in range(6) if i not in new_dict[rock.up]])
                for i in tmp:
                    y = rock.up
                    while y > self.current_min and (
                        y not in self.rocks or i not in self.rocks[y]
                    ):
                        y -= 1
                    new_min = min(self.current_min, y)
                self.current_min = new_min
                for i in range(self.current_min + 1, rock.up):
                    new_dict[i] = self.rocks[i]
                if 6 in new_dict[rock.up]:
                    if rock.up - 1 in new_dict:
                        new_dict[rock.up - 1].add(6)
                    else:
                        new_dict[rock.up - 1] = {6}
                self.rocks = new_dict
        return self.current_max + 1


class Day17(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        chamber = Chamber(input_value)
        return chamber.fall(2022)

    @staticmethod
    def solve_2(input_value):
        chamber = Chamber(input_value)
        return chamber.fall(1000000)
        return chamber.fall(1000000000000)

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
