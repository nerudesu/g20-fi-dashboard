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
from millify import millify

st.set_page_config(
    page_title='G20 Financial Inclusion',
    page_icon=':earth_asia:'
)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        '![G20 Presidency of Indonesia](https://drive.google.com/uc?id=1-0FMsHCpv7pIwG0nlSyCI5FcAUKzNRmH)')

with col2:
    st.title('G20 Financial Inclusion')
    st.markdown("<h2 style='text-align: left; color: gray;'>GDP and demographics relation to the Financial Inclusion rate</h1>",
                unsafe_allow_html=True)


st.markdown('___')
st.caption('Streamlit App by <a href="https://github.com/nerudesu">Pradipta A. Suryadi</a>',
           unsafe_allow_html=True)


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
data_load_state = st.text('Loading Global Findex data...')
# Load 10,000 rows of data into the dataframe.
databank = get_worldbank_data_source()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Fetched (using st.cache): Global Findex data")

# clone the returned value so we can freely mutate it.
df = databank.copy()


# Get GDP data
# https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD
gdp_data_source = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT5VFhPjLMaR1IA6VsQn4RaSDqs7w-6rIqV-py3uLTLOQN0Zvs6N93EW11-t7d0sQ/pub?output=xlsx"


@st.cache
def get_gdp_data_source():
    data = pd.read_excel(gdp_data_source)
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading WorldBank data...')
# Load 10,000 rows of data into the dataframe.
gdp_data = get_gdp_data_source()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Fetched (using st.cache): WorldBank data")

# clone the returned value so we can freely mutate it.
df_gdp = gdp_data.copy()


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

df.drop(index=df.index[0], inplace=True)

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
replace_map = {'South Korea': 'Korea, Rep.', 'Russia': 'Russian Federation'}

for key in replace_map:
    g20_member_list_new = [member.replace(
        key, replace_map[key]) for member in g20_member_list]
    g20_member_list = g20_member_list_new

g20_member_list_new = g20_member_list[:-1]  # Delete EU using slicing
# g20_member_list_new

_ = """#### Creating a new data frame"""

df_g20_new = df[df['countrynewwb'].isin(g20_member_list_new)]
# df_g20_new

# Check if number of country already correct
df_g20_new['countrynewwb'].nunique()

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
                              index=['incomegroupwb21', 'countrynewwb'],
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
st.subheader('Financial Inclusion')
st.write('Financial inclusion means that individuals and businesses have access to useful and affordable financial products and services that meet their needs – transactions, payments, savings, credit and insurance – delivered in a responsible and sustainable way.')
st.write('The Group of Twenty (G20) recognizes that financial inclusion is a key enabler in the fight against poverty.')

# map_scope = st.selectbox(label="Select scope", options=['World', 'USA', 'Europe', 'Asia', 'Africa', 'North America', 'South America'])

fig_geo = px.choropleth(df_g20_new, locations="codewb",
                        color="incomegroupwb21",  # lifeExp is a column of gapminder
                        color_discrete_map={'Lower middle income': '#E15139',
                                            'Upper middle income': '#FCA121',
                                            'High income': '#37B96D'},
                        # animation_frame="year",
                        hover_name="countrynewwb",  # column to add to hover information
                        hover_data=['incomegroupwb21'],
                        scope='world',
                        labels={'incomegroupwb21': 'Income group'},
                        category_orders={'incomegroupwb21': [
                            'High income', 'Upper middle income', 'Lower middle income']}
                        # color_continuous_scale=px.colors.sequential.Plasma
                        )

fig_geo.update_layout(
    title={
        'text': 'Member countries in the G-20'
    },
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations=[dict(
        x=0.5,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://en.wikipedia.org/wiki/G20">G20 - Wikipedia</a> | <a href="https://www.worldbank.org/en/publication/globalfindex/Data">Global Findex database</a>',
        showarrow=False
    )]
)

# fig.show()
# Plot!
st.plotly_chart(fig_geo, use_container_width=True)
st.info('With its economy impacted by the pandemic, **Indonesia** went from upper-middle income to **lower-middle income** status as of **July 2021**.', icon="ℹ️")

st.header("GDP Per capita")
st.write('GDP per capita shows a country\'s GDP divided by its total population. This gives us a way of describing the average level of wealth per person in a country.')

