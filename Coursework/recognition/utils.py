import matplotlib.pyplot as plt
import numpy as np

def title(y_pred, y_test, target_names, idx):
    if y_pred.max() == 1 and y_test.max() == 1 and target_names.max() == 1:
        pred_name = "Less or equal than 4" if int(y_pred[idx]) == 0 else "Greater or equal than 5"
        exp_name = "Less or equal than 4" if y_test[idx] == 0 else "Greater or equal than 5"
    else:
        pred_name = target_names[int(y_pred[idx])]
        exp_name = target_names[y_test[idx]]
    
    return f"predicted: {pred_name}\nexpected:      {exp_name}"


def plot_gallery(images, titles, h, w, rows = 3, cols = 4):
    plt.figure(figsize=(1.8 * cols, 2.4 * rows))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)

    for i in range(rows * cols):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())

    plt.show()


def convert_target(target):
    new_target = []

    for mark in target:
        if mark < 5:
            new_target.append(0)
        else:
            new_target.append(1)

    return np.array(new_target)