import plotly
import plotly.graph_objs as go

plotly.offline.plot({
    go.Scatter(​z=[[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]])
