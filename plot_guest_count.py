import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

date = '20201229'
limit = 4

sns.set_style('whitegrid')
g = sns.catplot(data=h.loc[h['appearances'] >= limit], 
                y='guest', x='appearances', 
                kind='bar', 
                aspect=1.6, 
                color='gray')
g.ax.set_xlabel('In Lieu of Fun appearances (min {})\nthru {}'.format(limit, date))
g.ax.set_ylabel('')
plt.savefig('inof.png', dpi=300)
plt.show()
