# Building Application

from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask,request,render_template

app=Flask(__name__)

app.config['MYSQL_HOST']="****"
app.config['MYSQL_USER']="****"
app.config['MYSQL_PASSWORD']="******"
app.config['MYSQL_DB']="*****"


mysql=MySQL(app)

@app.route('/addemp',methods=["GET","POST"])
def addemp():
  if request.method=="GET":
    return render_template('addemp_temp.html')
  elif request.method=="POST":
    empno=int(request.form['empno'])
    empname=request.form['ename']
    job=request.form['job']
    salary=float(request.form['sal'])
    cursor=mysql.connection.cursor()
    cmd = "INSERT INTO emp_flask (emp_id, ename, job, salary) VALUES (%s, %s, %s, %s)"
    cursor.execute(cmd,(empno,empname,job,salary))
    mysql.connection.commit()

    return render_template("home.html",msg="Employee Created..")
  
@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/listemp')
def listemp():
  cursor=mysql.connection.cursor()
  cursor.execute("select * from emp_flask")
  rows=cursor.fetchall()
  response=render_template('listemp.html',emp=rows)
  return response

@app.route('/updateemp',methods=["GET","POST"])
def updateemp():
  if request.method=="GET":
    return render_template("updateemp_temp.html")
  elif request.method=="POST":
    empno=int(request.form['empno'])
    sal=float(request.form['sal'])
    cursor=mysql.connection.cursor()
    cursor.execute("update emp_flask set salary=salary+%s where emp_id=%s",(sal,empno))
    k=cursor.rowcount

    if k==0:
      msg="Invalid EmployeeNo"
    else:
      msg="Salary Updated"
      mysql.connection.commit()
    response=render_template("home.html",msg=msg)
    return response


@app.route('/deleteemp',methods=["GET","POST"])
def deleteemp():
  if request.method=="GET":
    return render_template("deleteemp_temp.html")
  elif request.method=="POST":
    empno=int(request.form['empno'])
    cursor=mysql.connection.cursor()
    cursor.execute("delete from emp_flask where emp_id=%s",(empno,))
    k=cursor.rowcount
    if k==0:
      msg="Invalid Employee number"
    else:
      msg="Employee Deleted successfully..."
      mysql.connection.commit()
      response=render_template('home.html',msg=msg)
      return response


if __name__=="__main__":
  app.run(debug=True)