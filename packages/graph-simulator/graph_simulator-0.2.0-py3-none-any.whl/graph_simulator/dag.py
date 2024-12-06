import numpy as np
import networkx as nx

from .kernels import \
    MixedKernel, \
    NormalKernel, \
    PoissonKernel, \
    MixedPoissonKernel, \
    BinomialKernel, \
    UniformKernel, \
    LinearKernel, \
    DeterministicKernel, \
    ConstantKernel

class DAG_Simulator:

    def __init__(self, specs):
        self.time_step = 0
        self.specs = specs
        self.kernels = {var: self._get_kernel(var, spec["kernel"]) for var, spec in specs.items()}
        self.G = nx.DiGraph()

    def _get_kernel(self, var_name, kernel_params):
        kernel_type = kernel_params["type"]
        kernel_mapping = {
            "mixed": MixedKernel,
            "normal": NormalKernel,
            "poisson": PoissonKernel,
            "mixed_poisson": MixedPoissonKernel,
            "binomial": BinomialKernel,
            "uniform": UniformKernel,
            "linear": LinearKernel,
            "deterministic": DeterministicKernel,
            "constant": ConstantKernel,
        }
        return kernel_mapping[kernel_type](var_name, kernel_params)

    def _extend_graph(self):
        for var_name in self.topological_order:
            node_name = f"{var_name}_{self.time_step}"
            self._add_variable(var_name, self.time_step)
            self.G.add_edges_from([(parent_node, node_name) for parent_node in self._get_parent_nodes(var_name, self.time_step)])

    def get_parent_values(self, child_node: str):
        var_name = self.G.nodes[child_node]["var_name"]
        dependencies = self.specs[var_name]["dependencies"]

        if dependencies is None:
            return np.array([])

        parent_values = {}
        for graph_parent in self.G.predecessors(child_node):
            # if var_name == "X":
            #     print(f"    {graph_parent=}")
            # print(f"    {self.G.nodes=}")
            # print(f"    {self.G.nodes[graph_parent]=}")
            # print(f"    {self.G.nodes[graph_parent]["value"]=}")

            # lag = int(child_node.split("_")[1]) - int(graph_parent.split("_")[1])
            parent_lag = self.time_step - self.G.nodes[graph_parent]["time"]
            parent_var_name = self.G.nodes[graph_parent]["var_name"]
            parent_value = self.G.nodes[graph_parent]["value"]

            if not parent_lag in parent_values.keys():
                parent_values[parent_lag] = {}

            parent_values[parent_lag][parent_var_name] = parent_value

        return parent_values

    def _add_variable(self, var_name, time_step):
        node_name = var_name + f"_{time_step}"
        node_offset = self.specs[var_name]["level_offset"]
        self.G.add_node(node_name, level = time_step + node_offset, var_name = var_name, time = time_step)

    def _get_parent_nodes(self, var_name, time_step):
        dependencies = self.specs[var_name]["dependencies"]

        if dependencies is None:
            return []

        parent_nodes = []
        for lag, parent_vars in dependencies.items():
            for parent_var_name in parent_vars:
                t_append = time_step - int(lag)
                if t_append < 0:
                    continue

                parent_name = parent_var_name + f"_{str(t_append)}"

                if parent_name in self.G:
                    parent_nodes.append(parent_name)
                else:
                    raise ValueError(f"Parent {parent_name} of {var_name} at time-step {time_step} is missing in graph!")

        return parent_nodes

    def _set_values(self):
        values = {}

        for var_name, kernel in self.kernels.items():
            node_name = f"{var_name}_{self.time_step}"
            parent_values = self.get_parent_values(node_name)
            node_value = kernel.predict(parent_values)
            self.G.nodes[node_name]['value'] = node_value
            values[var_name] = node_value

            # if var_name == "X":
            #     print(f"    {self.topological_order}")
            #     print(f"    {node_name=}")

            #     print(f"    {var_name=}", f"{parent_values=}")
            #     print(f"    {node_value=}")
            #     print("\n")

            # if var_name == "A1":
            #     print(f"    {var_name=}", f"{parent_values=}")
            #     print(f"    {node_value=}")
            #     print("\n")

            # if var_name == "A2":
            #     print(f"    {var_name=}", f"{parent_values=}")
            #     print(f"    {node_value=}")
            #     print("\n")

            # if var_name == "L1":
            # print(f"    {node_value=}")

            # if var_name == "A":
            #     print(f"{var_name=}", f"{parent_values=}")
            #     print(f"{node_value=}")
                # if node_value != 1:
                #     sys.exit()
            # print(f"    {node_name=}")

        return values
    
    def run(self, steps=100):
        """will use TimeLimit wrapper for truncation..."""
        self._init_graph()

        data = []
        for _ in range(steps):
            # Extend Graph (build all next time-step variables)
            self._extend_graph()

            # Set node values
            data.append(self._set_values())

            # Clean-up graph (remove all non-dependencies)
            self._clean_up_graph()

            # Move one time-step
            self.time_step += 1

        return data

    def _clean_up_graph(self):
        relevant_nodes = set()
        min_required_time_step = self.time_step

        for var_name in self.specs.keys():
            node_name = f"{var_name}_{self.time_step}"
            relevant_nodes.add(node_name)
            for parent_node in self.G.predecessors(node_name):
                parent_time_step = int(parent_node.split("_")[1])
                min_required_time_step = min(min_required_time_step, parent_time_step)
                relevant_nodes.add(parent_node)

        redundant_nodes = [node for node in self.G.nodes if int(node.split("_")[1]) < min_required_time_step and node not in relevant_nodes]
        self.G.remove_nodes_from(redundant_nodes)

    def _init_graph(self, steps=5):
        # NB: Need to do this in two steps, b/c we don't know 
        # topological order yet. 

        # Init values
        for time_step in range(steps):
            for var_name in self.specs.keys():
                node_name = f"{var_name}_{time_step}"
                self._add_variable(var_name, time_step)
                self.G.nodes[node_name]["value"] = self.kernels[var_name].sample()

        # Init edges
        for time_step in range(steps):
            for var_name in self.specs.keys():
                node_name = f"{var_name}_{time_step}"
                # print(f"{node_name=}, {self._get_parent_nodes(var_name, time_step)=}")
                self.G.add_edges_from([(parent_node, node_name) for parent_node in self._get_parent_nodes(var_name, time_step)])

            self.time_step += 1

        # Set topological order
        topological_list = [i for i in list(nx.topological_sort(self.G)) if i.split("_")[1] == str(self.time_step - 1)]
        self.topological_order = [i.split("_")[0] for i in topological_list]

        self.kernels = {key: self.kernels[key] for key in self.topological_order} # sort kernel dict
