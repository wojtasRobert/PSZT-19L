from queue import PriorityQueue


class TooManyIterations(Exception):
    pass

def a_star(state, final, max_iterations=300):
    open_set = PriorityQueue()
    closed_set = []

    open_set.put(state)
    iterations = 0

    while not open_set.empty():
        current_state = open_set.get()
        closed_set.append(current_state)

        if current_state == final:
            return current_state, iterations

        if iterations > max_iterations:
            raise TooManyIterations

        for child in current_state.sprout():
            if child not in closed_set:
                open_set.put(child)

        iterations += 1
