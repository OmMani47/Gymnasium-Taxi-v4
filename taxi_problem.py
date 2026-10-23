# this is a knowledge base


class TaxiProblem:
    def __init__(self, start_state):
        self.start = start_state    
        # 4 loactions
        self.locations = {
            0: (0, 0),  # red
            1: (0, 4),        # Green
            2: (4, 0),  #    Yellow
            3: (4, 3),               # blue
        }

        _, _, passenger, destination = self.decode(start_state)
        if passenger == destination:
            raise ValueError(
                "Invalid start state as passenger is already at destination"
            )

    def start_state(self):
        return self.start

    def goal_test(self, state):
        """true when passenger location is == to destination"""
        _, _, passenger, destination = self.decode(state)
        return passenger == destination

    def SuccAndCost(self, state):                                  # get all valid next moves from this state
        row, col, passenger, destination = self.decode(state)
        result = []

        for action in range(6):                          # 0-3 move, 4 pickup, 5 dropoff
            new_row, new_col = row, col
            new_passenger = passenger

            if action < 4:  # movement
                if not self.is_valid_move(row, col, action):
                    continue
                if action == 0:
                    new_row += 1           # south
                elif action == 1:
                    new_row -= 1        #north
                elif action == 2:             
                    #east         
                    new_col += 1     #east
                elif action == 3:
                    new_col -= 1                        #west
            elif action == 4:  # pickup
                if passenger < 4 and (row, col) == self.locations[passenger]:
                    new_passenger = 4
                else:
                    continue

            elif action == 5:  # this is dropoff action
                if passenger == 4 and (row, col) == self.locations[destination]:
                    new_passenger = destination                  
                else:
                    continue  # invalid dropoff

            new_state = self.encode(new_row, new_col, new_passenger, destination)
            result.append((action, new_state, 1))  # cost = 1

        return result

    def decode(self, state):               # decoding actual values from 0-499
        dest = state % 4
        state //= 4
        passenger = state % 5
        state //= 5
        col = state % 5
        row = state // 5
        return row, col, passenger, dest

    def encode(self, row, col, passenger, dest):             #encoding
        return ((row * 5 + col) * 5 + passenger) * 4 + dest

    def is_valid_move(self, row, col, action):
        if action == 0:  # south
            return row < 4
        if action == 1:  # north
            return row > 0
        if action == 2:  # east
            if row in (0, 1) and col == 1:
                return False                     #wall hit
            if row in (3, 4) and col in (0, 2):
                return False              # hit wall
            return col < 4
        if action == 3:  # west
            if row in (0, 1) and col == 2:
                return False                 #hits wall
            if row in (3, 4) and col in (1, 3):
                return False                    #wall hit
            return col > 0
        return True

