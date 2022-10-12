# -*- coding: utf-8 -*-
"""EDA_capstone_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aLN9AeZKqP9iL7e1duPQ3GM2y49OJhSZ

# Analysis
Theme: Financial Inclusion
Source data: https://www.worldbank.org/en/publication/globalfindex
Target Submission: 12 October 2022

Hypothesis: GDP relates to the Financial Inclusion rate

Definition:
- Financial Inclusion
- Unbanked

Data needed:
- List of G20 countries
- Historical GDP
- Financial Inclusion rate

The fact to check:
The Global Findex shows the gap in financial inclusion across demographics, with women, the poor, youth, and rural residents at the greatest disadvantage.
- Gender: 55% of Men and 47% of Women have an account at a formal financial institution, worldwide.
- Age: Worldwide those aged 15-24 are 33% less likely to have an account and 40% less likely to have saved formally.
- Education: In developing economies, adults with tertiary education are more than twice as likely to have a formal account as those with primary education or less
- Income: in developing economies, the richest 20% of adults in the country are more than three times as likely to save in a formal financial institution as the poorest 20% of adults
- Residence: 35% of Urban Residents and 22% of Rural Residents have a formal account in low-income economies
"""

# Importing the library
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns

col1, col2 = st.columns([1,2])

with col1:
  st.markdown('![G20 Presidency of Indonesia](https://drive.google.com/uc?id=1-0FMsHCpv7pIwG0nlSyCI5FcAUKzNRmH)')

with col2:
  st.title('G20 Financial Inclusion')
  st.markdown("<h2 style='text-align: left; color: gray;'>GDP and demographics relation to the Financial Inclusion rate</h1>",
            unsafe_allow_html=True)


st.markdown('___')
st.caption('Streamlit App by <a href="https://github.com/nerudesu">Pradipta A. Suryadi</a>', unsafe_allow_html=True)


_ = """# Data Collection

## Get G20 Member country List

Fetch data from Wikipedia with pandas' read_html and turn into list.
"""

g20_member_source = 'https://en.wikipedia.org/wiki/G20'


@st.cache
def get_g20_member_list():
  data = pd.read_html(io=g20_member_source)[3]['Member'].tolist()
  return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading G20 Member country List data...')
# Load 10,000 rows of data into the dataframe.
g20_member_list = get_g20_member_list()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Fetched (using st.cache): G20 Member country List")

# g20_member_list

_ = """## Get WorldBank Data

### WorldBank data fetching

Fetch data from worldbank and put it into dataframe
"""

# worldbank_data_source = 'https://thedocs.worldbank.org/en/doc/6fa0abd1f7f266f7115adae07278eb97-0050062022/original/Databank-wide.xlsx'
worldbank_data_source = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXwoJAEWLKvOVKZTlNoNrCuH3j0Asiz5ysJdt5XYqF0YY3fWQv3H-NnJ6BcT39yw/pub?output=xlsx'

@st.cache
def get_worldbank_data_source():
  data = pd.read_excel(worldbank_data_source)
  return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading WorldBank data...')
# Load 10,000 rows of data into the dataframe.
databank = get_worldbank_data_source()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Fetched (using st.cache): WorldBank data")

# clone the returned value so we can freely mutate it.
df = databank.copy()


_ = """### Sneak peek into the data."""

# Dimension
# df.shape

_ = """Data sample"""

# df.head()

_ = """### Turn the first row into dictionary for later use

TODO: find parameter that relevan
"""

reference = df.iloc[0].to_dict()
# reference

_ = """Remove the first row because we already put it into the dict"""

df.drop(index=df.index[0],inplace=True)

# df

_ = """### Filter WorldBank data with G20 Country"""

df_g20 = df[df['countrynewwb'].isin(g20_member_list)]
# df_g20

_ = """#### Member list checking
We need to check whether country name on Wikipedia is the same as in the WorldBank data
"""

g20_member_data = df_g20['countrynewwb'].unique().tolist()
# g20_member_data

