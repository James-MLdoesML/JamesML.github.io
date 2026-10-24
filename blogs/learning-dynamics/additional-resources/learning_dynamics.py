"""Numerical helpers for the Training Dynamics primer. Requires NumPy only."""
import numpy as np


def loss_and_gradient(weights, gamma=0.0, target=1.0):
    """L = (prod(w)-target)^2/2 + gamma*sum(w^2), along the final axis.

    Products excluding each weight are computed without division, so zero
    weights (including the origin) are handled correctly.
    """
    w = np.asarray(weights, dtype=float)
    p = np.prod(w, axis=-1)
    left = np.concatenate((np.ones_like(w[..., :1]),
                           np.cumprod(w[..., :-1], axis=-1)), axis=-1)
    right = np.concatenate((np.cumprod(w[..., :0:-1], axis=-1)[..., ::-1],
                            np.ones_like(w[..., :1])), axis=-1)
    g = np.asarray(gamma)
    grad = (p - target)[..., None] * left * right + 2 * g[..., None] * w
    loss = 0.5 * (p - target)**2 + g * np.sum(w*w, axis=-1)
    return loss, grad


def gamma_star(N):
    """Saddle-node threshold for the positive balanced branch, N >= 3."""
    if N < 3:
        raise ValueError("gamma_star is for N >= 3; N=2 has threshold 1/2.")
    p = (N - 2) / (2 * N - 2)
    return 0.5 * p**((N - 2) / N) * (1 - p)


def _initial_weights(N, init):
    if not isinstance(N, (int, np.integer)) or N < 1:
        raise ValueError("N must be a positive integer.")
    w = np.full(N, float(init)) if np.ndim(init) == 0 else np.asarray(init, float).copy()
    if w.shape != (N,) or not np.all(np.isfinite(w)):
        raise ValueError("init must be a finite scalar or a length-N sequence.")
    return w


def _settling(times, outputs, reference, atol, rtol, eligible):
    """Last exit from a tolerance band, with final 10% inside it."""
    error = np.abs(outputs - reference)
    outside = error > atol + rtol * np.abs(reference)
    indices = np.arange(len(times))
    last_bad = np.max(np.where(outside, indices[:, None], -1), axis=0)
    settled = eligible & (last_bad < int(0.9 * (len(times) - 1)))
    next_index = np.minimum(last_bad + 1, len(times) - 1)
    return np.where(settled, times[next_index], np.nan)


def train(N=2, gamma=0.0, eta=0.01, init=0.1, target=1.0, *,
          steps=20000, atol=1e-4, rtol=1e-3, reference_output=None):
    """Simultaneous full-batch gradient descent; returns a trajectory dict.

    time = eta * step. loss excludes the additive constant of noisy data.
    settling_time is the last entrance into atol+rtol*abs(reference) of
    reference_output, remaining there for at least the final 10% of the run.
    Without a reference, use the final output, requiring a small final gradient.
    NaN means not settled within this finite budget, NOT infinite settling time.
    """
    if gamma < 0 or eta <= 0 or steps < 1:
        raise ValueError("Require gamma >= 0, eta > 0, steps >= 1.")
    w = _initial_weights(N, init)
    weights = np.empty((steps + 1, N))
    weights[0] = w
    stop = steps
    with np.errstate(over="ignore", invalid="ignore"):
        for k in range(steps):
            _, grad = loss_and_gradient(w, gamma, target)
            new_w = w - eta * grad  # both/all weights use the same old state
            if not np.all(np.isfinite(new_w)) or np.max(np.abs(new_w)) > 1e6:
                stop = k
                break
            w = new_w
            weights[k + 1] = w
    weights = weights[:stop + 1]
    output = np.prod(weights, axis=1)
    losses, gradients = loss_and_gradient(weights, gamma, target)
    times = eta * np.arange(stop + 1)
    complete = stop == steps
    ref = output[-1] if reference_output is None else float(reference_output)
    eligible = complete and (reference_output is not None or
                             np.linalg.norm(gradients[-1]) <= 1e-6)
    settling = _settling(times, output[:, None], np.array([ref]),
                         atol, rtol, np.array([eligible]))[0]
    return dict(time=times, weights=weights, output=output, loss=losses,
                gradient_norm=np.linalg.norm(gradients, axis=1),
                settling_time=float(settling), diverged=not complete)


