import plotly.plotly as py
import plotly.graph_objs as go

trace = go.Heatmap(z=[[1, 20, 30],
                      [20, 1, 60],
                      [30, 60, 1]])
data=[trace]
py.iplot(data, filename='basic-heatmap', include_plotlyjs = false)
