import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data.
* **Python Libraries:** base64, pandas, streamlit
* **Data Source:** [Basketball-reference.com]
(https://www.https://www.basketball-reference.com/)
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year?', list(reversed(range(1950, 2020))))


# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) \
          + '_per_game'
    html = pd.read_html(url, header=0)
    dataFrame = html[0]
    raw = dataFrame.drop(dataFrame[dataFrame.Age == 'Age'].index)
    raw = raw.fillna(0)
    player_stats = raw.drop(['Rk'], axis=1)
    return player_stats


player_stats = load_data(selected_year)

sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team,
                                       sorted_unique_team)

unique_pos = ['C', 'PF', 'SF', 'SG', 'PG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

dataFrame_selected_team = player_stats[(player_stats.Tm.isin(selected_team)) &
                                       (player_stats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(dataFrame_selected_team.shape[0]) +
         ' rows and ' + str(dataFrame_selected_team.shape[1]) + 'columns')
st.dataframe(dataFrame_selected_team)


def fileDownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f' <a href="data:file/csv;base64, {b64}" ' \
           f'download ="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(fileDownload(dataFrame_selected_team), unsafe_allow_html=True)


# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header("Intercorrelation Matrix Heatmap")
    dataFrame_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7,5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()
