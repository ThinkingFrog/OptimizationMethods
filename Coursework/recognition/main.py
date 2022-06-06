import numpy as np

from tabulate import tabulate

from recognition.launcher import launch


def main():
    exp_count = 5

    verbose = False
    graphical = False
    plot_rows = 3
    plot_cols = 4

    scores_table = {'SMO': {}}

    scores_table['SMO']['10cl'] = []
    scores_table['SMO']['2cl'] = []

    scores_table['IP'] = {'10cl': [], '2cl': []}
    scores_table['SLSQP'] = {'10cl': [], '2cl': []}
    for method in ('SMO', 'IP', 'SLSQP'):
        for convert_classes in (False, True):
            for _ in range(exp_count):
                score = launch(method, convert_classes, verbose, graphical, plot_rows, plot_cols)
                scores_table[method]['2cl' if convert_classes else '10cl'].append(score)

    headers = ['', '10 classes', '2 classes']
    tables = {'SMO': list(), 'IP': list(), 'SLSQP': list()}

    for method in ('SMO', 'IP', 'SLSQP'):
        tables[method] = [[idx + 1, sc10, sc2] for idx, sc10, sc2 in zip(range(exp_count), scores_table[method]['10cl'], scores_table[method]['2cl'])] + \
        [['Mean', np.mean(scores_table[method]['10cl']), np.mean(scores_table[method]['2cl'])]] + \
        [['Median', np.median(scores_table[method]['10cl']), np.median(scores_table[method]['2cl'])]] + \
        [['Max', max(scores_table[method]['10cl']), max(scores_table[method]['2cl'])]]

    print("Accuracy score tables:\n")
    for method in ('SMO', 'IP', 'SLSQP'):
        print(f"Method: {method}")
        print(tabulate(tables[method], headers))
        print()
