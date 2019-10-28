class PQueue:
    def __init__(self):
        self.items = []

    def push(self, node):
        self.items.append(node)
        self.items = sorted(self.items, key=lambda x: x[1])  # sort by value which is the second entry

    def decrease_key(self, u, value):
        for index, element in enumerate(self.items):
            if element[0] == u:
                self.items[index][1] = value
                print("yay")
                return

    def pop_min(self):
        return self.items.pop(0)

    def get_length(self):
        return len(self.items)

    def __contains__(self, item):
        if item in self.items:
            return True
        else:
            return False