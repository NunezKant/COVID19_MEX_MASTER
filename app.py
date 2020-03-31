from typing import Union

import streamlit as st
import xarray as xr
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.scenario import plot_scenario

st.title('Predicción del modelo SEAIR de la evolución de COVID-19 en Jalisco')

population = st.slider(
    label="Población",
    min_value=0.0,
    max_value=10000000.0,
    value=8000000.0,
    step=100000.0,
)

ro = st.slider(
    label="Ro",
    min_value=1.0,
    max_value=4.0,
    value=3.5,
    step=0.5,
)

initial_cases = st.slider(
    label="Casos Iniciales",
    min_value=-0,
    max_value=50,
    value=32,
    step=1,
)

exposed_per_case = st.slider(
    label="Expuestos por caso",
    min_value=-0,
    max_value=10,
    value=4,
    step=1,
)

number_of_deaths = st.slider(
    label="Muertes Reportadas",
    min_value=-0,
    max_value=10,
    value=0,
    step=1,
)

initial_conditions = {
    'initial_cases':initial_cases,
    'exposed_per_case': exposed_per_case,
    'deaths': number_of_deaths # No Muertos,
}

if st.button("Play"):
    st.markdown(f"Población: {population:.1f}")
    st.markdown(f"Ro:  {ro:.1f}")
    fig = plot_scenario(population,initial_conditions, ro , start_intervention =4, intervention_duration =90 )
    st.plotly_chart(fig)
else:
    st.markdown(
        "Selecciona la localización usando los controles Y pulsa en "
        "el botón 'Pinta'."
    )
