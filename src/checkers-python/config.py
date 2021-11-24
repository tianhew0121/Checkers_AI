#c = 10
c = 4
debug = False
sim_count = 450  # together with simulation limit, help control system usage no matter what the size of the board is.
sim_minimum = 1
sim_scaler = 1
reset_counter = 100000
p_scaler = 1.0
p_shrink = 1
p_min = 1
simulation_scaler = 1
simulation_max = 35
simulation_limit = 5000   # Not necessaryly the higher this number the better the result. 
                        #Since we used AMAF H, making this value small might help select the 
                        # moves that leads to actually winning faster.
