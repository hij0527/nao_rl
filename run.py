#!/usr/bin/python2
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nao_rl'))

import nao_rl
env = nao_rl.make('NaoTracking')
env.run(timeout=10)
env.close()
nao_rl.destroy_instances()

