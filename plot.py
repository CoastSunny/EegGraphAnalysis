
#Easy way to plot the connectivity matrix
import numpy as np
import matplotlib.pyplot as plt
r_con = con + con.T - np.diag(np.diag(con)) #I reflect the matrix
plt.imshow(r_con);
clb = plt.colorbar()
clb.ax.set_title('PLI')
plt.xlabel('Channels')
plt.show()
