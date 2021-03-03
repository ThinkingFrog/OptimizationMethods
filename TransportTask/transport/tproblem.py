import sys

import tabulate


class TransportProblem:
    def __init__(self, filename):
        self._demand = list()
        self._supply = list()
        self._costs = list()
        self._matrix = list()

        with open(filename, 'r') as f:
            problem = f.read().splitlines()

        supply = problem.pop(0).split()
        self._supply = [int(item) for item in supply]

        demand = problem.pop(0).split()
        self._demand = [int(item) for item in demand]

        while len(problem) > 0:
            costs = problem.pop(0).split(' ')
            self._costs.append([int(item) for item in costs])
        self.matrix = [[self.Shipment(0,0,0,0) for j in range(len( self._demand ))] for i in range(len( self._demand ))]
        print("Проверим задачу на замкнутость:")

        sum_sup = sum(self._supply)
        sum_dem = sum(self._demand)
        print("Сумма запасов:" + str(sum_sup))
        print("Сумма спросов:" + str(sum_dem))

        if sum_sup > sum_dem:
            print("Приведем задачу к замкнутому виду, добавив фиктовного поставщика")
            self._demand.append(sum_sup - sum_dem)
            for line in self._costs:
                line.append(0)

        elif sum_sup < sum_dem:
            print("Приведем задачу к замкнутому виду, добавив фиктовного заказчика")
            self._supply.append(sum_dem - sum_sup)
            self._costs.append([0] * len(self._costs[0]))
            pass

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
        rows = list()
        headers = [""]
        for col, item in enumerate(self._demand):
            headers.append(f"consumer {col + 1} needs {item}")
        for row_num, item in enumerate(self._supply):
            cur_row = list()
            cur_row.append(f"supplier {row_num + 1} supplies {item}")
            for col_num in range(len(self._demand)):
                cur_row.append(self._costs[row_num][col_num])
            rows.append(cur_row)
        # tablefmt="latex"
        print(tabulate.tabulate(rows, headers))

    def northWestCornerRule(self):
        northwest = 0
        for r in range(0, len(self._supply)):
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
        leaving = self.Shipment()

        self.fixDegenerateCase()
        for r in range(0, len(self._supply)):
            for c in range(0, len(self._demand)):
                if self._matrix[r][c] != None:
                    pass

                trail = self.Shipment(0, self._costs[r][c], r, c)
                path = self.getClosedPath(trail)

                reduction = 0
                lowestQuantity = sys._maxint
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
        result = list()
        for row in self._matrix:
            for shipment in row:
                if shipment is not None:
                    result.append(shipment)
        return result

    def getNeighbors(self, s: Shipment, s_list: Shipment):
        nbrs = self.Shipment[2]
        for el in s_list:
            if el != s:
                if self.Shipment(el).r == s.r and nbrs[0] is None:
                    nbrs[0] = el
                elif self.Shipment(el).r == s.r and nbrs[1] is None:
                    nbrs[1] = el
                if nbrs[0] is not None and nbrs[1] is not None:
                    break
        return nbrs

    def getClosedPath(self, s: Shipment):
        path = self.matrixToList()
        path.insert(0, s)
        removed = list()
        for el in path :
            nbrs = self.getNeighbors(el, path)
            if nbrs[0] is None or nbrs[1] is None:
                removed.append(el)
                path.remove(el)
        stones = self.Shipment[len(path)]
        prev = s
        for i in range(len(stones)):
            stones[i] = prev
            prev = self.getNeighbors(prev,path)[i%2]
        return stones

    def fixDegenerateCase(self):
        eps = sys.float_info.min * sys.float_info.epsilon
        if len(self._supply)+len(self._demand) - 1 != len(self.matrixToList()):
            for r in range(len(self._supply)):
                for c in range(len(self._demand)):
                    if self._matrix[r][c] is None:
                        dummy = self.Shipment(eps, self._costs[r][c],c)
                        if len(self.getClosedPath(dummy)) is None :
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
                    totalCosts+=(s.quantity*s.costPerUnit)
                else:
                    print(("  -  "))
        print(f"Итоговые минимальные затраты = {totalCosts}")

