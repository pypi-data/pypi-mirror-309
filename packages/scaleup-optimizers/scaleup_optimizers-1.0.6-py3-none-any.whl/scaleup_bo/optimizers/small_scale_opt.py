import numpy as np
from scipy.optimize import minimize
from skopt.space import Real, Integer, Categorical
from .base import BaseOptimizer
from ..acquisition_functions import ExpectedImprovement, ProbabilityOfImprovement, UpperConfidenceBound
from ..surrogate_models import SmallScaleGaussianProcess
from ..kernel import RBF
from ..scale import Scale
from ..utils import initialize_random_samples, ensure_scalar


class SmallScaleOptimizer(BaseOptimizer):
    def __init__(self, objective_func, search_space, acq_func='EI', gp=None, n_steps=10, n_initial_points=1, initial_points=None):
        """
        Initialize the SmallScaleOptimizer.

        Parameters
        ----------
        objective_func : callable
            The objective function to be minimized.
        
        search_space : list of tuples
            The bounds for each parameter in the optimization problem.
        
        acq_func : str, optional (default='EI')
            The acquisition function used to propose new points (e.g., 'EI' for Expected Improvement).
        
        gp : GaussianProcessRegressor or None, optional (default=None)
            A Gaussian Process model to be used as the surrogate. If None, a new GP is created.
        
        n_steps : int, optional (default=10)
            The number of optimization steps (must be greater than or equal to 10).
        
        n_initial_points : int, optional (default=1)
            The number of initial random points to sample.
        
        initial_points : list of points or None, optional (default=None)
            Initial points to start the optimization. If None, random points are generated.
        """

        if not callable(objective_func):
            raise ValueError("objective_func must be a callable function.")

        if not isinstance(search_space, list):
            raise ValueError("search_space must be a list.")
        if not all(isinstance(dim, (Real, Integer, Categorical)) for dim in search_space):
            raise ValueError("All elements in search_space must be instances of Real, Integer, or Categorical.")

        if acq_func not in ['EI', 'PI', 'UCB']:
            raise ValueError("acq_func must be one of 'EI', 'PI', or 'UCB'.")

        if not isinstance(n_steps, int) or n_steps <= 0:
            raise ValueError("set `n_steps` > 0")

        if n_initial_points <= 0 and not initial_points:
            raise ValueError("Either set `n_initial_points` > 0,"
                         " or provide `initial_points`")
        
        if initial_points is None:
            initial_points = []
        elif not isinstance(initial_points[0], list):
            initial_points = [initial_points]
        if not isinstance(initial_points, list):
            raise ValueError("`initial_points` should be a list, but got %s" % type(initial_points))
        
        if n_steps < 10:
            raise ValueError("n_steps must be greater than or equal to 10.")
        
        self.objective_func = objective_func
        self.search_space = search_space
        self.acq_func_type = acq_func
        self.acq_func = None
        self.n_steps = n_steps
        self.n_initial_points = n_initial_points
        self.initial_points = initial_points
        self.X_iters = None
        self.Y_iters = None
        self.best_params = None
        self.best_score = float('inf')
        self.gp = None
        self.scale = Scale(self.search_space)

        if gp is None:
            self.gp = SmallScaleGaussianProcess(kernel=RBF(1.0, (1e-5, 100)), alpha=0.1)
        else:
            self.gp = gp

        self.optimize()

    def propose_next_point(self):
        """
        Proposes the next point to evaluate in the parameter space.
        
        This function utilizes the acquisition function 
        to explore the search space and find the point that minimizes 
        the objective function by sampling points in the normalized 
        space and then optimizing the negative of acquisition function .
        
        Returns:
            np.ndarray: The proposed point in normalized space.
        """
        min_val = float('inf')
        min_x = None

        def min_obj(X):
            """
            Objective function for minimization.
            Computes the negative acquisition function to maximize improvement.
            """
            if self.acq_func_type == 'EI':
                self.acq_func = ExpectedImprovement()
            elif self.acq_func_type == 'PI':
                self.acq_func = ProbabilityOfImprovement()
            elif self.acq_func_type == 'UCB':
                self.acq_func = UpperConfidenceBound()
            else:
                raise ValueError("Invalid acquisition function: {}".format(self.acq_func))

            acquisition_value = self.acq_func.evaluation(X.reshape(1, -1), self.Y_iters, self.gp)

            return -acquisition_value 

        # Use normalized bounds
        bounds = [(0, 1) for _ in self.search_space]

        for _ in range(100):  # Sample 100 initial points for optimization
            x0 = np.random.uniform(0, 1, len(self.search_space))
            res = minimize(min_obj, x0=x0, bounds=bounds, method='L-BFGS-B')
            if res.fun < min_val:
                min_val = res.fun
                min_x = res.x

        return min_x

    def optimize(self):
        """
        Optimizes the Gaussian Process model to find the best parameters 
        using Bayesian optimization.

        This function initializes the optimizer with random samples, normalizes the samples, 
        and iteratively proposes new points for evaluation based on the 
        acquisition function until the specified number of calls is reached.
        """
        # Initialize with random samples
        if self.initial_points:
            self.X_iters = np.array(self.initial_points, dtype=object)
        else:
            self.X_iters = initialize_random_samples(self.n_initial_points, self.search_space)
        self.Y_iters = np.array([self.objective_func(x) for x in self.X_iters])

        # Normalize initial samples
        X_iters_norm = self.scale.normalize(self.X_iters)

        # Train the initial Gaussian Process model
        self.gp.fit(X_iters_norm, self.Y_iters)

        for _ in range(self.n_steps):
            X_next_norm = self.propose_next_point()

            X_next = self.scale.denormalize(X_next_norm.reshape(1, -1)).flatten()
            
            # Evaluate the objective function at the next point
            Y_next = ensure_scalar(self.objective_func(X_next))

            self.X_iters = np.vstack((self.X_iters, X_next))
            self.Y_iters = np.append(self.Y_iters, Y_next)

            X_iters_norm = self.scale.normalize(self.X_iters)

            # Optimize the hyperparameters of the Gaussian Process (length scale)
            self.gp.optimize_hyperparameters()

            # Update the GP model
            self.gp.fit(X_iters_norm, self.Y_iters)

        best_index = np.argmin(self.Y_iters)
        self.best_params = self.X_iters[best_index].tolist()
        self.best_score = self.Y_iters[best_index]

        return self

