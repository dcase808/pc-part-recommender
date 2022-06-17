from pulp import *
from .data import gpus, cpus

class Optimizer:
    def __init__(self):
        self.data = {}
        self.init_data()
    
    def init_data(self):
        self.data['cpus'] = [cpu['name'] for cpu in cpus]
        self.data['gpus'] = [gpu['name'] for gpu in gpus]
        self.data['cpu_price'] = {cpu['name']: cpu['price'] for cpu in cpus}
        self.data['gpu_price'] = {gpu['name']: gpu['price'] for gpu in gpus}
        self.data['cpu_perf'] = {cpu['name']: cpu['perf'] for cpu in cpus}
        self.data['gpu_perf'] = {gpu['name']: gpu['perf'] for gpu in gpus}    

    def run_optimalization(self, max_price):
        problem = LpProblem('problem', LpMaximize)

        use_cpu = LpVariable.dicts('use_cpu', self.data['cpus'], 0, 1, LpBinary)
        use_gpu = LpVariable.dicts('use_gpu', self.data['gpus'], 0, 1, LpBinary)

        problem += lpSum([self.data['cpu_perf'][i] * use_cpu[i] for i in self.data['cpus']]) \
            + lpSum([self.data['gpu_perf'][i] * use_gpu[i] for i in self.data['gpus']]), 'Total perfomance'

        problem += lpSum([self.data['cpu_price'][i] * use_cpu[i] for i in self.data['cpus']]) \
            + lpSum([self.data['gpu_price'][i] * use_gpu[i] for i in self.data['gpus']]) <= max_price, 'Max total price'

        problem += lpSum([use_cpu[i] for i in self.data['cpus']]) == 1, 'Only one CPU'
        problem += lpSum([use_gpu[i] for i in self.data['gpus']]) == 1, 'Only one GPU'

        status = problem.solve(PULP_CBC_CMD(msg=False))

        if LpStatus[status] == 'Optimal':
            chosen_parts = []
            for var in problem.variables():
                if var.varValue == 1:
                    chosen_parts.append(var.name)
            return chosen_parts
        else:
            return {
                'error': 'Cant build any PC with this budget'
            }