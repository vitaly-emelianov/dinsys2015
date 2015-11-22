from copy import copy
PRECISION = 1e-12


class View:
    """View class."""

    def __init__(self, init_codes, shift_parameter):
        self.codes = dict(init_codes)
        self.tree = {'root': set(init_codes.values())}
        self.map = dict()
        self.shift_parameter = shift_parameter

    def processStep(self):
        """Process one step of iteration."""
        self.shift()
        self.updateCodes()

    def shift(self):
        """Calculate where every segment maps."""
        for segment in self.codes:
            start = segment[0] + self.shift_parameter
            end = segment[1] + self.shift_parameter
            if start >= 1.:
                self.map[segment] = (start - 1., end - 1.)
            else:
                self.map[segment] = (start, end)

    def updateCodes(self):
        """Calculate next step codes."""
        points = set()
        for segment in self.codes:
            points.add(segment[0])
            points.add(segment[1])
            points.add(self.map[segment][0])
            points.add(self.map[segment][1])

        updated_points = copy(points)
        points = list(points)
        points.sort()
        for i in xrange(1, len(points)):
            if abs(points[i-1] - points[i]) < PRECISION:
                if points[i-1] in updated_points:
                    updated_points.remove(points[i-1])
        points = list(updated_points)
        points.sort()

        new_segments = []
        for i in xrange(1, len(points)):
            new_segments.append((points[i-1], points[i]))

        updated_codes = {}
        for new_segment in new_segments:
            for segment1 in self.codes:
                if self.haveIntersection(new_segment, segment1):
                    for segment2 in self.codes:
                        if self.haveIntersection(new_segment, self.map[segment2]):
                            updated_codes[new_segment] = self.codes[segment2] + self.codes[segment1][-1]
                            if self.codes[segment2] not in self.tree:
                                self.tree[self.codes[segment2]] = set()
                            self.tree[self.codes[segment2]].add(updated_codes[new_segment])
        self.codes = updated_codes

    def haveIntersection(self, segment1, segment2):
        """Check if two given segments have an intersection."""
        if self.overlap(segment1[0], segment1[1], segment2[0], segment2[1]) > PRECISION:
            return True
        else:
            return False

    def overlap(self, min1, max1, min2, max2):
        """Calculate overlap of two given segments."""
        return max(0, min(max1, max2) - max(min1, min2))
