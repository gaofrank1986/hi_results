import numpy as np
from matplotlib.pyplot import *


aa = np.loadtxt("new_body_result.txt")
bb = np.loadtxt("new_surface_result.txt")


r_b = bb[:,4] - bb[:,5]
r_a = aa[:,4] - aa[:,5]

r_b2 = abs(np.array(bb[:,4] - bb[:,5])/np.array(bb[:,5]))
r_a2 = abs(np.array(aa[:,4] - aa[:,5])/np.array(aa[:,5]))
subplot(211)
plot(range(len(r_a)),r_a)
plot(range(len(r_b)),r_b)
ylabel('Absolute Error')
title('Error Statistics for Surface')
subplot(212)
plot(range(len(r_a)),r_a2)
plot(range(len(r_b)),r_b2)
ylabel('Relative Error')
xlabel('Node Number')
show()


