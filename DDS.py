#GO TO POWERSHELL AND RUN COMMAND:  streamlit run data/DDS_data/DDS.py
#import plotly.express as px
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

st.title("Department of Developmental Services Purchase of Services Data 2022 - 2023")

df = pd.read_csv("cleaned_data2.csv")

# Melt the DataFrame to make it suitable for analysis
melted_df = pd.melt(df, id_vars=['Category', 'Regional Center', 'Title', 'Age Category'],
                    value_vars=['Consumers Count', 'Total Expenditures', 'Total Authorized Services', 
                                'Per Capita Expenditures', 'Per Capita Authorized Services', 
                                'Utilized', 'Total Eligible Consumers', 'Consumers Receiving Purchased Services', 
                                'Consumers with No Purchased Services', 'Percent With No Purchased Services'],
                    var_name='Metric', value_name='Value')

# Sidebar Filters
selected_title = st.sidebar.selectbox('Select a Title', df['Title'].unique())
selected_metric = st.sidebar.selectbox("Select a Metric", melted_df['Metric'].unique())
selected_age_category = st.sidebar.selectbox("Select an Age Category", melted_df['Age Category'].unique())
selected_regional_center = st.sidebar.selectbox("Select a Regional Center", melted_df['Regional Center'].unique())


# Apply filters for the first chart
filtered_df = melted_df[(melted_df['Title'] == selected_title) & 
                        (melted_df['Metric'] == selected_metric) & 
                        (melted_df['Age Category'] == selected_age_category) &
                        (melted_df['Regional Center'] == selected_regional_center)]

# Filter out "Totals" and "Totals Check" for the first bar chart
filtered_df_no_totals = filtered_df[~filtered_df['Category'].isin(['Totals', 'Totals Check'])]

# Bar Chart without "Totals"
st.markdown("## Regional Centers' Breakdowns of Totals by Title, Age, and Category")
bar_chart_no_totals = alt.Chart(filtered_df_no_totals).mark_bar().encode(
    x=alt.X('Category:N', title='Category'),
    y=alt.Y('sum(Value):Q', title='Total Value', scale=alt.Scale(zero=False)),
    color='Regional Center:N'
).properties(
    width=200,
    height=400
)
st.altair_chart(bar_chart_no_totals, use_container_width=True)

# Apply filters for the second chart (excluding the Regional Center filter)
filtered_df_only_totals = melted_df[(melted_df['Title'] == selected_title) & 
                                    (melted_df['Metric'] == selected_metric) & 
                                    (melted_df['Age Category'] == selected_age_category) & 
                                    (melted_df['Regional Center'] == selected_regional_center) & 
                                    (melted_df['Category'].isin(['Totals', 'Totals Check']))]

# Bar Chart including only "Totals" and "Totals Check"
st.markdown("## Regional Centers' Reported Totals vs Aggregate Totals of 'Title' Categories (Check Discrepancies)")


bar_chart_with_totals = alt.Chart(filtered_df_only_totals).mark_bar().encode( 
    alt.X('Category'), 
    alt.Y('sum(Value):Q', axis=alt.Axis(grid=False)), 
    alt.Color('Category'))

st.altair_chart(bar_chart_with_totals, use_container_width=True)

# Displaying Dataframe
st.write("### Data", filtered_df_only_totals)