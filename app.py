import streamlit as st
import pandas as pd
import plotly.express as px
from db_app import (create_table,add_data,view_all_data,get_nombre,view_unique_data,edit_data,delete_data)
import io

buffer = io.BytesIO()


def main():
	# st.title("AFC Soluciones Aplicación Web")
	st.markdown("<h1 style='text-align: center; color: white;'>AFC Soluciones Aplicación Web</h1>", unsafe_allow_html=True)

	menu = ["Crear", "Leer", "Actualizar", "Eliminar", "Descargas"]
	choice = st.sidebar.selectbox("Menu", menu)

	create_table()
	if choice == "Crear":
		#st.subheader("Agregar Datos")
		st.markdown("<h3 style='text-align: center; color: white;'>Agregar Datos</h3>", unsafe_allow_html=True)


		# Layout
		col1,col2,col3 = st.columns(3)

		with col2:
			nombre = st.text_area("Nombre del Productor(a)")
			tarea = st.text_area("Tarea que desempeñó")
			horas = st.selectbox("Número de horas empleadas", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
			desempeño = st.selectbox("¿Usted habitualmente desempeña esta tarea?", ["Si", "No"])

			if st.button("Agregar Datos"):
				add_data(nombre,tarea,horas,desempeño)
				st.success("Datos agregados satisfactoriamente")

		
		
			
	elif choice == "Leer":
		#st.subheader("Revisar Datos")
		st.markdown("<h3 style='text-align: center; color: white;'>Revisar Datos</h3>", unsafe_allow_html=True)
		result = view_all_data()
		#st.write(result)
		df = pd.DataFrame(result, columns=['Nombre', 'Tarea', 'Horas empleadas', 'Desempeña habitualmente'])
		
		with st.expander("Ver todos los datos"):
			st.dataframe(df)

		with st.expander("Ver cantidad de horas empleadas por cada productor"):
			



			nombre_df = df[["Nombre", "Horas empleadas"]].value_counts().to_frame()
			
			nombre_df = nombre_df.reset_index()
			
			p1 = px.pie(nombre_df, names='Nombre', values='Horas empleadas', width=500, height=500)
			st.plotly_chart(p1)

		with st.expander("Ver cantidad de horas empleadas por cada tarea"):
			tarea_df = df[["Tarea", "Horas empleadas"]].value_counts().to_frame()
			
			tarea_df = tarea_df.reset_index()
						
			p2 = px.pie(tarea_df, names='Tarea',values='Horas empleadas', width=500, height=500)
			st.plotly_chart(p2)




	elif choice == "Actualizar":
		st.markdown("<h3 style='text-align: center; color: white;'>Editar o Actualizar Datos</h3>", unsafe_allow_html=True)
		result = view_all_data()

		df = pd.DataFrame(result, columns=['Nombre', 'Tarea', 'Horas empleadas', 'Desempeña habitualmente'])
		
		with st.expander("Ver todos los datos actuales"):
			st.dataframe(df)

		list_of_nombre = [i[0] for i in view_unique_data()]
		
		selected_nombre = st.selectbox("Editar datos del o la productor(a)", list_of_nombre)

		selected_result = get_nombre(selected_nombre)
		
		if selected_result:
			nombre = selected_result[0][0]
			tarea = selected_result[0][1]
			horas = selected_result[0][2]
			desempeño = selected_result[0][3]
			# Layout
			col1,col2,col3 = st.columns(3)

			with col2:
				new_nombre = st.text_area("Nombre del Productor(a)", nombre)
				new_tarea = st.text_area("Tarea que desempeñó", tarea)
				new_horas = st.selectbox(horas, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
				new_desempeño = st.selectbox(desempeño, ["Si", "No"])

				if st.button("Actualizar Datos"):
					edit_data(new_nombre,new_tarea,new_horas,new_desempeño,nombre,tarea,horas,desempeño) 
					st.success("Datos actualizados satisfactoriamente")


		result2 = view_all_data()

		df2 = pd.DataFrame(result2, columns=['Nombre', 'Tarea', 'Horas empleadas', 'Desempeña habitualmente'])
		
		with st.expander("Ver todos los datos actualizados"):
			st.dataframe(df2)





	elif choice == "Eliminar":
		#st.subheader("Eliminar Datos")
		st.markdown("<h3 style='text-align: center; color: white;'>Eliminar Datos</h3>", unsafe_allow_html=True)

		result = view_all_data()

		df = pd.DataFrame(result, columns=['Nombre', 'Tarea', 'Horas empleadas', 'Desempeña habitualmente'])
		
		with st.expander("Ver todos los datos actuales"):
			st.dataframe(df)

		list_of_nombre = [i[0] for i in view_unique_data()]
		st.warning("¿Está seguro de que quiere eliminar los datos seleccionados?")
		selected_nombre = st.selectbox("Eliminar datos del o la productor(a)", list_of_nombre)
		if st.button("Eliminar datos"):
			delete_data(selected_nombre)
			st.success("Los datos fueron eliminados satisfactoriamente")
		
		new_result = view_all_data()

		df2 = pd.DataFrame(new_result, columns=['Nombre', 'Tarea', 'Horas empleadas', 'Desempeña habitualmente'])
		
		with st.expander("Ver todos los datos actualizados"):
			st.dataframe(df2)

	else:
		#st.subheader("Acerca de")
		st.markdown("<h3 style='text-align: center; color: white;'>Descargas</h3>", unsafe_allow_html=True)

		new_result = view_all_data()

		df2 = pd.DataFrame(new_result, columns=['Nombre', 'Tarea', 'Horas empleadas', 'Desempeña habitualmente'])
		
		with st.expander("Ver todos los datos actualizados"):
			st.dataframe(df2)

		#st.download_button("Descargar CSV", csv, "file.csv", "text/csv", key='download-csv')


		#st.download_button(label='Descargar CSV',data=df2.to_csv(),mime='text/csv')

		with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
			df2.to_excel(writer, index=False, sheet_name='Hoja1')
			writer.save()

			st.download_button(label='Descargar Excel', data=buffer, file_name="Registro.xlsx", mime="application/vnd.ms-excel")

if __name__ == '__main__':
	main() 