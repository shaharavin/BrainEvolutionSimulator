from simulation import init_evolve_and_calc_log_sizes, evolve_and_compare_populations, \
    evolve_and_compare_mutating_populations_with_variable_environment
from visualisation import plot_sizes_boxplot, plot_populations_boxplot, save_boxplot_data_to_csv, \
    save_history_to_csv
from world import create_fixed_environment

DEV_COUPLINGS = [0.0, 0.5, 1.0]

DEFAULTS = {
    'dev_coupling': 0.0,
    'func_coupling': 0.0,
    'num_critters': 100,
    'num_generations': 100,
    'num_offspring': 3,
    'lifespan': 3,
    'num_components': 3,
    'max_size': 3,
    'cost': 1,
    'max_benefit': 2
}
NUM_RUNS = 1000


def generate_mosaicism_plots_for_homogeneous_populations():

    defaults = DEFAULTS.copy()

    for func_coupling in [0.0, 0.5, 1.0]:
        for max_benefit in [1, 2, 4]:
            range_values = [0.0, 0.5, 1.0]
            range_param = {
                'dev_coupling': range_values
            }
            defaults['func_coupling'] = func_coupling
            defaults['max_benefit'] = max_benefit
            data = init_evolve_and_calc_log_sizes(defaults, range_param, NUM_RUNS)
            base_filename = 'box_plot_homogeneous_func_coupling_%.1f_max_benefit_%.1f' % \
                            (func_coupling, max_benefit)
            values = [list(data[value]) for value in range_values]
            save_boxplot_data_to_csv(base_filename + '.csv', range_values, values)
            # plot_sizes_boxplot(base_filename + '.png', range_values, values)


def generate_competition_plots():

    params = DEFAULTS.copy()

    params['dev_coupling_mosaic'] = DEV_COUPLINGS[0]
    params['dev_coupling_hybrid'] = DEV_COUPLINGS[1]
    params['dev_coupling_concerted'] = DEV_COUPLINGS[2]
    params['num_iterations'] = NUM_RUNS

    del(params['dev_coupling'])

    total_population = params['num_critters']*len(DEV_COUPLINGS)

    for func_coupling in [0.0, 0.5, 1.0]:
        for max_benefit in [1, 2, 4]:
            params['func_coupling'] = func_coupling
            params['max_benefit'] = max_benefit
            data = evolve_and_compare_populations(**params)
            base_filename = 'box_plot_competition_func_coupling_%.1f_max_benefit_%.1f' % \
                            (func_coupling, max_benefit)
            keys = DEV_COUPLINGS
            values = [[(result.get(dev_coupling, 0) / total_population)
                       for result in data] for dev_coupling in DEV_COUPLINGS]
            save_boxplot_data_to_csv(base_filename + '.csv', keys, values)
            # plot_populations_boxplot(base_filename + '.png', keys, values)


ENVIRONMENTS = [
    create_fixed_environment(1, [22, 2, 0]),  # [21,  1, -1]
    create_fixed_environment(1, [12, 8, 4]),  # [11,  7,  3]
    create_fixed_environment(1, [8, 8, 8]),   # [ 7,  7,  7]
    create_fixed_environment(3, [16, 2, 0]),  # [14, -1, -3]
    create_fixed_environment(3, [9, 6, 3]),   # [ 6,  3,  0]
    create_fixed_environment(3, [6, 6, 6]),   # [ 3,  3,  3]
    create_fixed_environment(5, [10, 2, 0]),  # [ 5, -3, -5]
    create_fixed_environment(5, [6, 4, 2]),   # [ 1, -1, -3]
    create_fixed_environment(5, [4, 4, 4])    # [-1, -1, -1]
]


def generate_competition_plots_specific_environments():

    params = DEFAULTS.copy()

    params['dev_coupling_mosaic'] = DEV_COUPLINGS[0]
    params['dev_coupling_hybrid'] = DEV_COUPLINGS[1]
    params['dev_coupling_concerted'] = DEV_COUPLINGS[2]
    params['num_iterations'] = NUM_RUNS

    del(params['dev_coupling'])

    total_population = params['num_critters']*len(DEV_COUPLINGS)

    for environment in ENVIRONMENTS:
        params['func_coupling'] = environment.func_coupling
        params['max_benefit'] = environment.max_benefit
        params['fixed_environment'] = environment
        data = evolve_and_compare_populations(**params)
        base_filename = 'box_plot_competition_fixed_environment_%s' % str(environment).replace(',', '_')
        keys = DEV_COUPLINGS
        values = [[(result.get(dev_coupling, 0) / total_population) for result in data]
                  for dev_coupling in DEV_COUPLINGS]
        save_boxplot_data_to_csv(base_filename + '.csv', keys, values)
        # plot_populations_boxplot(base_filename + '.png', keys, values)


