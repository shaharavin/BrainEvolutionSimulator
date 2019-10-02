import random


class BrainEvolver:
    def __init__(self, max_size, dev_coupling, num_components, sizes=None):
        self.max_size = max_size
        assert(0 <= dev_coupling <= 1)
        self.dev_coupling = dev_coupling
        self.age = 0

        if sizes is not None:
            assert(len(sizes) == num_components)
            self.sizes = list(sizes)  # copy list by value
        else:
            # initialise random individual component sizes
            self.sizes = [1] * num_components
            # for i in range(num_components):
            #    self.sizes.append(random.random()*max_size)

    def size(self):
        return sum(self.sizes)

    @staticmethod
    def _get_mutation_factor():
        return 0.5 + random.random()  # uniform distribution between 0.5 and 1.5

    def mutate(self):
        global_factor = self._get_mutation_factor()
        for i, size in enumerate(self.sizes):
            self.sizes[i] = (
                (self.dev_coupling * global_factor * size) +
                ((1-self.dev_coupling) * self._get_mutation_factor() * size)
            )

    def offspring(self):
        newborn = BrainEvolver(
            self.max_size,
            self.dev_coupling,
            len(self.sizes),
            self.sizes)
        newborn.mutate()
        return newborn

    def __repr__(self):
        return str(self.sizes)


class MutatingBrainEvolver(BrainEvolver):
    def mutate(self):
        self.dev_coupling = random.choice([0.0, 0.5, 1.0])
        super(MutatingBrainEvolver, self).mutate()

    def offspring(self):
        newborn = MutatingBrainEvolver(
            self.max_size,
            self.dev_coupling,
            len(self.sizes),
            self.sizes)
        newborn.mutate()
        return newborn
