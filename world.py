import random


class Environment:
    def __init__(self, cost, max_benefit, func_coupling, num_components, benefits=None, body_size_limit=False):
        self.cost = cost
        self.max_benefit = max_benefit
        assert(0 <= func_coupling <= 1)
        self.func_coupling = func_coupling
        self.body_size_limit = body_size_limit

        if benefits is not None:
            assert(len(benefits) == num_components)
            self.benefits = list(benefits)  # copy list by value
        else:
            # initialise component benefits based on functional coupling
            self.benefits = []
            global_factor = random.random()
            for i in range(num_components):
                self.benefits.append(
                    (self.func_coupling * global_factor * max_benefit) +
                    ((1-self.func_coupling) * random.random() * max_benefit)
                )

    def evaluate(self, critter):
        total_benefit = sum([size * benefit for size, benefit in zip(critter.sizes, self.benefits)])
        total_cost = self.calc_cost(critter)
        return total_benefit - total_cost

    def calc_cost(self, critter):
        if self.body_size_limit:
            return self.cost * critter.size() * 0.25 * ((3/critter.size()) + (critter.size()/3))**2
        else:
            return self.cost * critter.size()

    def __repr__(self):
        return str([b-self.cost for b in self.benefits]) + ("_with_body_size_limit" if self.body_size_limit else "")


def create_fixed_environment(cost, benefits):
    max_benefit = max(benefits)
    func_coupling = (max(benefits) - min(benefits)) / max(benefits)
    num_components = len(benefits)
    return Environment(cost, max_benefit, func_coupling, num_components, benefits)


def create_random_environment(cost_range, max_benefit_range, func_coupling_range, num_components, body_size_limit=False):
    cost = random.uniform(*cost_range)
    max_benefit = random.uniform(*max_benefit_range)
    func_coupling = random.uniform(*func_coupling_range)
    return Environment(cost, max_benefit, func_coupling, num_components, body_size_limit=body_size_limit)
