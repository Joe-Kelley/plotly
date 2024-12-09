# import plotly.graph_objects as go
# import numpy as np

# x = np.linspace(-2, 2, 50)
# y = np.linspace(-2, 2, 50)
# x, y = np.meshgrid(x, y)
# z = np.sin(np.sqrt(x**2 + y**2))

# fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
# fig.update_layout(title="3D Surface Plot", scene=dict(zaxis=dict(range=[-1, 1])))
# fig.show()


import plotly.express as px
import pandas as pd

df = px.data.gapminder()

fig = px.scatter(
    df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
    size="pop", color="continent", hover_name="country",
    log_x=True, size_max=60
)
fig.update_layout(title="Gapminder Over Time")
fig.show()