import numpy as np

class RBF:
    def __init__(self, length_scale=1.0, length_scale_bounds=(1e-5, 10)):
        self.length_scale = length_scale
        self.length_scale_bounds = length_scale_bounds

    def __call__(self, X, Y=None):
        """
        Compute the Radial Basis Function (RBF) kernel matrix.

        Parameters
        ----------
        X : array-like, shape (n_samples_X, n_features)
            Input data for which the kernel matrix is computed.

        Y : array-like, shape (n_samples_Y, n_features), optional
            Optional input data. If None, the kernel matrix is computed
            for the same data as X. Defaults to None.
        """
        X = np.atleast_2d(X).astype(float)
        if Y is None:
            Y = X
        else:
            Y = np.atleast_2d(Y).astype(float)

        # Calculate the pairwise squared Euclidean distances
        dists = np.sum((X[:, np.newaxis, :] - Y[np.newaxis, :, :]) ** 2, axis=-1)
        # Compute the RBF kernel matrix
        K = np.exp(-0.5 * dists / self.length_scale ** 2)

        return K

