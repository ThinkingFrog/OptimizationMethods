import sys
import tabulate

from itertools import chain
from typing import List


class TransportProblem:
    def __init__(self, filename):
        self._demand = []
        self._supply = []
        self._costs = []
        self._matrix = []
        self._penalties = False

        with open(filename, 'r') as f:
            problem = f.read().splitlines()

        supply = problem.pop(0).split()
        self._supply = [int(item) for item in supply]

        demand = problem.pop(0).split()
        self._demand = [int(item) for item in demand]

        while len(problem) > 0:
            costs = problem.pop(0).split(' ')
            if costs[0] == "penalty":
                self._penalties = True
                penalties = []
                while len(problem) > 0:
                    costs = problem.pop(0).split(' ')
                    penalties.append([int(item) for item in costs])
                break
            else:
                self._costs.append([int(item) for item in costs])
        self._matrix = [
            [self.Shipment(0, 0, 0, 0) for _ in range(len(self._demand))]
            for _ in range(len(self._demand))
        ]

        print("Проверим задачу на замкнутость:")

        sum_sup = sum(self._supply)
        sum_dem = sum(self._demand)
        print(f"Сумма запасов:{str(sum_sup)}")
        print(f"Сумма спросов:{str(sum_dem)}")

        if self._penalties:
            for i in range(len(penalties[0])):
                if abs(sum_sup - sum_dem) >= penalties[0][i]:
                    sum_peny = penalties[1][i]

        if sum_sup > sum_dem:
            print("Приведем задачу к замкнутому виду, добавив фиктовного поставщика")
            self._demand.append(sum_sup - sum_dem)
            for line in self._costs:
                if self._penalties:
                    line.append(sum_peny)
                else:
                    line.append(0)


        elif sum_sup < sum_dem:
            print("Приведем задачу к замкнутому виду, добавив фиктовного заказчика")
            self._supply.append(sum_dem - sum_sup)
            if self._penalties:
                self._costs.append([sum_peny] * len(self._costs[0]))
            else:
                self._costs.append([0] * len(self._costs[0]))


        else:
            print("Задача замкнутого вида")

    class Shipment:
        costPerUnit = 0.0
        quantity = 0.0
        r = 0
        c = 0

        def __init__(self, quantity, costPerUnit, r, c):
            self.quantity = quantity
            self.costPerUnit = costPerUnit
            self.r = r
            self.c = c

    def print_table(self):
        rows = []
        headers = [""]
        headers.extend(
            f"consumer {col + 1} needs {item}"
            for col, item in enumerate(self._demand)
        )

        for row_num, item in enumerate(self._supply):
            cur_row = [f"supplier {row_num + 1} supplies {item}"]
            cur_row.extend(
                self._costs[row_num][col_num]
                for col_num in range(len(self._demand))
            )

            rows.append(cur_row)
        # tablefmt="latex"
        print(tabulate.tabulate(rows, headers))

    def northWestCornerRule(self):
        northwest = 0
        for r in range(len(self._supply)):
            for c in range(northwest, len(self._demand)):
                quantity = min(self._supply[r], self._demand[c])
                if quantity > 0:
                    self._matrix[r][c] = self.Shipment(quantity, self._costs[r][c], r, c)
                    self._supply[r] = self._supply[r] - quantity
                    self._demand[c] = self._demand[c] - quantity
                    if self._supply[r] == 0:
                        northwest = c
                        break

    def steppingStone(self):
        maxReduction = 0
        move = []
        leaving = []

        self.fixDegenerateCase()
        for r in range(len(self._supply)):
            for c in range(len(self._demand)):
                trail = self.Shipment(0, self._costs[r][c], r, c)
                path = self.getClosedPath(trail)

                reduction = 0
                lowestQuantity = sys.maxsize
                leavingCandidate = None

                plus = True
                for s in path:
                    if plus == True:
                        reduction = reduction + s.costPerUnit
                    else:
                        reduction = reduction - s.costPerUnit
                        if s.quantity < lowestQuantity:
                            leavingCandidate = s
                            lowestQuantity = s.quantity
                    plus = not plus
                if reduction < maxReduction:
                    move = path
                    leaving = leavingCandidate
                    maxReduction = reduction

        if move != None:
            q = leaving.quantity
            plus = True
            for s in move:
                s.quantity = s.quantity + q if plus else s.quantity - q
                self.matrix[s.r][s.c] = None if s.quantity == 0 else s
                plus = not plus
            self.steppingStone()

    def matrixToList(self):
        result = []
        for row in self._matrix:
            result.extend(shipment for shipment in row if shipment is not None)
        return result

    def getNeighbors(self, s: Shipment, s_list):
        print(s_list)
        nbrs = {'0': None, '1': None}
        for el in s_list:
            if el != s:
                if el.r == s.r:
                    if nbrs['0'] is None:
                        nbrs['0'] = el
                    elif nbrs['1'] is None:
                        nbrs['1'] = el
                if nbrs['0'] is not None and nbrs['1'] is not None:
                    break
        return nbrs

    def getClosedPath(self, s: Shipment):
        path = self.matrixToList()
        path.insert(0, s)
        removed = []
        for el in path:
            nbrs = self.getNeighbors(el, path)
            if nbrs['0'] is None or nbrs['1'] is None:
                removed.append(el)
                path.remove(el)
        prev = s
        stones = []
        for i in range(len(path)):
            stones.append(prev)
            tmp = self.getNeighbors(prev, path)
            index = i % 2
            prev = tmp['1'] if index == 1 else tmp['0']
        return stones

    def fixDegenerateCase(self):
        eps = sys.float_info.min * sys.float_info.epsilon
        if len(self._supply) + len(self._demand) - 1 != len(self.matrixToList()):
            for r in range(len(self._supply)):
                for c in range(len(self._demand)):
                    if self._matrix[r][c] is None:
                        dummy = self.Shipment(eps, self._costs[r][c], c)
                        if len(self.getClosedPath(dummy)) is None:
                            self._matrix[r][c] = dummy
                            return

    def print_result(self):
        print("Оптимальное решение")
        totalCosts = 0
        for r in range(len(self._supply)):
            for c in range(len(self._demand)):
                s = self._matrix[r][c]
                if s is not None and s.r == r and s.c == c:
                    print(s.quantity)
                    totalCosts += (s.quantity * s.costPerUnit)
                else:
                    print(("  -  "))
        print(f"Итоговые минимальные затраты = {totalCosts}")

    def to_canonical(self):
        matrix = [
            [0 for _ in range(len(self._supply) * len(self._demand))]
            for _ in range(len(self._supply) + len(self._demand) - 1)
        ]

        for row in range(len(self._supply) + len(self._demand) - 1):
            for col in range(len(self._supply) * len(self._demand)):
                if (row < len(self._demand) - 1 and col in range(row * 5, (row + 1) * 5)) or (
                        row >= (len(self._demand) - 1) and col % 5 == row - len(self._demand) + 1):
                    matrix[row][col] = 1

        free_vector = self._supply + self._demand
        free_vector.pop()

        target = list(chain.from_iterable(self._costs))
        target.append("min")

        return matrix, free_vector, target


    def cost_summary(self, solution: List[List[int]]):
        sum = 0
        for row in range(len(solution)):
            for col in range(len(solution[row])):
                sum += solution[row][col] * self._costs[row][col]
        return sum
