import Setting_Simulation_Value
import InterconnectedLayerModeling
import KFRepeatDynamics
import sqlalchemy
from multiprocessing import Pool


class KFChanging_Variable:
    def __init__(self):
        self.setting = Setting_Simulation_Value.Setting_Simulation_Value()
        self.inter_layer = InterconnectedLayerModeling.InterconnectedLayerModeling(self.setting)
        self.kfrepeat_dynamics = KFRepeatDynamics.KFRepeatDynamics()

    def calculate_and_input_database(self, setting_variable_list):
        engine = sqlalchemy.create_engine('mysql+pymysql://root:2853@localhost:3306/%s' % self.setting.database)
        p = setting_variable_list[1][0]
        v = setting_variable_list[1][1]
        print(p, v)  # 프로그램 잘 실행되고 있는지 확인을 위해서 프린트 실시
        panda_db = self.kfrepeat_dynamics.repeat_dynamics(self.setting, self.inter_layer, p, v)
        panda_db.to_sql(name='%s' % self.setting.table, con=engine, index=False, if_exists='append')

    def paralleled_work(self):
        workers = self.setting.workers
        setting_variable_list = self.making_setting_variable_list()
        with Pool(workers) as p:
            p.map(self.calculate_and_input_database, setting_variable_list)

    def making_setting_variable_list(self):
        setting_variable_list = []
        node_and_node_state_tuple_list = self.making_node_A_and_state_tuple_list()
        for tuple_for_node_and_state in node_and_node_state_tuple_list:
            for tuple_for_gamma_beta in self.setting.variable_list:
                setting_variable_list.append((tuple_for_node_and_state, tuple_for_gamma_beta))
        return setting_variable_list

    def making_node_list(self):
        A_node_list = ['A_N']
        B_node_list = ['B_N']
        for node_i in range(self.setting.A_node):
            node_i_name = 'A_%s' % node_i
            A_node_list.append(node_i_name)
        for node_i in range(self.setting.B_node):
            node_i_name = 'B_%s' % node_i
            B_node_list.append(node_i_name)
        return A_node_list, B_node_list

    def making_node_A_and_state_tuple_list(self):
        node_and_state_tuple_list = []
        A_node_list = self.making_node_list()[0]
        A_state_list = [-1, -2, +1, +2]
        for node_name in A_node_list:
            if node_name == 'A_N':
                node_and_state_tuple_list.append((node_name, +1))
            else:
                for state in A_state_list:
                    node_and_state_tuple_list.append((node_name, state))
        return node_and_state_tuple_list

    def making_node_B_and_state_tuple_list(self):
        node_and_state_tuple_list = []
        B_node_list = self.making_node_list()[1]
        B_state_list = [-1, +1]
        for node_name in B_node_list:
            if node_name == 'B_N':
                node_and_state_tuple_list.append((node_name, -1))
            else:
                for state in B_state_list:
                    node_and_state_tuple_list.append((node_name, state))
        return node_and_state_tuple_list


if __name__ == "__main__":
    print("Changing_Variable")
    changing_variable = KFChanging_Variable()
    # print(changing_variable.temporary_list2())
    changing_variable.paralleled_work()
    # changing_variable.paralleled_work_for_only_100steps()
    print("Operating end")


    #def paralleled_work(self):
    #    workers = self.SS.workers
    #    variable_list = self.SS.variable_list
    #    with concurrent.futures.ProcessPoolExecutor(workers) as executor:
    #          executor.map(self.calculate_and_input_database, variable_list)
