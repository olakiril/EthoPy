from Experiments.Passive import *
from Stimuli.Movies import *
from Behaviors.HeadFixed import *
import random

# define session parameters
session_params = {
    'setup_conf_idx'     : 2,
    'trial_selection'    : 'random',
}

exp = Experiment()
exp.setup(logger, HeadFixed, session_params)

conditions = []

# define stimulus conditions
objects = ('MadMax')

key = {
    'clip_number'        : list(range(10, 40)),
    'skip_time'          : [0],
    'movie_duration'     : 5000,
    'static_frame'       : False,
    'intertrial_duration': 500,
}

for object in objects:
    conditions += exp.make_conditions(stim_class=Movies(), conditions={**key, 'movie_name': object})

random.seed(0)
random.shuffle(conditions)

# run experiment
exp.push_conditions(conditions)
exp.start()
