import sqlite3
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()


# DataBase
# Table
# Field/Columns
# DataType

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS registro(nombre TEXT, tarea TEXT, horas TEXT, desempeño TEXT)')

def add_data(nombre,tarea,horas,desempeño):
	c.execute('INSERT INTO registro(nombre,tarea,horas,desempeño) VALUES (?,?,?,?)',(nombre,tarea,horas,desempeño))
	conn.commit()

def view_all_data():
	c.execute('SELECT * FROM registro')
	data = c.fetchall()
	return data

def view_unique_data():
	c.execute('SELECT DISTINCT nombre FROM registro')
	data = c.fetchall()
	return data

def get_nombre(nombre):
	c.execute('SELECT * FROM registro WHERE nombre="{}"'.format(nombre))
	#c.execute('SELECT * FROM registro WHERE nombre=?',(nombre))
	data = c.fetchall()
	return data

def edit_data(new_nombre,new_tarea,new_horas,new_desempeño,nombre,tarea,horas,desempeño):
	c.execute("UPDATE registro SET nombre =?,tarea=?,horas=?,desempeño=? WHERE nombre=? and tarea=? and horas=? and desempeño=? ",(new_nombre,new_tarea,new_horas,new_desempeño,nombre,tarea,horas,desempeño))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(nombre):
	c.execute('DELETE FROM registro WHERE nombre="{}"'.format(nombre))
	conn.commit()