# Create new DF
headers = df_gdp.iloc[2]
new_df_gdp = pd.DataFrame(df_gdp.values[3:], columns=headers)

# Melt df
new_df_gdp = new_df_gdp.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                             var_name="Year",
                             value_name="Value")

# Cast year into int
new_df_gdp = new_df_gdp[new_df_gdp['Year'].notnull()].copy()
new_df_gdp['Year'] = new_df_gdp['Year'].astype('int')

# Turkey is not on the list (writed as Turkiye)
new_df_gdp_replaced = new_df_gdp.replace(to_replace="Turkiye",
                                         value="Turkey")

new_df_gdp_filtered = new_df_gdp_replaced[new_df_gdp_replaced['Year'].isin([
                                                                           2011, 2014, 2017, 2021])]
new_df_gdp_filtered = new_df_gdp_filtered[new_df_gdp_filtered['Country Name'].isin(
    g20_member_list_new)]

# Merge data frame
df_merged = df_g20_new.merge(new_df_gdp_filtered, how='left', left_on=[
                             'countrynewwb', 'year'], right_on=['Country Name', 'Year'])

fig_gdp = px.scatter(df_merged,
                     x="Value",
                     y="account_t_d",
                     size="pop_adult",
                     color="incomegroupwb21",
                     color_discrete_map={'Lower middle income': '#E15139',
                                         'Upper middle income': '#FCA121',
                                         'High income': '#37B96D'},
                     animation_frame="year",
                     hover_name="countrynewwb",
                     labels={'incomegroupwb21': 'Income group', 'Value': 'GDP Per Capita',
                             'account_t_d': 'Financial Inclusion Rate'},
                     category_orders={'incomegroupwb21': [
                         'High income', 'Upper middle income', 'Lower middle income']},
                     log_x=True,
                     size_max=60)

fig_gdp.update_layout(
    title={
        'text': 'Member countries in the G-20'
    },
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations=[dict(
        x=0.9,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://en.wikipedia.org/wiki/G20">G20 - Wikipedia</a> | <a href="https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD">World Bank</a>',
        showarrow=False
    )]
)

st.plotly_chart(fig_gdp, use_container_width=True)
st.info('Countries with higher GDP per capita are likely to have financial inclusive systems.', icon="ℹ️")

st.header('Demographics')
st.subheader('Formally banked adults')

# Global account ownership increased from 51 percent to 76 percent between 2011 and 2021
df_world = df[df['countrynewwb'] == 'World']
new_df_world = df_world[df_world['year'].notnull()].copy()
new_df_world['year'] = new_df_world['year'].astype('int')

acc_own_world_2021 = new_df_world.query('year==2021').account_t_d.iloc[0]
acc_own_world_2011 = new_df_world.query('year==2011').account_t_d.iloc[0]
acc_own_world_deltas = acc_own_world_2021 - acc_own_world_2011

acc_own_g20_2021 = df_merged.query(
    'year==2021')['account_t_d'].aggregate('average')
acc_own_g20_2011 = df_merged.query(
    'year==2011')['account_t_d'].aggregate('average')
acc_own_g20_deltas = acc_own_g20_2021 - acc_own_g20_2011

# Adults with an account (%), 2011–2021

acc_col1, acc_col2, acc_col3 = st.columns([2, 1, 1])
with acc_col1:
    st.markdown(
        'Global account ownership <span style="color:green">**increased**</span> from 51 percent to 76 percent between 2011 and 2021.', unsafe_allow_html=True)
    st.markdown('Adults with an account (%), 2011–2021')
with acc_col2:
    st.metric('World', '{0:.2f} %'.format(
        acc_own_world_2021*100), '{0:.2f} %'.format(acc_own_world_deltas/acc_own_world_2011*100))
with acc_col3:
    st.metric('G20', '{0:.2f} %'.format(
        acc_own_g20_2021*100), '{0:.2f} %'.format(acc_own_g20_deltas/acc_own_g20_2011*100))

# Unbanked by gender

new_df_world['unbanked_female'] = (1-new_df_world['account_t_d_1'])
new_df_world['unbanked_male'] = (1-new_df_world['account_t_d_2'])

new_df_world['unbanked_female_percentage'] = new_df_world.unbanked_female / \
    (new_df_world.unbanked_male + new_df_world.unbanked_female)
