# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Wed Jul 24 2024

import numpy as np
import tensorflow as tf

from edelweiss.custom_clfs import NeuralNetworkClassifier


def test_constructor():
    clf = NeuralNetworkClassifier()
    assert clf.hidden_units == (64, 32)
    assert clf.learning_rate == 0.001
    assert clf.epochs == 10
    assert clf.batch_size == 32
    assert clf.loss == "auto"
    assert clf.activation == "relu"
    assert clf.activation_output == "auto"

    clf = NeuralNetworkClassifier(
        hidden_units=(128, 64),
        learning_rate=0.01,
        epochs=20,
        batch_size=64,
        loss="categorical_crossentropy",
        activation="tanh",
        activation_output="softmax",
    )
    assert clf.hidden_units == (128, 64)
    assert clf.learning_rate == 0.01
    assert clf.epochs == 20
    assert clf.batch_size == 64
    assert clf.loss == "categorical_crossentropy"
    assert clf.activation == "tanh"
    assert clf.activation_output == "softmax"


def test_build_model():
    clf = NeuralNetworkClassifier()
    clf.fit(np.random.rand(100, 10), np.random.randint(2, size=100))
    model = clf.model
    assert isinstance(model, tf.keras.Sequential)
    assert model.input_shape == (None, 10)
    assert model.output_shape == (None, 1)


def test_fit():
    clf = NeuralNetworkClassifier(epochs=5)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y)
    assert hasattr(clf, "model")
    assert isinstance(clf.model, tf.keras.Sequential)

    sample_weight = np.random.rand(100)
    clf.fit(X, y, sample_weight=sample_weight)
    assert hasattr(clf, "model")
    assert isinstance(clf.model, tf.keras.Sequential)


def test_early_stopping():
    clf = NeuralNetworkClassifier(epochs=50)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y, early_stopping_patience=1)
    assert hasattr(clf, "model")
    assert isinstance(clf.model, tf.keras.Sequential)


def test_predict():
    clf = NeuralNetworkClassifier(epochs=5)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y)
    predictions = clf.predict(X)
    assert len(predictions) == 100
    assert set(predictions).issubset(set(clf.classes_))


def test_predict_proba():
    clf = NeuralNetworkClassifier(epochs=5)
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)

    clf.fit(X, y)
    probabilities = clf.predict_proba(X)
    assert probabilities.shape == (100, 2)
    assert np.all(probabilities >= 0) and np.all(probabilities <= 1)
