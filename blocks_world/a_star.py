from heapq import heappush, heappop


class TooManyIterations(Exception):
    pass


def a_star(state, final, max_iterations=300, step=False):
    open_set = []

    heappush(open_set, state)
    iterations = 0

    while len(open_set) > 0:
        iterations += 1

        current_state = heappop(open_set)

        if step:
            print(current_state)
            # input()

        if current_state == final:
            return current_state, iterations

        for child in current_state.sprout():
            try:
                existing_child_idx = open_set.index(child)
                existing_child = open_set[existing_child_idx]
                # child is in the open set
                if child.cost < existing_child.cost:
                    del open_set[existing_child_idx]
                    heappush(open_set, child)
            except ValueError:
                # child is not in the open_set
                heappush(open_set, child)

        if iterations > max_iterations:
            raise TooManyIterations

    assert False
