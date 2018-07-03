import plotly
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot
import plotly.graph_objs as go

plotly.offline.init_notebook_mode(connected=True)

plotly.offline.iplot({
    "data": [go.Scatter(z = [[1, 20, 30],
                          [20, 1, 60],
                          [30, 60, 1]])],
    "layout": go.Layout(title="basic-heatmap")
)}
