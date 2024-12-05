import calculator_179d.calculate_common_features as ccf
import numpy as np
import joblib
import pkg_resources

class proposed_naturalgas_179d():
        def __init__(self, calculator_user_inputs):
            self.bldg_type = calculator_user_inputs['building_type']
            self.climate_zone = calculator_user_inputs['climate_zone']
            self.hvac_system = calculator_user_inputs['hvac_system']
            self.proposed_naturalgas_model = self.read_proposed_model()


        # pick the sklearn model based on bldg type, climate zone and hvac_system
        def read_proposed_model(self):
            model_file = (
                'proposed_naturalgas_' +
                self.bldg_type.replace(' ','_') + '_' +
                self.hvac_system.replace(' ', '_') + '_'
                'CZ'+self.climate_zone +  '.pk'
            )

            model_path = pkg_resources.resource_filename(__name__, f"model_files/{model_file}")
            with open(model_path,'rb') as f:
                model = joblib.load(f)

            return model 


        # create input array used for model prediction
        def create_input_array(self, calculator_user_inputs):
            
            # calculated features - ua building, ACH infiltration, surface to volume ratio
            [cooling_cop,heating_cop] = ccf.calculate_cooling_and_heating_cop(
                calculator_user_inputs
            )
            [wh_ua_w_per_K, wh_eta_burner_final] = ccf.calculate_wh_ua_and_efficiency(
                calculator_user_inputs
            )
            ua_bldg = ccf.calculate_ua_bldg(calculator_user_inputs)
            ach_infiltration = ccf.calculate_ACH_infiltration(calculator_user_inputs)
            sa_to_vol_ratio = ccf.calculate_sa_to_vol_ratio(calculator_user_inputs)
            ext_wall_surface_area = ccf.calculate_ext_wall_surface_area(calculator_user_inputs)
            window_area = ccf.calculate_window_area(calculator_user_inputs)
            roof_area = ccf.calculate_roof_area(calculator_user_inputs)

            # create input array - same order as used during model development
            input_array = np.array(
                [[
                    calculator_user_inputs['number_of_floors'],
                    calculator_user_inputs['gross_floor_area'],
                    ua_bldg,
                    calculator_user_inputs['window_wall_ratio'],
                    calculator_user_inputs['window_shgc'],
                    ach_infiltration,
                    calculator_user_inputs['proposed_lpd'],
                    heating_cop,
                    sa_to_vol_ratio,
                    calculator_user_inputs['aspect_ratio'],
                    ext_wall_surface_area,
                    roof_area,
                    window_area,
                    calculator_user_inputs['wall_thermal_perf_type'],
                    calculator_user_inputs['window_u_factor'],
                    calculator_user_inputs['roof_thermal_perf_type'],
                    wh_eta_burner_final,
                    wh_ua_w_per_K
                ]]
            )

            return input_array


        # Predict annual electricity 179d
        def estimate_annual_naturalgas(self, calculator_user_inputs):
            #create input array for prediction
            input_array = self.create_input_array(calculator_user_inputs)
            # predict floor area normalized annualy electricity 179d
            proposed_naturalgas_179d_value = self.proposed_naturalgas_model.predict(
                input_array
            )[0][0]

            return proposed_naturalgas_179d_value