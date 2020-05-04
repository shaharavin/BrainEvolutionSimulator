import math
from collections import Counter

from critters import BrainEvolver, MutatingBrainEvolver
from world import Environment, create_random_environment


def init_population(num_critters, max_size, dev_coupling, num_components, mutating=False):
    if mutating:
        evolver_cls = MutatingBrainEvolver
    else:
        evolver_cls = BrainEvolver

    population = []
    for i in range(num_critters):
        population.append(evolver_cls(max_size, dev_coupling, num_components))
    return population


def evolve_and_calc_sizes(population, environment, num_generations, num_offspring, lifespan):

    assert(len(population[0].sizes) == len(environment.benefits))
    current_gen = list(population)
    num_critters = len(current_gen)

    evolution_history = [population]

    for g in range(num_generations):

        if not (g % 20):
            print("%d\r"%g, end="")

        # grow old and multiply
        for c in current_gen[:num_critters]:
            c.age += 1
            for i in range(num_offspring):
                current_gen.append(c.offspring())

        # death of the elderly
        current_gen = [c for c in current_gen if c.age < lifespan]
        # survival of the fittest
        sorted_by_fitness = sorted(current_gen, key=environment.evaluate, reverse=True)
        current_gen = sorted_by_fitness[:num_critters]

        evolution_history.append(list(current_gen))

    return evolution_history


def init_evolve_and_calc_sizes(
        num_critters,
        num_generations,
        num_offspring,
        lifespan,
        num_components,
        max_size,
        dev_coupling,
        cost,
        max_benefit,
        func_coupling):

    population = init_population(num_critters, max_size, dev_coupling, num_components)
    environment = Environment(cost, max_benefit, func_coupling, num_components)

    return evolve_and_calc_sizes(population, environment, num_generations, num_offspring, lifespan)


def init_evolve_and_calc_log_sizes(
        default_params_dict,
        param_range_dict,
        num_runs):
    data = {}

    assert(len(param_range_dict) == 1)

    key = list(param_range_dict.keys())[0]
    values = list(param_range_dict.values())[0]

    for value in values:
        data[value] = []
        default_params_dict[key] = value
        for i in range(num_runs):
            if not (i%100):
                print(i)
            final_gen = init_evolve_and_calc_sizes(**default_params_dict)[-1]
            data[value].append(calc_average_degree_of_mosaicism(final_gen))
    return data


def calc_average_degree_of_mosaicism(population):
    # calc degree of mosaicism (log of ratio between largest and smallest component)
    # for each critter in the population
    degree_of_mosaicism = [math.log(max(c.sizes)/min(c.sizes)) for c in population]
    # average across the population
    return sum(degree_of_mosaicism)/len(degree_of_mosaicism)


def init_mixed_population(
        num_critters,
        num_components,
        max_size,
        dev_coupling_concerted,
        dev_coupling_mosaic,
        dev_coupling_hybrid,
        mutating=False):

    concerted_population = init_population(
        num_critters=num_critters,
        num_components=num_components,
        max_size=max_size,
        dev_coupling=dev_coupling_concerted,
        mutating=mutating)
    mosaic_population = init_population(
        num_critters=num_critters,
        num_components=num_components,
        max_size=max_size,
        dev_coupling=dev_coupling_mosaic,
        mutating=mutating)
    hybrid_population = init_population(
        num_critters=num_critters,
        num_components=num_components,
        max_size=max_size,
        dev_coupling=dev_coupling_hybrid,
        mutating=mutating)
    return concerted_population + mosaic_population + hybrid_population


def evolve_and_compare_populations(
        num_critters,
        num_components,
        max_size,
        dev_coupling_concerted,
        dev_coupling_mosaic,
        dev_coupling_hybrid,
        cost,
        max_benefit,
        func_coupling,
        num_generations,
        num_offspring,
        lifespan,
        num_iterations,
        fixed_environment=None,
        retain_history=False):

    population = init_mixed_population(
        num_critters,
        num_components,
        max_size,
        dev_coupling_concerted,
        dev_coupling_mosaic,
        dev_coupling_hybrid)

    results = []
    if retain_history:
        history = []

    for i in range(num_iterations):

        if not (i % 100):
            print(i)

        if fixed_environment is not None:
            environment = fixed_environment
        else:
            environment = Environment(
                cost=cost,
                max_benefit=max_benefit,
                num_components=num_components,
                func_coupling=func_coupling)

        r = evolve_and_calc_sizes(list(population), environment, num_generations, num_offspring, lifespan)

        results.append(Counter([c.dev_coupling for c in r[-1]]))

        if retain_history:
            history.append({
                "environments": [environment],
                "critter_counts": [[Counter([c.dev_coupling for c in generation]) for generation in r]]
            })

    if retain_history:
        return results, history
    else:
        return results


def evolve_and_compare_mutating_populations_with_variable_environment(
        num_critters,
        num_components,
        max_size,
        dev_coupling_concerted,
        dev_coupling_mosaic,
        dev_coupling_hybrid,
        cost_range,
        max_benefit_range,
        func_coupling_range,
        num_generations_to_env_switch,
        num_episodes,
        num_offspring,
        lifespan,
        num_iterations,
        retain_history=False):

    results = []
    if retain_history:
        history = []

    for i in range(num_iterations):

        if not (i % 100):
            print(i)

        if retain_history:
            environments = []
            critter_counts = []

        population = init_mixed_population(
            num_critters,
            num_components,
            max_size,
            dev_coupling_concerted,
            dev_coupling_mosaic,
            dev_coupling_hybrid,
            mutating=False)

        for j in range(num_episodes):
            environment = create_random_environment(
                cost_range, max_benefit_range, func_coupling_range, num_components)
            r = evolve_and_calc_sizes(
                list(population), environment, num_generations_to_env_switch, num_offspring, lifespan)
            if retain_history:
                environments.append(environment)
                critter_counts.append([Counter([c.dev_coupling for c in generation]) for generation in r])
            population = r[-1]
        results.append(Counter([c.dev_coupling for c in population]))
        if retain_history:
            history.append({"environments": environments, "critter_counts": critter_counts})

    if retain_history:
        return results, history
    else:
        return results
