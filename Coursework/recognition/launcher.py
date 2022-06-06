from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

from mlfromscratch.supervised_learning import SupportVectorMachine as SVM
from mlfromscratch.utils.kernels import rbf_kernel

from recognition.utils import title, plot_gallery, convert_target
from recognition.slsqp import MaxMarginClassifier


def launch(
    method: str,
    convert_classes: bool = False, 
    verbose: bool = False, 
    graphical: bool = False, 
    plot_rows: int = 3, 
    plot_cols: int = 4
    ) -> int:

    """
    Args:
        method (str): Must be either 'SMO', 'IP' or 'SLSQP'
        convert_classes (bool, optional): Convert 10 classes to 2. Defaults to False.
        verbose (bool, optional): Print additional information. Defaults to False.
        graphical (bool, optional): Show plots. Defaults to False.
        plot_rows (int, optional): Amount of rows in plots. Defaults to 3.
        plot_cols (int, optional): Amount of columns in plots. Defaults to 4.

    Raises:
        ValueError: Incorrect value for 'method'

    Returns:
        int: Accuracy score
    """

    # Load dataset of 1800 graphical numbers
    digits = datasets.load_digits()
    n_samples, h, w = digits.images.shape

    # Debug info
    if verbose:
        print(f"Current method: {method}")
        print(f"Amount of pictures: {n_samples}")
        print(f"Array of features\n: {digits.data}")
        print(f"Array of corresponding labels: {digits.target}")

    # Set data and labels accordingly to current task
    X = digits.data
    if convert_classes:
        if verbose:
            print("Converting labels from 10 classes to 2")
        y = convert_target(digits.target)
    else:
        y = digits.target

    # Split data to train and test
    if verbose:
        print("Splitting data to train and test")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    # Select SVM Classifier
    if method == 'SMO':
        clf = svm.SVC(gamma=0.001, C=100)
    elif method == 'IP':
        clf = SVM(kernel=rbf_kernel, gamma=0.001, C=100)
    elif method == 'SLSQP':
        clf = MaxMarginClassifier()
    else:
        raise ValueError(f"Invalid value {method} for method")

    # Fitting the classifier
    if verbose:
        print("Fitting the classifier")
    clf.fit(X_train, y_train)

    # Predicting
    if verbose:
        print("Predicting")
    y_pred = clf.predict(X_test)

    # Metrics
    score = accuracy_score(y_test, y_pred)
    if verbose:
        print(f"Confusion matrix:\n{confusion_matrix(y_test, y_pred)}")
        print(f"Accuracy score: {score}")

    # Plots
    if graphical:
        prediction_titles = [title(y_pred, y_test, y, idx) for idx in range(y_pred.shape[0])]
        plot_gallery(X_test, prediction_titles, h, w, rows = plot_rows, cols = plot_cols)

    return score
