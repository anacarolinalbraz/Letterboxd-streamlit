import streamlit as st
import pandas as pd

df = pd.read_csv("diary.csv")

st.set_page_config(page_title="Movie Analysis", page_icon="🎥")
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

st.title("Life on Film")

col1, col2, col3, col4 = st.columns(4)

qtde_filmes = len(df)
nos_cinemas = df["Tags"].count()
periodos = df["Period"].nunique()
monthly_avg = qtde_filmes / periodos
ano_mais_assistido = df["Year Watched"].value_counts().idxmax()

col1.metric(label="Total Movies Watched", value=qtde_filmes, border=True)
col2.metric(label="Watched on Theaters", value=nos_cinemas, border=True)
col3.metric(label="Monthly Average", value=f"{monthly_avg:.2f}", border=True)
col4.metric(label="Year Mostly Watched", value=ano_mais_assistido, border=True)

st.subheader("Ratings Given")
st.bar_chart(df["Rating"].value_counts().sort_index())

st.subheader("Movies watched by month")
st.bar_chart(df["Month Watched"].value_counts().sort_index())

st.subheader("Movies by week-day")
st.bar_chart(df["Weekday"].value_counts().sort_index())

exp1 = st.expander("Detailed Data")
exp1.dataframe(df)