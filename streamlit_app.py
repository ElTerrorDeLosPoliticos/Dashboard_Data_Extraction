from functools import cache
from control_model.control_model_query import Control_Model_Query
from control_model.connection_base import ETDLP_Control_Model_Base
from control_model.close_connection import Close_Control_ModeL_Connection

import streamlit as st
import pandas as pd
import datetime

class Dashboard:
    def __init__(self):
        st.markdown("# ETDLP - Dashboard 🎈")
#        st.sidebar.markdown("# ETDLP - Dashboard 🎈")
        st.write("Monitoreo de toda la data extraída y almacenada por ETDLP")
        self.connection = ETDLP_Control_Model_Base.create_connection()

    def get_entidades(self, tipo_registro):
        query = f"SELECT entidad FROM control_table ct  where tipo_registro='{tipo_registro}' GROUP by entidad;"
        result = Control_Model_Query.query_db(self, query)
        cleaned_result = [values for tuples in result for values in tuples]
        Close_Control_ModeL_Connection
        return cleaned_result

    def get_tipo_registro(self):
        query = f"SELECT tipo_registro FROM control_table ct GROUP BY tipo_registro;"
        result = Control_Model_Query.query_db(self, query)
        cleaned_result = [values for tuples in result for values in tuples]
        Close_Control_ModeL_Connection
        return cleaned_result

    def get_csv(self, tipo_registro, entidad):
        query = f"SELECT * FROM control_table ct WHERE tipo_registro='{tipo_registro}' AND entidad='{entidad}';"
        return pd.read_sql_query(query, self.connection)

    @staticmethod
    def last_n_day_of_month(n):
        today = datetime.datetime.now()
        if today.day < n:
            return (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=n)
        elif today.day == n:
            return today
        else:
            return today.replace(day=n)

    @staticmethod
    def status(tipo_registro, data):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        st.write(today)
        st.write(Dashboard.last_n_day_of_month(15).strftime("%Y-%m"))
        if tipo_registro=="visita" and today in data["fecha_ejecucion"].iloc[-1]: # Checking if the last update was today.
            return "✔️"
        elif tipo_registro=="planilla" and Dashboard.last_n_day_of_month(15).strftime("%Y%m") in data["fecha_de_la_info"].iloc[-1]:
            return "✔️"
        elif tipo_registro=="OrdenesDeServicio" and Dashboard.last_n_day_of_month(15).strftime("%Y%m") in data["fecha_de_la_info"].iloc[-1]:
            return "✔️"
        else:
            return "❌"

    def window(self):
        col1, col2 = st.columns(2)
        tipo_registro = col1.selectbox('Selecciona una institución', Dashboard.get_tipo_registro(self))
        entidad = col2.selectbox('Selecciona una entidad', Dashboard.get_entidades(self, tipo_registro))
        data = Dashboard.get_csv(self, tipo_registro, entidad)
        col1, col2, col3, col4 =st.columns(4)       
        col1.metric("N° Registros almacenados", value="{:,}".format(sum(data["n_items"])),
            delta=str(round(data["n_items"].pct_change().iloc[-1], 2)*100) + "%")
        col2.metric("Almacenado en",
                    value=data["almacenamiento"].iloc[-1])
        col3.metric("Última actualización",
                    value=data["fecha_ejecucion"].iloc[-1])
        col4.metric("Status", value=Dashboard.status(tipo_registro, data))
        st.write(data)

if __name__ == '__main__':
    ct = Dashboard()
    ct.window()
