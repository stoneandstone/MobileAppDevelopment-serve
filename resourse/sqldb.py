import mysql.connector


def get_db():
	mydb = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='123456',
		database='Android'
	)
	return mydb


def test():
	mydb = get_db()
	cursor = mydb.cursor()
	# sql = "INSERT INTO student (idstudent, name, password, email) VALUES (%s, %s, %s, %s);"
	# val = ("12", "hha", "123456", "23445")
	# sql = "SELECT * FROM `test`"
	val = ("123456",)
	sql = "SELECT * FROM student"
	cursor.execute(sql)
	# mydb.commit()
	print(cursor.fetchall())
	mydb.disconnect()


if __name__ == '__main__':
	test()