NORMAL_RANGE = {
    'name': 'normal_range',
    'cost_range': [0.5, 5.0],
    'max_benefit_range': [1.0, 10.0],
    'func_coupling_range': [0.0, 1.0]
}

EXTREME_RANGE = {
    'name': 'extreme_range',
    'cost_range': [0.0, 10.0],
    'max_benefit_range': [0.0, 30.0],
    'func_coupling_range': [0.0, 1.0]
}


def generate_variable_environment_plots(range_params):

    params = DEFAULTS.copy()

    params['dev_coupling_mosaic'] = DEV_COUPLINGS[0]
    params['dev_coupling_hybrid'] = DEV_COUPLINGS[1]
    params['dev_coupling_concerted'] = DEV_COUPLINGS[2]
    params['num_generations_to_env_switch'] = 10
    params['num_episodes'] = 10
    params['num_iterations'] = NUM_RUNS
    params['cost_range'] = range_params['cost_range']
    params['max_benefit_range'] = range_params['max_benefit_range']
    params['func_coupling_range'] = range_params['func_coupling_range']

    del(params['num_generations'])
    del(params['dev_coupling'])
    del(params['cost'])
    del(params['max_benefit'])
    del(params['func_coupling'])

    total_population = params['num_critters']*len(DEV_COUPLINGS)

    for lifespan in [1, 3, 9]:
        for num_offspring in [1, 3, 9]:
            params['lifespan'] = lifespan
            params['num_offspring'] = num_offspring
            data = evolve_and_compare_mutating_populations_with_variable_environment(**params)
            filename_base = 'box_plot_competition_var_env_%s_lifespan_%d_offspring_%d' % \
                            (range_params['name'], lifespan, num_offspring)
            keys = DEV_COUPLINGS
            values = [[(result.get(dev_coupling, 0) / total_population) for result in data]
                      for dev_coupling in DEV_COUPLINGS]
            save_boxplot_data_to_csv(filename_base + '.csv', keys, values)
            # plot_populations_boxplot(filename_base + '.png', keys, values)


def generate_variable_environment_long_evolution_data(range_params):

    params = DEFAULTS.copy()

    params['dev_coupling_mosaic'] = DEV_COUPLINGS[0]
    params['dev_coupling_hybrid'] = DEV_COUPLINGS[1]
    params['dev_coupling_concerted'] = DEV_COUPLINGS[2]
    params['num_generations_to_env_switch'] = 10
    params['num_episodes'] = 10
    params['num_iterations'] = 100
    params['cost_range'] = range_params['cost_range']
    params['max_benefit_range'] = range_params['max_benefit_range']
    params['func_coupling_range'] = range_params['func_coupling_range']
    params['retain_history'] = True

    del(params['num_generations'])
    del(params['dev_coupling'])
    del(params['cost'])
    del(params['max_benefit'])
    del(params['func_coupling'])

    # total_population = params['num_critters']*len(DEV_COUPLINGS)

    for lifespan in [3]:
        for num_offspring in [1]:
            params['lifespan'] = lifespan
            params['num_offspring'] = num_offspring
            results, history = evolve_and_compare_mutating_populations_with_variable_environment(**params)
            filename = 'long_history_var_env_%s_lifespan_%d_offspring_%d.csv' % \
                            (range_params['name'], lifespan, num_offspring)
            keys = DEV_COUPLINGS
            save_history_to_csv(filename, keys, history, params['num_generations_to_env_switch'])


if __name__ == '__main__':
    print("generate_mosaicism_plots_for_homogeneous_populations")
    generate_mosaicism_plots_for_homogeneous_populations()
    print("generate_competition_plots")
    generate_competition_plots()
    print("generate_competition_plots_specific_environments")
    generate_competition_plots_specific_environments()
    print("generate_variable_environment_plots")
    generate_variable_environment_plots(NORMAL_RANGE)
    # generate_variable_environment_plots(EXTREME_RANGE)
    print("generate_variable_environment_long_evolution_data")
    generate_variable_environment_long_evolution_data(NORMAL_RANGE)
