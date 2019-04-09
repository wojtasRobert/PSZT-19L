from queue import PriorityQueue


def a_star(state, final):
    open_set = PriorityQueue()
    closed_set = []

    open_set.put(state)
    iterations = 0

    while not open_set.empty():
        current_state = open_set.get()
        closed_set.append(current_state)

        if current_state == final:
            return current_state, iterations

        for child in current_state.sprout():
            if child not in closed_set:
                open_set.put(child)

        iterations += 1