def sweep(gammas, N=2, eta=0.01, init=0.1, target=1.0, *,
          steps=30000, atol=1e-4, rtol=1e-3, reference_outputs=None):
    """Independent runs for each gamma, vectorised across the sweep.

    Every run starts from init (no automatic continuation/warm start).
    Returns gamma, final_output, final_weights, settling_time, diverged and
    stationary. See train for the settling-time definition.
    """
    gs = np.asarray(gammas, float)
    if gs.ndim != 1 or gs.size == 0 or np.any(gs < 0) or not np.all(np.isfinite(gs)):
        raise ValueError("gammas must be a nonempty 1-D array of finite nonnegative values.")
    if eta <= 0 or steps < 1:
        raise ValueError("Require eta > 0 and steps >= 1.")
    w = np.tile(_initial_weights(N, init), (len(gs), 1))
    output = np.empty((steps + 1, len(gs)))
    output[0] = np.prod(w, axis=1)
    alive = np.ones(len(gs), bool)
    with np.errstate(over="ignore", invalid="ignore"):
        for k in range(steps):
            _, grad = loss_and_gradient(w, gs, target)
            new_w = w - eta * grad
            alive &= np.all(np.isfinite(new_w), axis=1) & (np.max(np.abs(new_w), axis=1) <= 1e6)
            w = np.where(alive[:, None], new_w, 0.0)
            output[k + 1] = np.where(alive, np.prod(w, axis=1), np.nan)
    _, grad = loss_and_gradient(w, gs, target)
    stationary = alive & (np.linalg.norm(grad, axis=1) <= 1e-6)
    ref = output[-1] if reference_outputs is None else np.broadcast_to(reference_outputs, gs.shape)
    times = eta * np.arange(steps + 1)
    settling = _settling(times, output, ref, atol, rtol,
                         stationary if reference_outputs is None else alive)
    return dict(gamma=gs, final_output=output[-1], final_weights=np.where(alive[:, None], w, np.nan),
                settling_time=settling, diverged=~alive, stationary=stationary)


def train_relu(x, y, init=(0.3, 0.2), eta=0.001, steps=10000):
    """Unregularised two-weight ReLU network, full batch; derivative(0)=0."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.shape != y.shape or x.ndim != 1 or x.size == 0:
        raise ValueError("x and y must be nonempty 1-D arrays of equal shape.")
    w = np.empty((steps + 1, 2)); w[0] = init
    losses = np.empty(steps + 1)
    for k in range(steps + 1):
        a, b = w[k]
        activation = np.maximum(b*x, 0)
        residual = a*activation - y
        losses[k] = 0.5*np.mean(residual**2)
        if k < steps:
            grad = np.array([np.mean(residual*activation),
                             np.mean(residual*a*x*(b*x > 0))])
            w[k+1] = w[k] - eta*grad
    return dict(time=eta*np.arange(steps+1), weights=w, loss=losses,
                imbalance=w[:, 0]**2-w[:, 1]**2)


def noisy_dataset(n=64, sigma=0.5, seed=0):
    """Fixed label noise, inputs normalised to empirical mean(x^2)=1."""
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    x /= np.sqrt(np.mean(x*x))
    y = x + sigma*rng.normal(size=n)
    return x, y, float(np.mean(x*y))


def soft_threshold(target, gamma):
    """Exact globally optimal output, valid for positive or negative targets."""
    target = np.asarray(target)
    return np.sign(target)*np.maximum(np.abs(target)-2*np.asarray(gamma), 0)
