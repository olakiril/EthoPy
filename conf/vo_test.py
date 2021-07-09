from Stimuli.SmellyObjects import *
from Experiments.Match2Sample import *
from Behaviors.MultiPort import *

# define session parameters
session_params = {
    'trial_selection'    : 'staircase',
    'start_time'         : '08:00:00',
    'stop_time'          : '22:00:00',
    'min_reward'         : 100,
    'max_reward'         : 3000,
    'bias_window'        : 5,
    'staircase_window'   : 10,
    'stair_up'           : 0.7,
    'stair_down'         : 0.6,
    'noresponse_intertrial': True,
}

exp = Experiment()
exp.setup(logger, MultiPort, session_params)
vo_conds = []
v_conds = []
o_conds = []

# define stimulus conditions
odor_ratios = {2: [(100, 0)],
               1: [(0, 100)]}
objects = {1: 'obj4v6',
           2: 'obj3v6'}
v_dur = 4000
o_dur = 500

trial_params = {
    'difficulty'            : 0,
    'timeout_duration'      : 6000,
    'trial_duration'        : 5000,
    'intertrial_duration'   : 500,
    'init_duration'         : 100,
    'delay_duration'        : 500,
    'reward_amount'         : 3,
}

v_params = {
    'clip_number'           : 1,
    'skip_time'             : [0],
    'static_frame'          : False,
    'movie_duration'        : 4000,
}

o_params = {
    'odorant_id'            : (1, 3),
    'delivery_port'         : (1, 2),
    'odor_duration'         : 500
}

for port in [1, 2]:
    vo_conds += exp.make_conditions(stim_class=SmellyObjects(), conditions={**trial_params, **o_params, **v_params,
                          'reward_port': port,
                          'response_port': port,
                          'movie_name': objects[port],
                          'dutycycle': odor_ratios[port]})
    o_conds += exp.make_conditions(stim_class=SmellyObjects(), conditions={**trial_params, **o_params,
                          'reward_port': port,
                          'response_port': port,
                          'movie_name': objects[port],
                          'dutycycle': odor_ratios[port],
                          'clip_number': 1,
                          'skip_time': 0,
                          'static_frame': False,
                          'movie_duration': 0})
    v_conds += exp.make_conditions(stim_class=SmellyObjects(), conditions={**trial_params, **v_params,
                          'port': port,
                          'movie_name': objects[port],
                          'odorant_id': (1, 3),
                          'delivery_port': (1, 2),
                          'dutycycle': (0, 0),
                          'odor_duration': 0})

conditions = vo_conds + v_conds + o_conds

# run experiments
exp.push_conditions(conditions)
exp.start()

