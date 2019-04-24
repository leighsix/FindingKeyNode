import numpy as np
import Setting_Simulation_Value
import InterconnectedLayerModeling
import KFInterconnectedDynamics
import MakingPandas
import CalculatingProperty

class KFRepeatDynamics:
    def __init__(self):
        self.kfinter_dynamics = KFInterconnectedDynamics.KFInterconnectedDynamics()
        self.mp = MakingPandas.MakingPandas()
        self.cal_property = CalculatingProperty.CalculatingProperty()

    def repeat_dynamics(self, setting, inter_layer, gamma, beta, node_i_name, fixed_node_state):
        node_number = node_i_name.split('_')[1]
        if node_number != 'N':
            node_number = int(node_number)
            inter_layer.two_layer_graph.node[node_number]['state'] = fixed_node_state
        Num_Data = self.kfinter_dynamics.interconnected_dynamics(setting, inter_layer, gamma, beta, node_i_name)
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
