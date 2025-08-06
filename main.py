import streamlit as st
import pandas as pd

df = pd.read_csv("diary.csv")

st.set_page_config(page_title="Movie Analysis", page_icon="🎥", layout="wide")
st.title("Life on Film")

df["Watched Date"] = pd.to_datetime(df["Watched Date"])

df["Year Watched"] = df["Watched Date"].dt.year
df["Month Watched"]  = df["Watched Date"].dt.month
df["Period"] = df["Watched Date"].dt.strftime("%Y%m")
df["Weekday"] = df["Watched Date"].dt.day_name()
df["Tipo Dia"] = df["Watched Date"].dt.dayofweek.apply(lambda x: "Final de semana" if x >=5 else "Dia de semana")

meses = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

df["Month Name"] = df["Month Watched"].map(meses)
ordem_meses = list(meses.values())
df["Month Name"] = pd.Categorical(df["Month Name"], categories=ordem_meses, ordered=True)

ordem_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df["Weekday"] = pd.Categorical(df["Weekday"], categories=ordem_dias, ordered=True)

with st.sidebar:
    st.title("Filters:")

    watched_year_list = df["Year Watched"].unique()
    year_selection = st.pills("Select the year(s) to be analyzed", watched_year_list, selection_mode="multi")

    watched_month_list = df["Month Watched"].unique()
    month_selection = st.pills("Select the months to be analyzed", watched_month_list, selection_mode="multi") 

    rating_given_list = df["Rating"].unique()
    rating_selection = st.pills("Select the rating to be analyzed", rating_given_list, selection_mode="multi")

    df_filtrado = df.copy()
    
    if year_selection:
        df_filtrado = df_filtrado[df_filtrado["Year Watched"].isin(year_selection)]

    if month_selection:
        df_filtrado = df_filtrado[df_filtrado["Month Watched"].isin(month_selection)]

    if rating_selection:
        df_filtrado = df_filtrado[df_filtrado["Rating"].isin(rating_selection)]               
       
col1, col2, col3, col4 = st.columns(4)

qtde_filmes = len(df_filtrado)
nos_cinemas = df_filtrado["Tags"].count()
periodos = df_filtrado["Period"].nunique()
monthly_avg = qtde_filmes / periodos
ano_mais_assistido = df_filtrado["Year Watched"].value_counts().idxmax()

col1.metric(label="Total Movies Watched", value=qtde_filmes, border=True)
col2.metric(label="Watched on Theaters", value=nos_cinemas, border=True)
col3.metric(label="Monthly Average", value=f"{monthly_avg:.2f}", border=True)
col4.metric(label="Year Mostly Watched", value=ano_mais_assistido, border=True)

col1_chart, col2_chart = st.columns(2)

col1_chart.subheader("Ratings Given")
col1_chart.bar_chart(df_filtrado["Rating"].value_counts().sort_index())

col2_chart.subheader("Movies watched by month")
col2_chart.bar_chart(df_filtrado["Month Name"].value_counts().sort_index())

col1_chart.subheader("Movies by week-day")
col1_chart.bar_chart(df_filtrado["Weekday"].value_counts().sort_index())

exp1 = st.expander("Detailed Data")
exp1.dataframe(df_filtrado)