import numpy as np
import networkx as nx
import Setting_Simulation_Value
import KFOpinionDynamics
import KFDecisionDynamics
import MakingPandas
import InterconnectedLayerModeling
import matplotlib
import Interconnected_Network_Visualization
matplotlib.use("Agg")


class KFInterconnectedDynamics:
    def __init__(self):
        self.kfopinion = KFOpinionDynamics.KFOpinionDynamics()
        self.kfdecision = KFDecisionDynamics.KFDecisionDynamics()
        self.mp = MakingPandas.MakingPandas()

    def average_interconnected_dynamics(self, setting, inter_layer, p, v, node_i_name):
        num_data = np.zeros([setting.Limited_step + 1, 16])
        for i in range(setting.Repeating_number):
            temp_inter_layer = inter_layer
            dynamics_result = self.interconnected_dynamics(setting, temp_inter_layer, p, v, node_i_name)
            num_data = num_data + dynamics_result
        Num_Data = num_data / setting.Repeating_number
        return Num_Data

    def average_interconnected_dynamics_for_100steps(self, setting, inter_layer, p, v, node_i_name):
        num_data = np.zeros(16)
        for i in range(setting.Repeating_number):
            temp_inter_layer = inter_layer
            dynamics_result = self.interconnected_dynamics_100steps_result_only(setting, temp_inter_layer, p, v, node_i_name)
            num_data = num_data + dynamics_result
        Num_Data = num_data / setting.Repeating_number
        return Num_Data

    def interconnected_dynamics_100steps_result_only(self, setting, inter_layer, p, v, node_i_name):
        step_number = 0
        prob_p = p
        while True:
            inter_layer = self.kfopinion.A_layer_dynamics(setting, inter_layer, prob_p, node_i_name)
            decision = self.kfdecision.B_layer_dynamics(setting, inter_layer, v, node_i_name)
            inter_layer = decision[0]
            prob_beta_mean = decision[1]
            step_number += 1
            if step_number >= setting.Limited_step:
                layer_state_mean = self.mp.layer_state_mean(setting, inter_layer)
                different_state_ratio = self.mp.different_state_ratio(setting, inter_layer)
                fraction_plus = self.mp.calculate_fraction_plus(setting, inter_layer)
                time_count = self.kfopinion.A_COUNT + self.kfdecision.B_COUNT
                array_value = np.array([layer_state_mean[0], layer_state_mean[1],
                                        fraction_plus[0], fraction_plus[1],
                                        prob_p, prob_beta_mean, different_state_ratio[0],
                                        different_state_ratio[1], different_state_ratio[2],
                                        len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                        self.mp.judging_consensus(setting, inter_layer),
                                        self.mp.counting_negative_node(setting, inter_layer),
                                        self.mp.counting_positive_node(setting, inter_layer), time_count, v])
                break
        self.kfopinion.A_COUNT = 0
        self.kfdecision.B_COUNT = 0
        return array_value

    def interconnected_dynamics(self, setting, inter_layer, p, v, node_i_name):
        total_value = np.zeros(16)
        step_number = 0
        prob_p = p
        while True:
            if step_number == 0:
                time_count = self.kfopinion.A_COUNT + self.kfdecision.B_COUNT
                prob_beta_mean = self.calculate_initial_prob_beta_mean(setting, inter_layer, beta)
                layer_state_mean = self.mp.layer_state_mean(setting, inter_layer)
                different_state_ratio = self.mp.different_state_ratio(setting, inter_layer)
                fraction_plus = self.mp.calculate_fraction_plus(setting, inter_layer)
                initial_value = np.array([layer_state_mean[0], layer_state_mean[1],
                                          fraction_plus[0], fraction_plus[1],
                                          prob_p, prob_beta_mean, different_state_ratio[0],
                                          different_state_ratio[1], different_state_ratio[2],
                                          len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                          self.mp.judging_consensus(setting, inter_layer),
                                          self.mp.counting_negative_node(setting, inter_layer),
                                          self.mp.counting_positive_node(setting, inter_layer), time_count, v])
                total_value = total_value + initial_value
            inter_layer = self.kfopinion.A_layer_dynamics(setting, inter_layer, prob_p, node_i_name)
            decision = self.kfdecision.B_layer_dynamics(setting, inter_layer, v, node_i_name)
            inter_layer = decision[0]
            prob_beta_mean = decision[1]
            step_number += 1
            layer_state_mean = self.mp.layer_state_mean(setting, inter_layer)
            different_state_ratio = self.mp.different_state_ratio(setting, inter_layer)
            fraction_plus = self.mp.calculate_fraction_plus(setting, inter_layer)
            time_count = self.kfopinion.A_COUNT + self.kfdecision.B_COUNT
            array_value = np.array([layer_state_mean[0], layer_state_mean[1],
                                    fraction_plus[0], fraction_plus[1],
                                    prob_p, prob_beta_mean, different_state_ratio[0],
                                    different_state_ratio[1], different_state_ratio[2],
                                    len(sorted(inter_layer.A_edges.edges)), len(inter_layer.B_edges),
                                    self.mp.judging_consensus(setting, inter_layer),
                                    self.mp.counting_negative_node(setting, inter_layer),
                                    self.mp.counting_positive_node(setting, inter_layer), time_count, v])
            total_value = np.vstack([total_value, array_value])
            if step_number >= setting.Limited_step:
                break
        self.kfopinion.A_COUNT = 0
        self.kfdecision.B_COUNT = 0
        return total_value

    def calculate_initial_prob_beta_mean(self, setting, inter_layer, v):
        prob_beta_list = []
        for i in range(setting.B_node):
            opposite = []
            external_edge_number = len(inter_layer.AB_neighbor[i])
            internal_edge_number \
                = len(sorted(nx.all_neighbors(inter_layer.two_layer_graph, i+setting.A_node))) - external_edge_number
            for j in range(internal_edge_number):
                a = inter_layer.two_layer_graph.nodes[i + setting.A_node]['state']
                b = inter_layer.two_layer_graph.nodes[sorted(nx.all_neighbors(inter_layer.two_layer_graph, i+setting.A_node), reverse=True)[j]]['state']
                if a * b < 0:
                    opposite.append(1)
            for j in range(external_edge_number):
                a = inter_layer.two_layer_graph.nodes[i + setting.A_node]['state']
                b = inter_layer.two_layer_graph.nodes[sorted(nx.all_neighbors(inter_layer.two_layer_graph, i+setting.A_node), reverse=False)[j]]['state']
                if a * b < 0:
                    opposite.append(1)
            prob_beta = (((sum(opposite))/((external_edge_number)+(internal_edge_number)))**(1/v))\
                        *((external_edge_number)+(internal_edge_number)/(sum(opposite)))
            prob_beta_list.append(prob_beta)
        prob_beta_mean = sum(prob_beta_list) / setting.B_node
        return prob_beta_mean

if __name__ == "__main__":
    print("InterconnectedDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    prob_p = 0.1
    beta = 20
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    state = 0
    for i in range(setting.A_node, setting.A_node + setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    inter_dynamics = KFInterconnectedDynamics()
    array = inter_dynamics.average_interconnected_dynamics(setting, inter_layer, prob_p, beta, 'A_0')
    # array = inter_dynamics.average_interconnected_dynamics_for_100steps(setting, inter_layer, prob_p, beta, 'A_0')
    print(array)
    state = 0
    for i in range(setting.A_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    state = 0
    for i in range(setting.A_node, setting.A_node + setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)