# len(g20_member_data)

_ = """ Only 17 out of 20? Find the differences!"""

not_in_list = []
for element in g20_member_list:
    if element not in g20_member_data:
        not_in_list.append(element)

# print(not_in_list)

_ = """#### Mapping and deletion

**Mapping**
*   South Korea = Korea, Rep.
*   Russia = Russian Federation

**Delete**

Eureopean Union --> We want to fetch only country data at this moment
"""

# Create mapping using dict
replace_map = {'South Korea' : 'Korea, Rep.', 'Russia' : 'Russian Federation'}

for key in replace_map:
  g20_member_list_new = [member.replace(key, replace_map[key]) for member in g20_member_list]
  g20_member_list = g20_member_list_new

g20_member_list_new = g20_member_list[:-1] # Delete EU using slicing
# g20_member_list_new

_ = """#### Creating a new data frame"""

df_g20_new = df[df['countrynewwb'].isin(g20_member_list_new)]
# df_g20_new

df_g20_new['countrynewwb'].nunique() # Check if number of country already correct

_ = """Get sample data for Indonesia"""

# df_g20_new[df_g20_new['countrynewwb'] == 'Indonesia'][['countrynewwb','year','account_t_d_1','fin1_t_d_1']]

_ = """Year data type is still in float, we need to cast it into integer on the next section

Check empty data for overview data column
"""

df_g20_new.isnull().sum()

_ = """# Data Preparation

## Casting year to integer
"""

df_g20_new = df_g20_new[df_g20_new['year'].notnull()].copy()

df_g20_new['year'] = df_g20_new['year'].astype('int')

# df_g20_new

_ = """# Data Visualization

## Create Pivot
"""

df_g20_pivot = pd.pivot_table(df_g20_new,
                              values='account_t_d',
                              index=['incomegroupwb21','countrynewwb'],
                              columns=['year'],
                              aggfunc='sum',
                              fill_value=None,
                              margins=False,
                              dropna=True,
                              margins_name='All',
                              observed=False,
                              sort=True)

# df_g20_pivot

# order=['High income','Upper middle income','Lower middle income']

# df_g20_pivot.loc[order].sort_values(by=2021, ascending=False)

# Clustering data row-wise and
# changing color of the map.
# sns.heatmap(df_g20_pivot.loc[order], annot=True, fmt='.4f', cmap="BuGn")


st.header('Overview')
st.write('Financial inclusion means that individuals and businesses have access to useful and affordable financial products and services that meet their needs – transactions, payments, savings, credit and insurance – delivered in a responsible and sustainable way.')
st.write('The Group of Twenty (G20) recognizes that financial inclusion is a key enabler in the fight against poverty.')

# map_scope = st.selectbox(label="Select scope", options=['World', 'USA', 'Europe', 'Asia', 'Africa', 'North America', 'South America'])

fig = px.choropleth(df_g20_new, locations="codewb",
                    color="incomegroupwb21", # lifeExp is a column of gapminder
                    color_discrete_map={'Lower middle income':'red',
                                        'Upper middle income':'Yellow',
                                        'High income':'Green'},
                    # animation_frame="year",
                    hover_name="countrynewwb", # column to add to hover information
                    hover_data=['incomegroupwb21'],
                    scope='world',
                    labels={'incomegroupwb21':'Income group'},
                    category_orders={'incomegroupwb21': ['High income', 'Upper middle income', 'Lower middle income']}
                    # color_continuous_scale=px.colors.sequential.Plasma
                    )

fig.update_layout(
    title = {
        'text':'Member countries in the G-20'
    },
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.5,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://en.wikipedia.org/wiki/G20">G20 - Wikipedia</a> | <a href="Global Findex database">Global Findex database</a>',
        showarrow = False
    )]
)

# fig.show()
# Plot!
st.plotly_chart(fig, use_container_width=True)
st.info('As we can see on the map, Indonesia still categorized on Lower middle income', icon="ℹ️")