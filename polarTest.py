import matplotlib.pyplot as plt
import mplstereonet

fig, ax = mplstereonet.subplots()
strikes = [230,344,20,192,260,333,244,264,190,328,327,118,66,220,95,334,270]
dips = [65,83,45,45,50,84,48,84,45,85,70,40,63,72,60,65,72]
cax = ax.density_contourf(strikes, dips, measurement='poles')

ax.pole(strikes, dips)
ax.grid(kind='polar')
cb = fig.colorbar(cax)
cb.remove()
plt.show()