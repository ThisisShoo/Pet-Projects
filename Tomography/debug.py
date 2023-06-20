from matplotlib import pyplot as plt

import config_fns

plt.plot(config_fns.Gaussian(0, 252))
plt.savefig("Intermediate Plots/filter.png")