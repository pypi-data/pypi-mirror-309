import numpy as np


def _make_param(value, size=None):
    if size is None:
        return value
    if isinstance(size, (int, tuple)):
        return np.full(size, value)
    raise ValueError()


def gaussian_process(mean=0, std=1, dt=1, size=None):
    """
    Generator to produce vectorized Gaussian process.
    
    Parameters:
    - mean: Mean of the Gaussian process, can be a float or an array of shape (n,)
    - std: Standard deviation of the Gaussian process, can be a float or an array of shape (n,)
    - dt: Time step
    - size: Dimension of the vector. If None, yields a scalar; if an integer, yields an array of shape (size,)
    
    Yields:
    - x: Scalar or array of shape (size,) representing the current time step's Gaussian process value
    """
    # Convert scalar parameters to arrays if necessary
    mean = _make_param(mean, size)
    std = _make_param(std, size)
    
    scale = std * np.sqrt(dt)
    
    while True:
        x = np.random.normal(loc=mean, scale=scale, size=size)
        yield x


def ornstein_uhlenbeck_process(x0=0, mu=0, theta=1, sigma=1, dt=1, size=None):
    """ Generator to produce scaler or vectorized Ornstein-Uhlenbeck (OU) process.
    
    Parameters:
    - x0: Initial value, can be a float or an array of shape `size`
    - mu: Long-term mean, can be a float or an array of shape `size`
    - theta: Mean reversion speed, can be a float or an array of shape `size`
    - sigma: Volatility, can be a float or an array of shape `size`
    - dt: Time step
    - size: Dimension of the vector. If None, yields a scalar; if an integer, yields an array of shape `size`
    
    Yields:
    - x: Scalar or array of shape `shape` representing the current time step's OU process value
    """
    # Convert scalar parameters to arrays if necessary
    x0 = _make_param(x0, size)
    mu = _make_param(mu, size)
    theta = _make_param(theta, size)
    sigma = _make_param(sigma, size)

    x = x0
    sqrt_dt = np.sqrt(dt)
    
    while True:
        dw = sqrt_dt * np.random.normal(size=size)
        x = x + theta * (mu - x) * dt + sigma * dw
        yield x
