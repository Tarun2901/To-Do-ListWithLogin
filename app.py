import streamlit as st
import pandas as pd

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db',check_same_thread = False)
c = conn.cursor()

import plotly.express as px
# DB fxn

from db_fxn import create_table,add_data,view_all_data,get_task,view_unique_tasks,edit_task_data,delete_data

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False






def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	st.title("Signup/Login to access To-Do List Application")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.title("To-Do app with Streamlit")

				menu = ["Create","Read","Update","Delete","About"]
				choice = st.sidebar.selectbox("Menu",menu)

				create_table()
				if choice == "Create":
					st.subheader("Add Items")
					# Layout
					col1,col2 = st.beta_columns(2)

					with col1:
						task = st.text_area("Task To Do")
					with col2:
						task_status = st.selectbox("Status",["To-Do","Doing","Done"])
						task_due_date = st.date_input("Due Date")

					if st.button("Add Task"):
						add_data(task,task_status,task_due_date)
						st.success("Successfully Added Data {} ".format(task))

				elif choice == "Read":
					st.subheader("View Items")
					result = view_all_data()
					st.write(result)
					df = pd.DataFrame(result,columns = ['Task','Status','Due Date'])
					with st.beta_expander("View All Data"):
						st.dataframe(df)

					with st.beta_expander("Task Status"):
						task_df = df['Status'].value_counts().to_frame()

						task_df = task_df.reset_index()
						st.dataframe(task_df)
						p1 = px.pie(task_df, names = 'index', values = 'Status')
						st.plotly_chart(p1)
							



				elif choice == "Update":
					st.subheader("Edit or Update Items")
					result = view_all_data()
					df = pd.DataFrame(result,columns = ['Task','Status','Due Date'])
					with st.beta_expander("Current Data"):
						st.dataframe(df)
					# st.write(view_unique_tasks())
					list_of_task =[i[0] for i in view_unique_tasks()]
					# st.write(list_of_task) 

					selected_task = st.selectbox("Task To Edit", list_of_task)
					selected_result = get_task(selected_task)
					st.write(selected_result)

					if selected_result:
						task = selected_result[0][0]
						task_status = selected_result[0][1]
						task_due_date = selected_result[0][2]
						# Layout
						col1,col2 = st.beta_columns(2)

						with col1:
							new_task = st.text_area("Task To Do",task)
						with col2:
							new_task_status = st.selectbox(task_status,["To-Do","Doing","Done"])
							new_task_due_date = st.date_input(task_due_date)

						if st.button("Update Task"):
							edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
							st.success("Successfully Updated:: {} To ::{} ".format(task,new_task))

					result2 = view_all_data()
					df = pd.DataFrame(result2,columns = ['Task','Status','Due Date'])
					with st.beta_expander("Updated Data"):
						st.dataframe(df)



				elif choice == "Delete":
					st.subheader("Delete Item")
					result = view_all_data()
					df = pd.DataFrame(result,columns = ['Task','Status','Due Date'])
					with st.beta_expander("Current Data"):
						st.dataframe(df)

					list_of_task =[i[0] for i in view_unique_tasks()]
					# st.write(list_of_task) 

					selected_task = st.selectbox("Task To Delete", list_of_task)
					st.warning("Do you want to delete ::{}".format(selected_task))
					if st.button("Delete Task"):
						delete_data(selected_task)
						st.success("Task has been successfully Deleted")

					new_result = view_all_data()
					df2 = pd.DataFrame(new_result,columns = ['Task','Status','Due Date'])
					with st.beta_expander("Updated Data"):
						st.dataframe(df2)

				else:
					st.subheader("About")

				
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")








if __name__ == '__main__':
	main()