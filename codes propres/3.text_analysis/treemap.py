import pandas as pd
import plotly.express as px


file_path = "/Users/inasnanat/Documents/resultats3_class.xlsx"
data = pd.read_excel(file_path)

cluster_counts = data['Class'].value_counts().reset_index()
cluster_counts.columns = ['Class', 'Count']

fig = px.treemap(cluster_counts,
    path=['Class'],
    values='Count',
    title="Distribution des classes dans une treemap",
    color='Count',
    color_continuous_scale='Viridis')

fig.show()