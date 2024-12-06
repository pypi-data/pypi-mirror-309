import numpy as np
from scipy import stats
from scipy.special import expit
from .utils import *

class ConstantKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name
        self.dependencies = None
        self.value = kernel_params["value"]

    def predict(self, observation):
        return self.value

    def sample(self):
        return self.value

class MixedKernel:
    def __init__(self, var_name, kernel_params):

        kernel_mapping = {
            "poisson": PoissonKernel,
            "mixed_poisson": MixedPoissonKernel,
            "binomial": BinomialKernel,
            "uniform": UniformKernel,
            "linear": LinearKernel,
            "deterministic": DeterministicKernel,
            "constant": ConstantKernel,
        }

        self.var_name = var_name
        self.dependencies = None

        # Noise
        self.noise_type = None
        if "noise" in kernel_params.keys():
            self.noise_type = kernel_params["noise"]["type"]
            if "prob" in kernel_params["noise"].keys():
                self.noise_prob = kernel_params["noise"]["prob"]
            else:
                self.noise_prob = None

        self.kernel_params = kernel_params
        self.kernels = []
        for kernel in kernel_params["kernels"]:
            kernel_type = kernel["type"]

            self.kernels.append(
                kernel_mapping[kernel_type](var_name, kernel)
            )

        self.mixed_probs = kernel_params["mixed_probs"]

    def predict(self, observation):

        # Add stochastic term
        if self.noise_type == "random":
            coin = stats.binom.rvs(n = 1, p = self.noise_prob)
            if coin:
                return self.sample()

        # sample kernel
        kernel_idx = np.random.choice(
            a = list(range(len(self.kernels))),
            p = self.mixed_probs)

        # get kernel
        kernel = self.kernels[kernel_idx]

        return kernel.predict(observation)

    def sample(self):
        return self.kernels[0].sample()

class DeterministicKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name
        self.dependencies = None
        self.terms = kernel_params["terms"]
        self.tree = kernel_params["tree"]
        self.domain = kernel_params["domain"]

    def predict(self, observation):
        for leaf in self.tree:
            correct_leaf = True

            for lag in set(leaf) - set(["output"]):
                for var in leaf[lag]:
                    obs_var_val = observation[lag][var]
                    leaf_var_val = leaf[lag][var]

                    if obs_var_val != leaf_var_val:
                        correct_leaf = False

            if not correct_leaf:
                continue

            # if observation[0]["DE"] == 1:
            #     print(f"{observation=}")
            #     print(f"{leaf=}")
            #     print(f"{leaf["output"]=}")

            return leaf["output"]

        raise ValueError("No leaf match found.")

    def sample(self):
        return np.random.choice(self.domain)


class NormalKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name

    def pdf(self, x, observation):
        return stats.norm.pdf(x, 0, 1).item()

    def predict(self, observation):
        return stats.norm.rvs(0, 1).item()

    def sample(self):
        return stats.norm.rvs(0, 1).item()

class LinearKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name

        self.sample_domain = kernel_params["sample_domain"]
        self.terms = kernel_params["terms"]

        self.indicator_terms = None
        if "indicator_terms" in kernel_params.keys():
            self.indicator_terms = kernel_params["indicator_terms"]

        self.lower_bound = None
        if "lower_bound" in kernel_params.keys():
            self.lower_bound = kernel_params["lower_bound"]

        self.upper_bound = None
        if "upper_bound" in kernel_params.keys():
            self.upper_bound = kernel_params["upper_bound"]

        self.intercept = 0
        if "intercept" in kernel_params.keys():
            self.intercept = kernel_params["intercept"]

        self.noise_type = None
        if "noise" in kernel_params.keys():
            self.noise_type = kernel_params["noise"]["type"]
            if "prob" in kernel_params["noise"].keys():
                self.noise_prob = kernel_params["noise"]["prob"]
            else:
                self.noise_prob = None

    def predict(self, observation):

        prod = linear_predictor(self.terms, self.intercept, observation)

        prod += indicator_predictor(self.indicator_terms, observation)

        # Add stochastic term
        if self.noise_type == "random":
            coin = stats.binom.rvs(n = 1, p = self.noise_prob)
            if coin:
                return self.sample()

        if self.lower_bound is not None:
            if prod < self.lower_bound:
                return self.lower_bound

        if self.upper_bound is not None:
            if prod > self.upper_bound:
                return self.upper_bound

        return prod

    def sample(self):
        return np.random.choice(self.sample_domain).item()

class UniformKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name
        self.domain = kernel_params["domain"]

        self.probs = None
        if "probs" in kernel_params.keys():
            self.probs = kernel_params["probs"]

    def predict(self, observation):
        value = np.random.choice(self.domain, p=self.probs).item()
        return value

    def sample(self):
        value = np.random.choice(self.domain).item()
        return value

class PoissonKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name
        self.terms = kernel_params["terms"]

        if "indicator_terms" in kernel_params.keys():
            self.indicator_terms = kernel_params["indicator_terms"]
        else:
            self.indicator_terms = []

        # capacity limit
        self.limit_value = None
        self.limit_variables = None
        if "limit" in kernel_params.keys():
            self.limit_value = kernel_params["limit"]["value"]
            self.limit_variables = kernel_params["limit"]["variables"]

        if "intercept" in kernel_params.keys():
            self.intercept = kernel_params["intercept"]
        else:
            self.intercept = 0

        self.noise_type = None
        if "noise" in kernel_params.keys():
            self.noise_type = kernel_params["noise"]["type"]
            if "prob" in kernel_params["noise"].keys():
                self.noise_prob = kernel_params["noise"]["prob"]
            else:
                self.noise_prob = None

    def predict(self, observation):
        mu = self._get_mu(observation)

        # print(f"{observation=}")
        # print(f"{mu=}")

        output = stats.poisson.rvs(mu)

        # Add stochastic term
        if self.noise_type == "random":
            coin = stats.binom.rvs(n = 1, p = self.noise_prob)
            if coin:
                return self.sample()

        if self.limit_value:
            current_value = 0
            if self.limit_variables:
                for lag in self.limit_variables:
                    for variable in self.limit_variables[lag]:
                        current_value += observation[lag][variable]

            if current_value + output > self.limit_value:
                return self.limit_value - current_value

        return output

    def _get_mu(self, observation):

        prod = linear_predictor(self.terms, self.intercept, observation)

        prod += indicator_predictor(self.indicator_terms, observation)

        return np.exp(prod)

    def sample(self):
        if self.limit_value:
            return np.random.choice(range(self.limit_value + 1)).item()
        else:
            return np.random.choice(range(10)).item()

class BinomialKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name

        self.dim = kernel_params["dim"]
        self.offset = 0
        if "offset" in kernel_params.keys():
            self.offset = kernel_params["offset"]
        self.terms = kernel_params["terms"]

        if "intercept" in kernel_params.keys():
            self.intercept = kernel_params["intercept"]
        else:
            self.intercept = 0

        if "noise" in kernel_params.keys():
            self.noise_type = kernel_params["noise"]["type"]
            if "prob" in kernel_params["noise"].keys():
                self.noise_prob = kernel_params["noise"]["prob"]
            else:
                self.noise_prob = None
        else:
            self.noise_type = None

    def pdf(self, x, observation):
        probs = self._get_p(observation)
        return stats.binom.pmf(x, self.dim - 1, probs).item()

    def predict(self, observation):

        # Add stochastic term
        if self.noise_type == "random":
            coin = stats.binom.rvs(n = 1, p = self.noise_prob)
            if coin:
                return self.sample()

        probs = self._get_p(observation)

        output = stats.binom.rvs(n = self.dim - 1, p = probs)

        return self.offset + output

    def _get_p(self, observation):

        if self.terms is None:
            return 0.5

        prod = linear_predictor(self.terms, self.intercept, observation)

        return expit(prod)

    def sample(self):
        output = np.random.choice(range(self.dim)).item()
        return self.offset + output

class MixedPoissonKernel:
    def __init__(self, var_name, kernel_params):
        self.var_name = var_name

        # demand
        self.d_terms = kernel_params["demand"]["terms"]
        self.d_constant = kernel_params["demand"]["constant"]
        self.d_intercept = kernel_params["demand"]["intercept"]            

        self.d_shock_prob = kernel_params["demand"]["shock"]["prob"]
        self.d_shock_value = kernel_params["demand"]["shock"]["value"]

        # success prob
        self.p_terms = kernel_params["success_prob"]["terms"]
        self.p_constant = kernel_params["success_prob"]["constant"]
        self.p_intercept = kernel_params["success_prob"]["intercept"]            

        # capacity limit
        self.limit_value = kernel_params["limit"]["value"]
        self.limit_variables = kernel_params["limit"]["variables"]

        # noise
        if "noise" in kernel_params.keys():
            self.noise_type = kernel_params["noise"]["type"]
            self.noise_prob = kernel_params["noise"]["prob"]

    def predict(self, observation):

        # Get distribution parameters
        d = self._get_expected_demand(observation)
        p = self._get_prob_of_rejection(observation)
        r = p / (1 - p) * d

        lam = stats.gamma.rvs(a = r, scale = (1 - p) / p)

        l = stats.poisson.rvs(lam)

        if self.noise_type == "random":
            if stats.bernoulli.rvs(self.noise_prob):
                l = self.sample()

        # print(f"{d=}, {p=}, {r=}, {l=}")

        remaining_value = self.remaining_value(observation)

        if remaining_value < l:
            return max(remaining_value, 0)

        return l

    def remaining_value(self, observation):
        remaining_value = self.limit_value

        if self.limit_variables is None:
            return remaining_value

        for lag in self.limit_variables.keys():
            for variable in self.limit_variables[lag]:
                remaining_value -= observation[lag][variable]

        return remaining_value
 
    def _get_expected_demand(self, observation):
        if stats.bernoulli.rvs(self.d_shock_prob):
            d = self.d_shock_value
        else:
            prod = linear_predictor(self.d_terms, self.d_intercept, observation)
            d = self.d_constant * np.exp(prod)

        return d

    def _get_prob_of_rejection(self, observation):
        prod = linear_predictor(self.p_terms, self.p_intercept, observation)

        p = 1 / (1 + self.p_constant * np.exp(prod))

        return p
    
    def sample(self):
        return np.random.choice(range(self.limit_value + 1))