
# Importing the libraries
import matplotlib.pyplot as plt
import pandas as pd

# reading the csv file
pdb_growth_data = open(".\\data\\metadata\\Data Export Growth.csv")
# protein data bank growth data
pdb_growth_df = pd.read_csv(pdb_growth_data)
# pdb_growth_df = pdb_growth_df.iloc[:-13, :]
pdb_growth_df = pdb_growth_df[pdb_growth_df.index % 2 == 0]
print(pdb_growth_df.head())

pdb_growth_df.plot(x="Year", y=["Total Number of Entries Available", "Number of Structures Released Annually"],
                   kind="bar", stacked=True, width=.75, figsize=(20, 16))
line_graph = pdb_growth_df.plot(x='Year',
                                y=["Total Number of Entries Available", "Number of Structures Released Annually"],
                                figsize=(20, 16), linewidth=6)
plt.title('PDB Statistics: Overall Growth of Released Structures and entries over the Years', fontsize=24)
plt.xlabel("Year", fontsize=20)
plt.legend(fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=17)
plt.ylabel("Number of Entries", fontsize=20)
plt.show()
