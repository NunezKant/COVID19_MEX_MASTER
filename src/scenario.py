import numpy as np
import pandas as pd
import plotly.express as px

def SEAIR_D(t, population, initial_conditions,  Ro = 4, start_intervention=1, intervention_duration=119):
    """
    Esta parte de código es la que implementa las ecuaciones diferenciales.

    Se resuelven por medio de integración númerica de Euler
    """

    initial_cases = initial_conditions['initial_cases']
    exposed_per_case = initial_conditions['exposed_per_case']
    deaths = initial_conditions['deaths']

    I_o = initial_cases / population  # Tenemos 32 casos
    E_o = (initial_cases*exposed_per_case)/ population # Asumimos 4 expuestos por caso
    A_o = exposed_per_case / population
    D_o = deaths / population # No Muertos
    S_o = (1) - (E_o+I_o+A_o+D_o) # El resto somos suceptibles
    R_o = 0 # NO hay ningun recuperado

    dt =t[1]- t[0]

    alpha = 0.2
    gamma = 0.5
    rho = 0.82
    kappa = .016
    Ro = 4.0

    S,E,A,I,R,D = [S_o],[E_o],[E_o],[I_o],[R_o],[D_o]
    for i in t[1:]:
        if (i >= start_intervention and i <=(intervention_duration+start_intervention)):
            beta = Ro*gamma
        else:
            beta = Ro*gamma


        St = S[-1] - (beta*S[-1]*I[-1])*dt
        Et = E[-1] + (beta*S[-1]*I[-1] - alpha*E[-1])*dt
        At = A[-1] + (1-rho)*(alpha*E[-1] - gamma*A[-1])*dt
        It = I[-1] + rho*(alpha*E[-1] - gamma*I[-1])*dt
        Dt = kappa*I[-1]
        Rt = 1 - (S[-1]+E[-1]+A[-1]+I[-1]-D[-1])

        S.append(St)
        E.append(Et)
        A.append(At)
        I.append(It)
        R.append(Rt)
        D.append(Dt)
    return S,E,A,I,R,D


def plot_scenario(population,initial_conditions, Ro =4 , start_intervention =1, intervention_duration =119 ):

    dt=.01
    t = np.arange(0,intervention_duration+dt,dt)

    S,E,A,I,R,D = SEAIR_D(t, population, initial_conditions, Ro, start_intervention,intervention_duration)

    E_a = np.array(E)*population
    I_a = np.array(I)*population
    A_a = np.array(A)*population
    D_a = np.array(D)*population
    class_graph = np.array(["Expuestos"]*np.array(E).shape[0] + ["Infectados"]*np.array(E).shape[0]+
                      ["Asintomaticos o No reportados"]*np.array(E).shape[0] + ["Muertes"]*np.array(E).shape[0])


    days = np.concatenate([t,t,t,t])
    SEIR_df = pd.DataFrame({
        "Casos": np.concatenate([E_a,I_a,A_a,D_a]),
        "Clase": class_graph,
        "Dias" : days
    })

    fig = px.line(SEIR_df, x="Dias", y="Casos", color='Clase',color_discrete_sequence=["green", "red", "goldenrod", "blue"], template = "ggplot2")

    fig.update_layout(
        title=f"Predicción del modelo SEAIR de la evolución de COVID-19 en Jalisco",

        xaxis_title="Días",
        yaxis_title="Casos Totales",
        )

    return fig

