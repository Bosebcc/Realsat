import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot
import plotly.graph_objs as go

init_notebook_mode(connected=True)

trace = go.Heatmap(z=[[1, 20, 30],
                      [20, 1, 60],
                      [30, 60, 1]])
data=[trace]
plotly.offline.iplot(data, filename='basic-heatmap')
