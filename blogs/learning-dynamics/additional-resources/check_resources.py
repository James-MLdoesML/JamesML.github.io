"""Run with: python check_resources.py"""
import numpy as np
from learning_dynamics import loss_and_gradient, train, sweep, gamma_star, noisy_dataset

def main():
    rng = np.random.default_rng(42)
    for N in (1, 2, 3, 4):
        for w in (rng.normal(size=N), np.zeros(N), np.r_[0., np.ones(N-1)]):
            gamma, target, h = .17, .8, 1e-6
            _, analytic = loss_and_gradient(w, gamma, target)
            numeric = np.array([(loss_and_gradient(w+e, gamma, target)[0]
                                 - loss_and_gradient(w-e, gamma, target)[0])/(2*h)
                                for e in h*np.eye(N)])
            np.testing.assert_allclose(analytic, numeric, atol=1e-7, rtol=1e-6)
    for _ in range(100):
        a, b = rng.normal(size=2)
        eta = .01
        g = a*b-1
        an, bn = np.array([a,b])-eta*loss_and_gradient([a,b])[1]
        np.testing.assert_allclose(an*an-bn*bn, (1-eta*eta*g*g)*(a*a-b*b), atol=1e-12)
    gs = np.array([0, .1, .3, .7])
    result = sweep(gs, steps=15000, init=.2, reference_outputs=np.maximum(1-2*gs, 0))
    np.testing.assert_allclose(result["final_output"], np.maximum(1-2*gs, 0), atol=1e-6)
    for i,g in enumerate(gs):
        single = train(gamma=g, steps=15000, init=.2)
        np.testing.assert_allclose(single["output"][-1], result["final_output"][i], atol=1e-12)
    exceptional = train(init=[.2,-.2], steps=15000)
    np.testing.assert_allclose(exceptional["weights"][-1], [0,0], atol=1e-8)
    origin = train(N=3, gamma=.1, init=0, steps=10)
    np.testing.assert_array_equal(origin["weights"], 0)
    assert abs(gamma_star(3)-.2362351968552887) < 1e-12
    x,y,target = noisy_dataset(seed=2026)
    np.testing.assert_allclose(np.mean(x*x), 1)
    for p in (.1,.5,1):
        actual=.5*np.mean((p*x-y)**2)
        predicted=.5*(p-target)**2+.5*(np.mean(y*y)-target**2)
        np.testing.assert_allclose(actual,predicted,atol=1e-12)
    unresolved = train(gamma=.49, init=.05, steps=10, reference_output=.02)
    assert np.isnan(unresolved["settling_time"])
    divergent = train(eta=10, init=2, steps=100)
    assert divergent["diverged"] and np.isnan(divergent["settling_time"])
    print("PASS: gradients (including zeros), imbalance update, scalar/batched agreement,")
    print("known equilibria, exceptional line, threshold, noisy loss and run status.")

if __name__ == "__main__":
    main()
