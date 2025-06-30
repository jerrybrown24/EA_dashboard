import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load Data
df = pd.read_csv("EA.csv")

# Sidebar Filters
st.sidebar.header("🔎 Filter Data")
dept = st.sidebar.multiselect("Select Department:", df['Department'].unique(), default=df['Department'].unique())
edu = st.sidebar.multiselect("Select Education Field:", df['EducationField'].unique(), default=df['EducationField'].unique())

df_filtered = df[(df['Department'].isin(dept)) & (df['EducationField'].isin(edu))]

# Title
st.title("📊 Employee Attrition Insights Dashboard")
st.markdown("""
This dashboard provides visual insights into employee attrition patterns for HR stakeholders. 
Apply filters to explore trends in attrition across departments, demographics, and job characteristics.
""")

# Tabs for different analysis sections
tabs = st.tabs(["Overview", "Demographics", "Job & Department", "Experience & Compensation", 
                "Performance & Engagement", "Advanced Insights", "Summary Tables"])

# --- Tab 1: Overview --- #
with tabs[0]:
    st.subheader("1. Attrition Distribution")
    st.markdown("This chart shows the proportion of employees who have left the organization.")
    fig = px.pie(df_filtered, names='Attrition', title='Attrition Breakdown')
    st.plotly_chart(fig)

    st.markdown("This chart shows count of employees with and without attrition.")
    fig2 = sns.countplot(data=df_filtered, x='Attrition')
    st.pyplot(fig2.figure)

# --- Tab 2: Demographics --- #
with tabs[1]:
    st.subheader("2. Age Distribution")
    st.markdown("Age distribution split by attrition status.")
    fig = px.histogram(df_filtered, x='Age', color='Attrition', barmode='overlay')
    st.plotly_chart(fig)

    st.subheader("3. Gender Distribution")
    st.markdown("This chart compares gender representation by attrition.")
    st.plotly_chart(px.histogram(df_filtered, x='Gender', color='Attrition'))

    st.subheader("4. Marital Status")
    st.markdown("Attrition rate comparison by marital status.")
    fig = sns.countplot(data=df_filtered, x='MaritalStatus', hue='Attrition')
    st.pyplot(fig.figure)

# --- Tab 3: Job & Department --- #
with tabs[2]:
    st.subheader("5. Job Role vs Attrition")
    st.markdown("Compare attrition across different job roles.")
    st.plotly_chart(px.histogram(df_filtered, x='JobRole', color='Attrition'))

    st.subheader("6. Department Analysis")
    st.markdown("Visualizing attrition counts by department.")
    fig = sns.countplot(data=df_filtered, y='Department', hue='Attrition')
    st.pyplot(fig.figure)

    st.subheader("7. Business Travel Frequency")
    st.markdown("How business travel affects attrition rates.")
    st.plotly_chart(px.histogram(df_filtered, x='BusinessTravel', color='Attrition'))

# --- Tab 4: Experience & Compensation --- #
with tabs[3]:
    st.subheader("8. Years at Company")
    st.markdown("Attrition patterns based on company tenure.")
    st.plotly_chart(px.histogram(df_filtered, x='YearsAtCompany', color='Attrition'))

    st.subheader("9. Monthly Income Distribution")
    st.markdown("Income levels and their impact on attrition.")
    st.plotly_chart(px.box(df_filtered, x='Attrition', y='MonthlyIncome', color='Attrition'))

    st.subheader("10. Years in Current Role")
    st.markdown("How long an employee has been in their current role vs attrition.")
    st.plotly_chart(px.histogram(df_filtered, x='YearsInCurrentRole', color='Attrition'))

# --- Tab 5: Performance & Engagement --- #
with tabs[4]:
    st.subheader("11. Overtime Effect")
    st.markdown("Attrition among employees who do or don't work overtime.")
    st.plotly_chart(px.histogram(df_filtered, x='OverTime', color='Attrition'))

    st.subheader("12. Environment Satisfaction")
    st.markdown("Work environment satisfaction and its correlation with attrition.")
    fig = sns.boxplot(data=df_filtered, x='Attrition', y='EnvironmentSatisfaction')
    st.pyplot(fig.figure)

    st.subheader("13. Work-Life Balance")
    st.markdown("Work-life balance score and attrition relationship.")
    fig = sns.boxplot(data=df_filtered, x='Attrition', y='WorkLifeBalance')
    st.pyplot(fig.figure)

# --- Tab 6: Advanced Insights --- #
with tabs[5]:
    st.subheader("14. Correlation Heatmap")
    st.markdown("Heatmap showing correlations between numerical variables.")
    corr = df_filtered.select_dtypes(include='number').corr()
    fig = plt.figure(figsize=(10,6))
    sns.heatmap(corr, annot=False, cmap='coolwarm')
    st.pyplot(fig)

    st.subheader("15. Education Level vs Job Satisfaction")
    st.markdown("Does education affect job satisfaction?")
    st.plotly_chart(px.box(df_filtered, x='Education', y='JobSatisfaction', color='Attrition'))

    st.subheader("16. Total Working Years vs Monthly Income")
    st.markdown("Visualize career experience vs salary by attrition.")
    st.plotly_chart(px.scatter(df_filtered, x='TotalWorkingYears', y='MonthlyIncome', color='Attrition'))

# --- Tab 7: Summary Tables --- #
with tabs[6]:
    st.subheader("17. Department-wise Summary")
    st.markdown("Attrition stats by department.")
    st.dataframe(df_filtered.groupby(['Department', 'Attrition']).size().unstack(fill_value=0))

    st.subheader("18. Age Group Summary")
    st.markdown("Attrition split by age bins.")
    df_filtered['AgeGroup'] = pd.cut(df_filtered['Age'], bins=[18, 25, 35, 45, 60], labels=['18–25', '26–35', '36–45', '46+'])
    st.dataframe(df_filtered.groupby(['AgeGroup', 'Attrition']).size().unstack(fill_value=0))

    st.subheader("19. Job Role & Gender Table")
    st.markdown("Gender-wise attrition for each role.")
    st.dataframe(df_filtered.pivot_table(index='JobRole', columns='Gender', values='Attrition', aggfunc=lambda x: (x == 'Yes').mean()))

st.markdown("---")
st.caption("Dashboard built using Streamlit | Data source: EA.csv")
