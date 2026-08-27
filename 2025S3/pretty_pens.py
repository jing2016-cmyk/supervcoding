import heapq
import sys


class PrettyPens:
    def __init__(self, colours, prettiness, colour_count):
        self.colours = colours
        self.prettiness = prettiness
        self.versions = [0] * len(colours)
        self.heaps = [[] for _ in range(colour_count)]
        self.best_heaps = []
        self.second_heaps = []
        self.colour_versions = [0] * colour_count
        self.current_best = [None] * colour_count

        for pen, (colour, value) in enumerate(zip(colours, prettiness)):
            heapq.heappush(self.heaps[colour], (-value, pen, 0))

        self.base = 0
        for colour in range(colour_count):
            self._refresh_colour(colour)

    def _top_two(self, colour):
        heap = self.heaps[colour]
        while heap and (
            self.versions[heap[0][1]] != heap[0][2]
            or self.colours[heap[0][1]] != colour
        ):
            heapq.heappop(heap)

        if not heap:
            return None, None

        first = heapq.heappop(heap)
        while heap and (
            self.versions[heap[0][1]] != heap[0][2]
            or self.colours[heap[0][1]] != colour
        ):
            heapq.heappop(heap)

        second = heap[0] if heap else None
        heapq.heappush(heap, first)
        return -first[0], -second[0] if second else None

    def _refresh_colour(self, colour):
        best, second = self._top_two(colour)
        if self.current_best[colour] is not None:
            self.base -= self.current_best[colour]

        self.base += best
        self.current_best[colour] = best
        self.colour_versions[colour] += 1
        version = self.colour_versions[colour]
        heapq.heappush(self.best_heaps, (best, colour, version))
        if second is not None:
            heapq.heappush(self.second_heaps, (-second, colour, version))

    def update_colour(self, pen, new_colour):
        old_colour = self.colours[pen]
        if old_colour == new_colour:
            return
        self.versions[pen] += 1
        self.colours[pen] = new_colour
        heapq.heappush(
            self.heaps[new_colour],
            (-self.prettiness[pen], pen, self.versions[pen]),
        )
        self._refresh_colour(old_colour)
        self._refresh_colour(new_colour)

    def update_prettiness(self, pen, new_value):
        self.versions[pen] += 1
        self.prettiness[pen] = new_value
        colour = self.colours[pen]
        heapq.heappush(
            self.heaps[colour],
            (-new_value, pen, self.versions[pen]),
        )
        self._refresh_colour(colour)

    def _two_valid(self, heap, sign):
        values = []
        while heap and len(values) < 2:
            while heap and heap[0][2] != self.colour_versions[heap[0][1]]:
                heapq.heappop(heap)
            if not heap:
                break
            value, colour, version = heapq.heappop(heap)
            values.append((sign * value, colour, version))
        for value, colour, version in values:
            heapq.heappush(heap, (sign * value, colour, version))
        return values

    def answer(self):
        donors = self._two_valid(self.second_heaps, -1)
        destinations = self._two_valid(self.best_heaps, 1)
        improvement = 0
        for donor_value, donor_colour, _ in donors:
            for destination_value, destination_colour, _ in destinations:
                if donor_colour != destination_colour:
                    improvement = max(
                        improvement, donor_value - destination_value
                    )
        return self.base + max(0, improvement)


def solve(data):
    values = list(map(int, data.split()))
    if not values:
        return ""

    iterator = iter(values)
    pen_count = next(iterator)
    colour_count = next(iterator)
    query_count = next(iterator)
    colours = [0] * pen_count
    prettiness = [0] * pen_count

    for pen in range(pen_count):
        colours[pen] = next(iterator) - 1
        prettiness[pen] = next(iterator)

    pens = PrettyPens(colours, prettiness, colour_count)
    answers = [str(pens.answer())]

    for _ in range(query_count):
        update_type = next(iterator)
        pen = next(iterator) - 1
        value = next(iterator)
        if update_type == 1:
            pens.update_colour(pen, value - 1)
        else:
            pens.update_prettiness(pen, value)
        answers.append(str(pens.answer()))

    return "\n".join(answers)


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.buffer.read()))
    sys.stdout.write("\n")
