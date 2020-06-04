import matplotlib.pyplot as plt
import csv

def plot_sizes(results, num_generations, num_components):
    plt.cla()
    xs = [x for x in range(num_generations)]
    ys = {
        'total': results['average_total_size'],
    }
    for i in range(num_components):
        ys['component %d' % (i+1)] = [l[i] for l in results['average_component_sizes']]

    for t in ys.keys():
        plt.plot(xs, ys[t], label=t)
    plt.legend()
    plt.show()


def plot_sizes_boxplot(filename, keys, values):
    plt.boxplot(values, labels=keys, showfliers=False)
    plt.ylim(-0.2, 7)
    plt.savefig(filename)
    plt.close()


def plot_populations_boxplot(filename, keys, values):
    plt.boxplot(values, labels=keys, showfliers=False)
    plt.ylim(-0.2, 1.2)
    plt.yticks([i/10 for i in range(0, 11, 1)])
    plt.savefig(filename)
    plt.close()


def save_boxplot_data_to_csv(filename, keys, values):
    with open(filename, 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file)
        data_writer.writerow(keys)
        values_zip = zip(*values)
        for row in values_zip:
            data_writer.writerow(row)


def save_history_to_csv(filename, keys, history, generations_per_env):
    with open(filename, 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file)
        for i, iteration in enumerate(history):
            data_writer.writerow(["Iteration #%d" % i])
            data_writer.writerow(["Env start at generation", "Cost", "Benefit A", "Benefit B", "Benefit C"])
            for j, env in enumerate(iteration["environments"]):
                data_writer.writerow([j * generations_per_env, env.cost, *env.benefits])
            data_writer.writerow(["Critter counts"])
            data_writer.writerow(keys)
            for episode in iteration["critter_counts"]:
                for generation in episode:
                    data_writer.writerow([generation.get(key, 0) for key in keys])


def save_history_of_dev_coupling_to_csv(filename, keys, history):
    with open(filename, 'w', newline='') as csv_file:
        data_writer = csv.writer(csv_file)
        for i, iteration in enumerate(history):
            row = []
            for episode in iteration["critter_counts"]:
                for generation in episode:
                    crit_count = 0
                    dev_coupling_count = 0
                    for key in keys:
                        crit_count += generation.get(key, 0)
                        dev_coupling_count += generation.get(key, 0) * key
                    row.append(dev_coupling_count / crit_count)
            data_writer.writerow(row)
