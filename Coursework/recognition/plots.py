import matplotlib.pyplot as plt


def title(y_pred, y_test, target_names, i):
    pred_name = target_names[int(y_pred[i])]
    exp_name = target_names[y_test[i]]
    return f"predicted: {pred_name}\nexpected:      {exp_name}"


def plot_gallery(images, titles, h, w, n_row=3, n_col=4):
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)

    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i], size=12)
        plt.xticks(())
        plt.yticks(())

    plt.show()
