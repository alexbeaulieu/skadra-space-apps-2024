from algorithms.algorithm import Algorithm


class AlgorithmManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AlgorithmManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.algorithms = [] # List of algorithms
        
    def add_algorithm(self, algorithm: Algorithm):
        self.algorithms.append(algorithm)
        
    def get_algorithms(self):
        return self.algorithms
    
    def process(self, algorithm_name: str, data):
        algo = next((a for a in self.algorithms if a.name == algorithm_name), None)
        if algo is None:
            raise ValueError(f"Algorithm {algorithm_name} not found in the list of algorithms")
        return algo.process(data)
        