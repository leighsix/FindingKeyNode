import random
import numpy as np
import Setting_Simulation_Value
import InterconnectedLayerModeling
import networkx as nx

class KFDecisionDynamics:
    def __init__(self):
        self.B_COUNT = 0

    def B_layer_dynamics(self, setting, inter_layer, v, node_i_names):  # B_layer 다이내믹스, 베타 적용 및 언어데스 알고리즘 적용
        prob_v_list = []
        for node_i in range(setting.A_node, setting.A_node+setting.B_node):
            neighbors = np.array(sorted(nx.neighbors(inter_layer.two_layer_graph, node_i)))
            neighbor_state = []
            for neighbor in neighbors:
                neighbor_state.append(inter_layer.two_layer_graph.nodes[neighbor]['state'])
            neighbor_array = np.array(neighbor_state)
            same_orientation = int(np.sum(neighbor_array * inter_layer.two_layer_graph.nodes[node_i]['state'] > 0))
            opposite_orientation = len(neighbors) - same_orientation
            if opposite_orientation == 0:
                prob_v = 0
            else:
                if v == 0:
                    prob_v = 0
                else:
                    prob_v = (opposite_orientation / len(neighbors)) ** (1 / v) * \
                                (len(neighbors) / opposite_orientation)
            z = random.random()
            if z < prob_v:
                for node_i_name in node_i_names:
                    if inter_layer.two_layer_graph.nodes[node_i]['name'] != node_i_name:
                        inter_layer.two_layer_graph.nodes[node_i]['state'] = \
                            -(inter_layer.two_layer_graph.nodes[node_i]['state'])
                        self.B_COUNT += 1
            prob_v_list.append(prob_v)
        prob_v_array = np.array(prob_v_list)
        return inter_layer, prob_v_array


if __name__ == "__main__":
    print("DecisionDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    state = 0
    for i in range(setting.A_node, setting.A_node+setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    decision = KFDecisionDynamics()
    for i in range(100):
        inter_layer = decision.B_layer_dynamics(setting, inter_layer, 0.3, ['A_0', 'A_1'])[0]
    state = 0
    for i in range(setting.A_node, setting.A_node+setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)


