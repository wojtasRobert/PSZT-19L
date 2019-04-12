from heapq import heappush, heappop


class TooManyIterations(Exception):
    pass


def a_star(state, final, max_iterations=300, step=False):
    open_set = []
    closed_set = []

    heappush(open_set, state)
    iterations = 0

    while len(open_set) > 0:
        current_state = heappop(open_set)
        closed_set.append(current_state)

        iterations += 1

        if step:
            print(current_state)
            input()

        if current_state == final:
            return current_state, iterations

        if iterations > max_iterations:
            raise TooManyIterations

        for child in current_state.sprout():
            if child not in closed_set:
                heappush(open_set, child)

