import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_digits
    from sklearn.manifold import TSNE

    return TSNE, load_digits, plt


@app.cell
def _(load_digits):
    X, y = load_digits(return_X_y=True)
    return X, y


@app.cell
def _(X, plt):
    plt.imshow(X[0].reshape(8, 8))
    return


@app.cell
def _(TSNE, X, y):
    import plotly.express as px

    X_embedded = TSNE(n_components=3, perplexity=30).fit_transform(X)

    fig = px.scatter_3d(
        x=X_embedded[:, 0],
        y=X_embedded[:, 1],
        z=X_embedded[:, 2],
        color=y.astype(str),   # важно: как категории
    )

    fig.show()
    return (X_embedded,)


@app.cell
def _():
    from sklearn.multiclass import OneVsOneClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    return LogisticRegression, OneVsOneClassifier, train_test_split


@app.cell
def _(LogisticRegression, OneVsOneClassifier, X_embedded, train_test_split, y):
    X_train, X_test, y_train, y_test = train_test_split(X_embedded, y)
    classifier = OneVsOneClassifier(estimator=LogisticRegression())
    classifier.fit(X_train, y_train)
    return X_test, classifier, y_test


@app.cell
def _(X_test, classifier, y_test):
    from sklearn.metrics import accuracy_score

    acc = accuracy_score(classifier.predict(X_test), y_test)
    acc
    return


@app.cell
def _(X_embedded, classifier, plt, y):
    import numpy as np

    h = 0.05
    x_min, x_max = X_embedded[:, 0].min() - 1, X_embedded[:, 0].max() + 1
    y_min, y_max = X_embedded[:, 1].min() - 1, X_embedded[:, 1].max() + 1

    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, h),
        np.arange(y_min, y_max, h)
    )

    # предсказываем для каждой точки сетки
    Z = classifier.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # рисуем
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.3)
    plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=y, edgecolor="k", s=20)
    plt.title("Decision Boundary (OneVsOne + LogisticRegression)")
    plt.xlabel("Component 1")
    plt.ylabel("Component 2")
    plt.show()
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
