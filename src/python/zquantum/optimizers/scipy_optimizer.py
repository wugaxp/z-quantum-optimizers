from zquantum.core.interfaces.optimizer import Optimizer
import scipy

class ScipyOptimizer(Optimizer):

    def __init__(self, method, options={}):
        self.method = method
        self.options = options
        if "keep_value_history" not in self.options.keys():
            self.options["keep_value_history"] = False

    def minimize(self, cost_function, initial_params=None, callback=None):
        """
        Minimizes given cost function using functions from scipy.minimize.

        Args:
            cost_function(): python method which takes numpy.ndarray as input
            initial_params(np.ndarray): initial parameters to be used for optimization
            callback(): callback function. If none is provided, a default one will be used.
        
        Returns:
            optimization_results(scipy.optimize.OptimizeResults): results of the optimization.
        """
        history = []

        def default_callback(params):
            history.append({'params': params})
            if self.options["keep_value_history"]:
                value = cost_function(params)
                history[-1]['value'] = value
                print(f'Iteration {len(history)}: {value}', flush=True)
            else:
                print(f'iteration {len(history)}')
            print(f'{params}', flush=True)
        
        if callback is None:
            callback = default_callback

        result = scipy.optimize.minimize(cost_function,
                                        initial_params,
                                        method=self.method,
                                        options=self.options,
                                        callback=callback)

        result.opt_value = result.fun
        result.opt_params = result.x
        result.history = history
        if 'hess_inv' in result.keys():
            del result['hess_inv']
        return result
