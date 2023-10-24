# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 18:55:02 2023

@author: stuar
"""

import streamlit as st
import pandas as pd
import numpy as np
from urllib.request import urlopen
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager


font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))


path = 'https://github.com/StuMacf89/FBref-Data-for-Streamlit-Application/raw/main/FBref%20Clean%20Streamlit.xlsx'
df = pd.read_excel(path)
#path = r'C:\Users\stuar\Documents\Fbref Clean Streamlit Filt.xlsx'
#df = pd.read_excel(path)

df['Defensive Index'] = (df['Rank_Defensive Duels SEPI'] + df['Rank_Aerial SEPI'] + df['Rank_p90_pmin_interceptions'] + df['Rank_p90_pmin_ball_recoveries'])/4
df['Attacking Index'] = (df['Rank_p90_pmin_Gls'] + df['Rank_p90_pmin_Ast'] + df['Rank_p90_pmin_shot_creating_actions_p90'] + df['Rank_Dribble SEPI'])/4
df['Defensive Index'] = (df['Rank_Defensive Duels SEPI'] + df['Rank_Aerial SEPI'] + df['Rank_p90_pmin_interceptions'] + df['Rank_p90_pmin_ball_recoveries'])/4
df['Passing Index'] = (df['Rank_Passing SEPI'] + df['Rank_p90_pmin_progressive_passes'] + df['Rank_p90_pmin_key_passes'] )/3

df = df.drop_duplicates(subset='Player', keep="first")
df = df.drop('Unnamed: 0', axis=1)
 
st.sidebar.header('Please Filter Here:')

position = st.sidebar.multiselect(
    'Select Position(s):',
    options = df['sub_position'].unique(),
    )
df = df[df['sub_position'].isin(position)]

age = st.sidebar.slider(
    'Select Maximum Age',
    df['Age'].min(),df['Age'].max()
)

df = df[df['Age'] < age]

matches_played = st.sidebar.slider(
    'Select Minimum Number of matches Played',
    df['matches_played'].min(),df['matches_played'].max()
)

df = df[df['matches_played'] > matches_played]

team_index = st.sidebar.slider(
    'Filter Team Ranking',
    df['Team Final League Ranking'].min(),df['Team Final League Ranking'].max()
)

df = df[df['Team Final League Ranking'] > team_index]

player_rank = st.sidebar.slider(
    'Select Minimum Player Rank/ Quality',
    df['Position Specific Index'].min(),df['Position Specific Index'].max() 
)

df = df[df['Position Specific Index'] > player_rank]

def_index = st.sidebar.slider(
    'How Defensive?',
    df['Defensive Index'].min(),df['Defensive Index'].max()
)

df = df[df['Defensive Index'] > def_index]

att_index = st.sidebar.slider(
    'How Attacking?',
    df['Attacking Index'].min(),df['Attacking Index'].max()
)

df = df[df['Attacking Index'] > att_index]

pass_index = st.sidebar.slider(
    'How Good in Possession?',
    df['Passing Index'].min(),df['Passing Index'].max()
)

df = df[df['Passing Index'] > pass_index]

df=df.set_index('Player')

player_select = st.sidebar.selectbox('Select Player to Visualise Attributes',df.index)

cols = ['Rank_Defensive Duels SEPI',
 'Rank_Aerial SEPI',
 'Rank_Passing SEPI',
 'Rank_p90_pmin_errors',
 'Rank_p90_pmin_ball_recoveries',
 'Rank_p90_pmin_Gls',
 'Rank_p90_pmin_Ast',
 'Rank_p90_pmin_shot_creating_actions_p90',
 'Rank_G-xG',
 'Rank_p90_pmin_interceptions',
 'Rank_p90_pmin_progressive_passes',
 'Rank_p90_pmin_dispossessed',
 'Rank_p90_pmin_errors.1',
 'Rank_p90_pmin_key_passes',
 'Rank_Dribble SEPI']

df[cols] = df[cols].round(2)

st.dataframe(df)


params = ["Goals",
"Assists","Shot Creating\nActions", "Goals Minus\nxG", "Dribbling\nAbility","Defensive\nDuels",
"Aerial\nAbility","Ball\nRecoveries","Interceptions", "Passing\nAbility","No of\nProgressive\nPasses","Key Passes",
"Errors","Dispossessed"]

n = player_select
values = [df['Rank_p90_pmin_Gls'][n],df['Rank_p90_pmin_Ast'][n],df['Rank_p90_pmin_shot_creating_actions_p90'][n],
          df['Rank_G-xG'][n],df['Rank_Dribble SEPI'][n],df['Rank_Defensive Duels SEPI'][n],
          df['Rank_Aerial SEPI'][n],df['Rank_p90_pmin_ball_recoveries'][n],df['Rank_p90_pmin_interceptions'][n],
          df['Rank_Passing SEPI'][n],df['Rank_p90_pmin_progressive_passes'][n],df['Rank_p90_pmin_key_passes'][n],
         df['Rank_p90_pmin_errors'][n],df['Rank_p90_pmin_dispossessed'][n]]

slice_colors = ["#cf9d1f"] * 5 + ['#13e83a'] *4 +['#0a69f0']*3 + ['#d60913']*2
text_colors = ["#000000"] * 5 + ['#000000'] * 4 +["#fffcfc"]*3 + ["#fffcfc"]*2

min_range = [0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0]
max_range = [1, 1, 1, 1, 1,1,1,1,1,1,1,1,1,1]
   
baker = PyPizza(
    params=params,                  # list of parameters
    background_color="#ffffff",     # background color
    straight_line_color="#EBEBE9",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=0,               # linewidth of last circle
    other_circle_lw=0,              # linewidth for other circles
    inner_circle_size=20,
    min_range = min_range,
    max_range = max_range            # size of inner circle
)

fig, ax = baker.make_pizza(
    values,                          # list of values
    figsize=(8, 8.5),                # adjust figsize according to your need
    color_blank_space="same",        # use same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.4,                 # alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#F2F2F2", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
    kwargs_params=dict(
        color="#000000", fontsize=11,
        fontproperties=font_normal.prop, va="center"
    ),                               # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=11,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                # values to be used when adding parameter-values
)

fig.text(
    0.515, 0.975, player_select, size=16,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

fig.text(
    0.515, 0.953,
    "Percentile Rank vs Players in Same Position | Seasons 2018-23",
    size=13,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

fig.text(
    0.28, 0.925, "Attacking", size=14,
    fontproperties=font_bold.prop, color="#000000"
)
fig.text(
    0.43, 0.925, "Defending", size=14,
    fontproperties=font_bold.prop, color="#000000"
)
fig.text(
    0.58, 0.925, "Passing", size=14,
    fontproperties=font_bold.prop, color="#000000"
)
fig.text(
    0.73, 0.925, "Errors", size=14,
    fontproperties=font_bold.prop, color="#000000"
)

fig.patches.extend([
    plt.Rectangle(
        (0.25, 0.9225), 0.025, 0.021, fill=True, color="#cf9d1f",
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.40, 0.9225), 0.025, 0.021, fill=True, color="#13e83a",
        transform=fig.transFigure, figure=fig
    ),plt.Rectangle(
        (0.55, 0.9225), 0.025, 0.021, fill=True, color="#0a69f0",
        transform=fig.transFigure, figure=fig
    ),plt.Rectangle(
        (0.70, 0.9225), 0.025, 0.021, fill=True, color="#d60913",
        transform=fig.transFigure, figure=fig
    )
])
    
st.pyplot(fig)





