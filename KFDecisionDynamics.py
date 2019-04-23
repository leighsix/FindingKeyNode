import random
import Setting_Simulation_Value
import InterconnectedLayerModeling
import networkx as nx

class KFDecisionDynamics:
    def __init__(self):
        self.B_COUNT = 0

    def B_layer_dynamics(self, setting, inter_layer, beta, node_i_name):  # B_layer 다이내믹스, 베타 적용 및 언어데스 알고리즘 적용
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
            prob_beta = ((sum(opposite))/((external_edge_number)+(internal_edge_number)))**beta
            prob_beta_list.append(prob_beta)
            z = random.random()
            if z < prob_beta:
                if inter_layer.two_layer_graph.nodes[i + setting.A_node]['name'] != node_i_name:
                    inter_layer.two_layer_graph.nodes[i + setting.A_node]['state'] = \
                        -(inter_layer.two_layer_graph.nodes[i + setting.A_node]['state'])
                self.B_COUNT += 1
        prob_beta_mean = sum(prob_beta_list) / len(prob_beta_list)
        return inter_layer, prob_beta_mean



if __name__ == "__main__" :
    print("DecisionDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    state = 0
    for i in range(setting.A_node, setting.A_node+setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)
    decision = KFDecisionDynamics()
    for i in range(100):
        inter_layer = decision.B_layer_dynamics(setting, inter_layer, 1.5, 'B_0')[0]
    state = 0
    for i in range(setting.A_node, setting.A_node+setting.B_node):
        state += inter_layer.two_layer_graph.nodes[i]['state']
    print(state)


