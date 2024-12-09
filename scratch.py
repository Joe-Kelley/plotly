import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Plotly
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species_id",
                 title="Iris Dataset Scatter Plot")
fig.show()


# Matplotlib
df = sns.load_dataset('iris')
sns.scatterplot(x="sepal_width", y="sepal_length", hue="species", data=df)
plt.show()
