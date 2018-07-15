import plotly
import plotly.graph_objs as go

plotly.offline.plot({
    go.Scatter(y=[2,3], x=[4,5], name='line')
