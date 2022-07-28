from psycopg2 import OperationalError
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import datetime
import psycopg2
import os

class ETDLP_Control_Model:
    def create_connection():
        load_dotenv()
        connection = psycopg2.connect(
            database=os.getenv("db_name"),
            user=os.getenv("db_user"),
            password=os.getenv("db_password"),
            host=os.getenv("db_host"),
            port=os.getenv("db_port")
            )
        
        print("Connection to PostgreSQL DB successful")                 
        return connection

    @staticmethod
    def  query_db(self, query):
        connection = self.connection
        connection.autocommit = True
        cursor = connection.cursor()
        postgres_insert_query = f"{query}"
        cursor.execute(postgres_insert_query)
        result = cursor.fetchall()
        return result

    @staticmethod
    def close_connection(self):
        connection = self.connection
        cursor = connection.cursor()
        if connection is not None:
            cursor.close()
            connection.close()
            print("Connection to PostgreSQL DB was closed successful")       
        return True

class Dashboard:
    def __init__(self):
        st.markdown("# ETDLP - Dashboard 🎈")
        st.write("Monitoreo de toda la data extraída y almacenada por ETDLP")
        self.connection = ETDLP_Control_Model.create_connection()

    def get_entidades(self, tipo_registro):
        query = f"SELECT entidad FROM control_table ct  where tipo_registro='{tipo_registro}' GROUP by entidad;"
        result = ETDLP_Control_Model.query_db(self, query)
        cleaned_result = [values for tuples in result for values in tuples]
        ETDLP_Control_Model.close_connection
        return cleaned_result

    def get_tipo_registro(self):
        query = f"SELECT tipo_registro FROM control_table ct GROUP BY tipo_registro;"
        result = ETDLP_Control_Model.query_db(self, query)
        cleaned_result = [values for tuples in result for values in tuples]
        ETDLP_Control_Model.close_connection
        return cleaned_result

    def get_csv(self, tipo_registro, entidad):
        query = f"SELECT * FROM control_table ct WHERE tipo_registro='{tipo_registro}' AND entidad='{entidad}';"
        return pd.read_sql_query(query, self.connection)

    @staticmethod
    def get_nota(tipo_registro):
        #Returns the index of the searched file
        if tipo_registro=="OrdenesDeServicio":
            nota = "Nota: El primer registro de la tabla es solo una imagen, no las columnas.\n"
        elif tipo_registro=="visita":
            nota = "Nota: El primer registro de la tabla es solo un título, no las columnas.\n"
        elif tipo_registro=="planilla":
            nota = "Nota: Todo el dataframe es data. No es necesario eliminar la primera fila.\n"
        return nota

    @staticmethod
    def get_columns(tipo_registro):
        #Returns the columns of the searched file
        if tipo_registro=="OrdenesDeServicio":
            columns = "Columns : [ENTIDAD, RUC_ENTIDAD, FECHA_REGISTRO, FECHA_DE_EMISION, FECHA_COMPROMISO_PRESUPUESTAL, FECHA_DE_NOTIFICACION, TIPOORDEN, NRO_DE_ORDEN, ORDEN, DESCRIPCION_ORDEN, MONEDA, MONTO_TOTAL_ORDEN_ORIGINAL, OBJETOCONTRACTUAL, ESTADOCONTRATACION, TIPODECONTRATACION, DEPARTAMENTO__ENTIDAD, RUC_CONTRATISTA, NOMBRE_RAZON_CONTRATISTA]\n"
        elif tipo_registro=="visita":
            columns = "Columns: [Fecha, Entidad visitada, Visitante, Documento del visitante, Entidad del visitante, Funcionario visitado, Hora Ingreso, Hora Salida, Motivo, Lugar específico, Observación]\n"
        elif tipo_registro=="planilla":
            columns = "Columns: [ENTIDAD,PK_ID_PERSONAL,VC_PERSONAL_RUC_ENTIDAD,IN_PERSONAL_ANNO,IN_PERSONAL_MES,VC_PERSONAL_REGIMEN_LABORAL,VC_PERSONAL_PATERNO,VC_PERSONAL_MATERNO,VC_PERSONAL_NOMBRES,VC_PERSONAL_CARGO,VC_PERSONAL_DEPENDENCIA,MO_PERSONAL_REMUNERACIONES,MO_PERSONAL_HONORARIOS,MO_PERSONAL_INCENTIVO,MO_PERSONAL_GRATIFICACION,MO_PERSONAL_OTROS_BENEFICIOS,MO_PERSONAL_TOTAL,VC_PERSONAL_OBSERVACIONES,FEC_REG]\n"
        return columns

    @staticmethod
    def get_length(tipo_registro):
        #Returns the length of the searched file
        if tipo_registro=="OrdenesDeServicio":
            n_columns = "N_Columns: 18"
        elif tipo_registro=="visita":
            n_columns = "N_Columns: 11"
        elif tipo_registro=="planilla":
            n_columns = "N_Columns: 19"
        return n_columns

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
        st.code(Dashboard.get_nota(tipo_registro) + Dashboard.get_columns(tipo_registro) + Dashboard.get_length(tipo_registro))
        st.write(data)

if __name__ == '__main__':
    ct = Dashboard()
    ct.window()
