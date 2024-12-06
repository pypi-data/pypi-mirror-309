import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Dynamic Perspective Learning Framework
class PerspectiveLearning:
    def __init__(self, dataset, features, target, perspectives, learning_rate=0.01, epochs=500, gradient_clip_value=1.0):
        """
        Initialize the Perspective Learning framework.
        
        :param dataset: pd.DataFrame, the dataset with features and target.
        :param features: list, list of feature column names.
        :param target: str, target column name.
        :param perspectives: dict, dictionary of perspectives with feature indices.
        :param learning_rate: float, learning rate for training.
        :param epochs: int, number of epochs for training.
        :param gradient_clip_value: float, maximum value for gradient clipping.
        """
        self.dataset = dataset
        self.features = features
        self.target = target
        self.perspectives = perspectives
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.gradient_clip_value = gradient_clip_value
        
        # Scalers for normalization
        self.scaler_X = MinMaxScaler()
        self.scaler_y = MinMaxScaler()
        self._prepare_data()

    def _prepare_data(self):
        """Normalize features and target using MinMaxScaler."""
        X = self.dataset[self.features].values
        y = self.dataset[[self.target]].values
        self.X = self.scaler_X.fit_transform(X)
        self.y = self.scaler_y.fit_transform(y).flatten()

    def mse_loss(self, y_true, y_pred):
        """Mean Squared Error Loss."""
        return np.mean((y_true - y_pred) ** 2)

    def train_perspective(self, perspective):
        """
        Train a single perspective.
        
        :param perspective: dict, perspective details including weights and feature indices.
        :return: dict, updated perspective with refined weights and loss.
        """
        weights = perspective["weights"]
        feature_indices = perspective["features"]
        features = self.X[:, feature_indices]
        
        for _ in range(self.epochs):
            # Predictions
            predictions = np.dot(features, weights[:-1]) + weights[-1]  # Last weight is the bias
            
            # Compute loss
            loss = self.mse_loss(self.y, predictions)
            
            # Gradient Descent
            errors = predictions - self.y
            gradients = np.dot(features.T, errors) / len(self.y)
            bias_gradient = np.mean(errors)
            
            # Gradient Clipping
            gradients = np.clip(gradients, -self.gradient_clip_value, self.gradient_clip_value)
            bias_gradient = np.clip(bias_gradient, -self.gradient_clip_value, self.gradient_clip_value)
            
            # Update weights and bias
            weights[:-1] -= self.learning_rate * gradients
            weights[-1] -= self.learning_rate * bias_gradient
        
        perspective["weights"] = weights
        perspective["loss"] = loss
        return perspective

    def train(self):
        """Train all perspectives and identify the best one."""
        for name, perspective in self.perspectives.items():
            print(f"Training {name}...")
            self.perspectives[name] = self.train_perspective(perspective)
            print(f"{name} Loss: {self.perspectives[name]['loss']}")

        # Select the best perspective
        self.best_perspective = min(self.perspectives, key=lambda k: self.perspectives[k]["loss"])
        print(f"Best Perspective: {self.best_perspective}")
        self.refined_perspective = self.train_perspective(self.perspectives[self.best_perspective])
        print("\nRefined Perspective Weights:")
        print(self.refined_perspective["weights"])
        print(f"Refined Loss: {self.refined_perspective['loss']}")

    def predict(self, new_data):
        """
        Predict outcomes using the refined perspective.
        
        :param new_data: np.array, new input data.
        :return: np.array, predicted outcomes.
        """
        # Normalize new data
        new_data_normalized = self.scaler_X.transform(new_data)
        
        # Use the best perspective for prediction
        weights = self.refined_perspective["weights"]
        feature_indices = self.refined_perspective["features"]
        selected_features = new_data_normalized[:, feature_indices]
        predictions = np.dot(selected_features, weights[:-1]) + weights[-1]
        
        # Reverse normalization for output
        return self.scaler_y.inverse_transform(predictions.reshape(-1, 1)).flatten()