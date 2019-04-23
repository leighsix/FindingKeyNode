import pandas as pd
import numpy as np
import InterconnectedLayerModeling
import Setting_Simulation_Value


class MakingPandas:
    def making_dataframe_per_step(self, setting, value_array):
        columns = ['p', 'v',  'prob_v',
                   'A_plus', 'A_minus', 'B_plus', 'B_minus',
                   'Layer_A_Mean', 'Layer_B_Mean', 'AS',
                   'A_total_edges', 'B_total_edges', 'change_count']
        df = pd.DataFrame(value_array, columns=columns)
        step = [i for i in range(0, setting.Limited_step+1)]
        df['Model'] = setting.MODEL
        df['Steps'] = step
        df['Structure'] = setting.Structure
        df['A_node_number'] = setting.A_node
        df['B_node_number'] = setting.B_node
        df['A_external_edges'] = setting.A_inter_edges
        df['B_external_edges'] = setting.B_inter_edges
        return df

    def making_df_for_100steps(self, setting, total_data):
        columns = ['p', 'v', 'Layer_A_Mean', 'Layer_B_Mean', 'AS', 'prob_v',
                   'A_plus', 'A_minus', 'B_plus', 'B_minus, '
                   'A_total_edges', 'B_total_edges', 'change_count',
                   'Steps', 'A_node_number', 'B_node_number', 'A_external_edges', 'B_external_edges',
                   'Un_A_node_state', 'A_Hub', 'A_Authority', 'A_Pagerank', 'A_Eigenvector', 'A_Degree',
                   'A_Betweenness', 'A_Closeness', 'A_Load', 'A_NumberofDegree', 'B_Hub', 'B_Authority',
                   'B_Pagerank', 'B_Eigenvector', 'B_Degree', 'B_Betweenness', 'B_Closeness', 'B_Load']
        df = pd.DataFrame(total_data, columns=columns)
        df['Model'] = setting.MODEL
        df['Structure'] = setting.Structure
        return df


    def making_array_for_100steps(self, setting, value_array):
        additional_array = np.array([100, setting.A_node, setting.B_node,
                                     setting.A_inter_edges, setting.B_inter_edges])
        new_array = np.concatenate([value_array, additional_array])
        return new_array


    def interacting_property(self, setting, inter_layer):
        property_A = []
        property_B = []
        for i in range(setting.A_node):
            property_A.append(inter_layer.two_layer_graph.nodes[i]['state'])
        for i in range(setting.A_node, setting.A_node + setting.B_node):
            property_B.append(inter_layer.two_layer_graph.nodes[i]['state'])
        judge_A = np.array(property_A)
        judge_B = np.array(property_B)

        A_plus = int(np.sum(judge_A > 0))
        A_minus = int(np.sum(judge_A < 0))
        B_plus = int(np.sum(judge_B > 0))
        B_minus = int(np.sum(judge_B < 0))
        layer_A_mean = int(np.sum(judge_A)) / setting.A_node
        layer_B_mean = int(np.sum(judge_B)) / setting.B_node
        average_state = ((layer_A_mean / setting.MAX) + layer_B_mean) / 2

        return A_plus, A_minus, B_plus, B_minus, layer_A_mean, layer_B_mean, average_state

if __name__ == "__main__":
    print("MakingPandas")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)

