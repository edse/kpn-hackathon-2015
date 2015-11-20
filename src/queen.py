import sys
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from random import shuffle


class Queen:
    def __init__(self, rows, cols, max_queens_on_sight=0, initial_queens=[]):

        self.initial_queens = initial_queens
        self.max_queens_on_sight = max_queens_on_sight
        self.rows = rows
        self.cols = cols
        self.matrix = [[0 for i in xrange(cols)] for i in xrange(rows)]
        self.queens = []
        self.start = datetime.now()
        self.max_time = self.start + timedelta(milliseconds=+1700)
        self.best = []
        self.tries = 0

        for position in initial_queens:
            self.place_queen([position.get('x'), position.get('y')])

        self.solve()

    def place_queen(self, position):
        if position[0] < 0 or position[0] >= self.rows or \
           position[1] < 0 or position[1] >= self.cols:
            return None

        if position in self.queens:
            return None

        on_sight = self.queens_on_sight(position)
        if len(on_sight) > self.max_queens_on_sight:
            return None

        self.queens.append(position)
        self.matrix[position[0]][position[1]] = 1

    def queens_on_sight(self, position):
        if not self.queens:
            return []

        queens = []
        sight = self.get_sight(position)

        for position in self.queens:
            if position in sight:
                queens.append(position)

        return queens

    def get_sight(self, position):
        sight = []

        for i in range(self.rows):
            sight.append([position[0], i])

        for i in range(self.cols):
            sight.append([i, position[1]])

        for i in range(min([self.rows, self.cols])):
            should_break = False

            tb1 = [position[0] + 1, position[1] - 1]
            bt1 = [position[0] - 1, position[1] + 1]

            tb2 = [position[0] + 1, position[1] + 1]
            bt2 = [position[0] - 1, position[1] - 1]

            if tb1[0] > self.rows or tb1[1] < 0:
                should_break = True
            else:
                sight.append(tb1)

            if bt1[0] < 0 or bt1[1] > self.cols:
                should_break = True
            else:
                sight.append(bt1)

            if tb2[0] > self.rows or tb2[1] > self.cols:
                should_break = True
            else:
                sight.append(tb2)

            if bt2[0] < 0 or bt2[1] < 0:
                should_break = True
            else:
                sight.append(bt2)

            if should_break:
                break

        return sight

    def free_positions(self):
        positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.matrix[row][col]:
                    positions.append([row, col])

        return positions

    def on_sight_positions(self):
        positions = []
        for q in self.queens:
            positions += self.get_sight(q)

        return positions

    def display(self):
        print 'time: ', datetime.now() - self.start
        print 'tries: ', self.tries
        print 'queens: ', len(self.queens)
        for row in self.matrix:
            print row

    def elapsed_time(self):
        d = datetime.now() - self.start
        return d.microseconds + d.seconds * 1000

    def added_queens(self):
        added = []
        for item in self.queens:
            if item not in self.initial_queens:
                added.append({'x': item[0], 'y': item[1]})

        return added

    def solve(self, retry=False):
        self.tries += 1

        if retry:
            self.matrix = [
                [0 for i in xrange(self.cols)] for i in xrange(self.rows)
            ]
            self.queens = []

        free = self.free_positions()

        # adding some black magic ;-)
        if self.rows > 1 and self.cols > 1:
            shuffle(free)

        for position in free:
            self.place_queen(position)

        if len(self.best) < len(self.queens):
            self.best = self.queens
        else:
            self.queens = self.best

        # there still time left? lest make some more magic
        if datetime.now() < self.max_time:
            self.solve(retry=True)
        else:
            self.display()
            return self.added_queens()


if __name__ == '__main__':
    sys.setrecursionlimit(2000)
    app = Flask(__name__)

    @app.route('/max_queens', methods=['POST'])
    def max_queens():
        queen = Queen(
            request.get_json(force=True).get('rows'),
            request.get_json(force=True).get('columns'),
            request.get_json(force=True).get('max_queens_on_sight'),
            request.get_json(force=True).get('initial_queens'),
        )

        response = {'added_queens': queen.added_queens()}

        return jsonify(**response)

    @app.route('/')
    def index():
        return "Ahhhh ma papaya!"

    app.run(debug=True, host='0.0.0.0', port=8080)
