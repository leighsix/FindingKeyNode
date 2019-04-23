import numpy as np
import Setting_Simulation_Value
import InterconnectedLayerModeling
import KFInterconnectedDynamics
import MakingPandas
import CalculatingProperty
import tqdm
from concurrent import futures


class KFRepeatDynamics:
    def __init__(self):
        self.kfinter_dynamics = KFInterconnectedDynamics.KFInterconnectedDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.cal_property = CalculatingProperty.CalculatingProperty()

    def repeat_dynamics_for_only_100steps_threading(self, setting, inter_layer, node_i_name, fixed_node_state):
        total_data = np.zeros(0)
        node_number = node_i_name.split('_')[1]
        if node_number != 'N':
            node_number = int(node_number)
            inter_layer.two_layer_graph.node[node_number]['state'] = fixed_node_state
        with futures.ProcessPoolExecutor(max_workers=5) as executor:
            to_do_map = {}
            for gamma_beta_tuple in setting.variable_list:
                gamma = gamma_beta_tuple[0]
                beta = gamma_beta_tuple[1]
                future = executor.submit(self.kfinter_dynamics.average_interconnected_dynamics_for_100steps, setting,
                                         inter_layer, gamma, beta, node_i_name)
                to_do_map[future] = gamma_beta_tuple
            done_iter = futures.as_completed(to_do_map)
            line = 0
            for future in done_iter:
                line += 1
                Num_Data = future.result()
                additional_array = self.mp.making_array_for_100steps(setting, Num_Data)
                final_array = self.cal_property.making_array_for_property(additional_array, inter_layer, node_i_name)
                if line == 1:
                    total_data = final_array
                elif line > 1:
                    total_data = np.vstack([total_data, final_array])
        return total_data

    def repeat_dynamics_for_only_100steps(self, setting, inter_layer, node_i_name, fixed_node_state):
        total_data = np.zeros(0)
        node_number = node_i_name.split('_')[1]
        if node_number != 'N':
            node_number = int(node_number)
            inter_layer.two_layer_graph.node[node_number]['state'] = fixed_node_state
        line = 0
        for gamma_beta_tuple in setting.variable_list:
            gamma = gamma_beta_tuple[0]
            beta = gamma_beta_tuple[1]
            line += 1
            Num_Data = self.kfinter_dynamics.average_interconnected_dynamics_for_100steps(setting, inter_layer, gamma, beta, node_i_name)
            additional_array = self.mp.making_array_for_100steps(setting, Num_Data)
            final_array = self.cal_property.making_array_for_property(additional_array, inter_layer, node_i_name)
            if line == 1:
                total_data = final_array
            elif line > 1:
                total_data = np.vstack([total_data, final_array])
        return total_data

    def repeat_dynamics(self, setting, inter_layer, gamma, beta, node_i_name, fixed_node_state):
        node_number = node_i_name.split('_')[1]
        if node_number != 'N':
            node_number = int(node_number)
            inter_layer.two_layer_graph.node[node_number]['state'] = fixed_node_state
        Num_Data = self.kfinter_dynamics.average_interconnected_dynamics(setting, inter_layer, gamma, beta, node_i_name)
        panda_db = self.mp.making_dataframe_per_step(setting, Num_Data)
        panda_db = self.cal_property.making_df_for_property(panda_db, inter_layer, node_i_name)
        return panda_db


if __name__ == "__main__":
    print("RepeatDynamics")
    setting = Setting_Simulation_Value.Setting_Simulation_Value()
    inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(setting)
    node_i_name = 'A_0'
    gamma = 0.5
    beta = 1.5
    fixed_node_state = 1
    repeat = KFRepeatDynamics()
    result = repeat.repeat_dynamics(setting, inter_layer, gamma, beta, node_i_name, fixed_node_state)
    print(result['gamma'])