new_df_world['unbanked_male_percentage'] = new_df_world.unbanked_male / \
    (new_df_world.unbanked_male + new_df_world.unbanked_female)

df_gender = new_df_world[['countrynewwb', 'year',
                          'unbanked_female_percentage', 'unbanked_male_percentage']]
df_gender_pie = pd.melt(df_gender, id_vars=['countrynewwb', 'year'], value_vars=[
                        'unbanked_female_percentage', 'unbanked_male_percentage'], var_name='unbanked_gender_percentage')

gender_labels={"unbanked_female_percentage": "Female",
        "unbanked_male_percentage": "Male"}

df_gender_pie['unbanked_gender_percentage'] = df_gender_pie['unbanked_gender_percentage'].map(gender_labels)

fig_gender_pie = px.pie(df_gender_pie,
                        names='unbanked_gender_percentage',
                        values='value',
                        color='unbanked_gender_percentage',
                        color_discrete_map={'Female': '#F2A3B9',
                                            'Male': '#7BE1F5'},
                        # labels={"unbanked_gender_percentage": "Gender (%)",
                        #         "unbanked_female_percentage": "Female",
                        #         "unbanked_male_percentage": "Male"},
                        title='Adults without an account by gender (%), World average 2011-2021',
                        hole=0.3
                        )
fig_gender_pie.update_traces(
    hovertemplate=None,
    hoverinfo='skip'
)

st.plotly_chart(fig_gender_pie, use_container_width=True)
st.info('Most unbanked adults are woman', icon="ℹ️")

# st.subheader('Adults with credit at regulated institutions')

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.subheader(':family: Pop of G20')
    g20_adult_pop = df_merged.query('year==2021')['pop_adult'].aggregate('sum')
    st.metric(label='Adult Pop', value=millify(g20_adult_pop, precision=2))
    st.markdown('<span style="color:red">{0}</span> People Underserved'.format(
        millify((1-acc_own_g20_2021)*g20_adult_pop, precision=2)), unsafe_allow_html=True)
with tech2:
    st.subheader(':iphone: Mobile phone')
    phone_percentage = df_merged.query(
        'year==2021')['Own_phone'].aggregate('average')
    st.metric(label='Own a mobile phone',
              value='{0:.2f} %'.format(phone_percentage*100))
    st.markdown('{0} People'.format(
        millify(g20_adult_pop*phone_percentage, precision=2)))
with tech3:
    st.subheader(':computer: Internet')
    internet_percentage = df_merged.query(
        'year==2021')['Internet'].aggregate('average')
    st.metric(label='Has access to the Internet',
              value='{0:.2f} %'.format(internet_percentage*100))
    st.markdown('{0} People'.format(
        millify(g20_adult_pop*internet_percentage, precision=2)))

st.subheader(
    'Corellation between bank account, internet access and mobile phone')
df_corr_world = df.query('codewb not in ["EAS","ECS","LCN","MEA","NAC","SSF","OED","ARB","EMU","HIC","LIC","LMC","UMC","MIC","LMY","EAP","ECA","LAC","MNA","SAS","SSA","WLD"] and year == 2021.0')[
    ['account_t_d', 'Internet', 'Own_phone']].astype(float)
matrix_corr_world = df_corr_world.corr(method ='pearson')
fig_corr = px.imshow(matrix_corr_world.round(2),
                text_auto=True,
                aspect="auto",
                labels=dict(color="Corellation"),
                x=['Bank Account', 'Internet Access', 'Mobile Phone'],
                y=['Bank Account', 'Internet Access', 'Mobile Phone'],
                zmin=-1,
                zmax=1)
st.plotly_chart(fig_corr, use_container_width=True)
st.info('Internet Access and Mobile Phone have **Strong Positive** Relation to Bank Account', icon="ℹ️")

st.header('Conclusion')
# , the poor, the least educated and the unemployed.')
st.write('Gaps have remained in financial access, particularly for women')
st.write('People already have a **mobile phone** and **internet access**, **digital technology** can be opportunities to closes the gaps.')
st.write('The strategy is to promote the development of **digital payment systems** that allow digital or **mobile access** to **financial services** without a bank account. It will also allow women access to financial services, advancing gender equality.')
