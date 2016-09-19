from PulseGeneration import *
import numpy as np
import matplotlib.pyplot as plt

params1 = {'seed': 1,
          'frequency': 20.0,
          'shatter_frequency': 500.0,
          'fromLength': True,
          'length': 3,
          'amp_min': 0.1,
          'amp_max': 0.9,
          'onset': 0.1,
          'offset': 0.2}

params2 = {'seed': 1,
           'frequency': 20.0,
           'shatter_frequency': 500.0,
           'fromLength': True,
           'length': 3,
           'amp_min': 0.1,
           'amp_max': 0.9,
           'onset': 0.1,
           'offset': 0.2}

samp_rate = 30000

pulse1, t = noise_pulse(samp_rate, params1)
pulse2, t = noise_pulse(samp_rate, params2)

print(np.array_equal(pulse1, pulse2))

plt.figure()
plt.hold(True)
plt.plot(t, pulse1)
plt.plot(t, -pulse2)
plt.show()
