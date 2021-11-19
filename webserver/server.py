
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.74.246.148/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@34.74.246.148/proj1part2"
#
DATABASEURI = "postgresql://rs4202:3746@34.74.246.148/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)
conn = engine.connect()
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: https://flask.palletsprojects.com/en/2.0.x/quickstart/?highlight=routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/2.0.x/api/?highlight=incoming%20request%20data

  """

  # DEBUG: this is debugging code to see what request looks like
  print(request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT * FROM Animal_Founded")
  lines = []
  for result in cursor:
    lines.append(list(result))  # can also be accessed using result[0]
    print(list(result))
  cursor.close()

  cursor2 = g.conn.execute("SELECT bid FROM Breeder_Managed")
  line2 = []
  for result in cursor2:
      line2.append(result["bid"])
  cursor2.close()
    
  cursor3 = g.conn.execute("SELECT tid FROM Trainer_Managed")
  line3 = []
  for result in cursor3:
      line3.append(result["tid"])
  cursor3.close()
  line3.append(None)
    
  cursor4 = g.conn.execute("SELECT fname FROM Food")
  line4 = []
  for result in cursor4:
      line4.append(result["fname"])
  cursor4.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = lines)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context, breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
    cursor = g.conn.execute("SELECT * FROM Trainer_Managed")
    lines = []
    for result in cursor:
        lines.append(list(result))  # can also be accessed using result[0]
        print(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("another.html", **context)


@app.route('/breeder')
def breeder():
    cursor = g.conn.execute("SELECT * FROM Breeder_Managed")
    lines = []
    for result in cursor:
        lines.append(list(result))  # can also be accessed using result[0]
        print(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("breeder.html", **context)


@app.route('/facility')
def facility():
    cursor = g.conn.execute("SELECT * FROM Facility_Located")
    lines = []
    for result in cursor:
        lines.append(list(result))  # can also be accessed using result[0]
        print(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("facility.html", **context)


@app.route('/food')
def food():
    cursor = g.conn.execute("SELECT * FROM Food")
    lines = []
    for result in cursor:
        lines.append(list(result))  # can also be accessed using result[0]
        print(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("food.html", **context)


@app.route('/animalShow')
def animalShow():
    cursor = g.conn.execute("SELECT * FROM Animal_Show_Held")
    lines = []
    for result in cursor:
        lines.append(list(result))  # can also be accessed using result[0]
        print(list(result))
    cursor.close()
    context = dict(data=lines)
        cursor2 = g.conn.execute("SELECT aid FROM Animal_Founded")
    lines2 = []
    for result in cursor2:
        lines2.append(result["aid"])
    cursor2.close()
    lines2.append(None)

    cursor3 = g.conn.execute("SELECT tid FROM Trainer_Managed")
    lines3 = []
    for result in cursor3:
        lines3.append(result["tid"])
    cursor3.close()
    lines3.append(None)
    return render_template("animalShow.html", **context,animalMessage=lines2,
                           trainerMessage=lines3)


@app.route('/manager')
def manageer():
    cursor = g.conn.execute("SELECT * FROM Manager")
    lines = []
    for result in cursor:
        lines.append(list(result))  # can also be accessed using result[0]
        print(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("manager.html", **context)


@app.route('/park')
def park():
    cursor = g.conn.execute("SELECT * FROM Park")
    lines = []
    for result in cursor:
        lines.append(list(result))  # can also be accessed using result[0]
        print(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("park.html", **context)


@app.route('/relationBA')
def relationBA():
    cursor = g.conn.execute("SELECT * FROM Breeded_By")
    lines = []
    for result in cursor:
        lines.append(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("relationBA.html",**context)


@app.route('/relationTA')
def relationTA():
    cursor = g.conn.execute("SELECT * FROM Trained_By")
    lines = []
    for result in cursor:
        lines.append(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("relationTA.html",**context)


@app.route('/relationFA')
def relationFA():
    cursor = g.conn.execute("SELECT * FROM Eat")
    lines = []
    for result in cursor:
        lines.append(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("relationBA.html",**context)


@app.route('/relationP')
def relationP():
    cursor = g.conn.execute("SELECT * FROM Participate_In")
    lines = []
    for result in cursor:
        lines.append(list(result))
    cursor.close()
    context = dict(data=lines)
    return render_template("relationP.html",**context)


# Example of adding new data to the database
#@app.route('/add', methods=['POST'])
#def add():
#  name = request.form['name']
#  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#  return redirect('/')

@app.route('/addAnimal',methods=['GET','POST'])
def addAnimal():
    aid = request.form['aid']
    species = request.form['species']
    age = request.form['age']
    comesFrom = request.form['comes_from']
    eatingProperty = request.form['eating_property']
    activityTime = request.form['activity_time']
    lifestyle = request.form['lifestyle']
    pname = request.form['parkname']
    
    bid=request.form['B']
    tid=request.form['T']
    fname=request.form['F']

    cursor2 = g.conn.execute("SELECT bid FROM Breeder_Managed")
    line2 = []
    for result in cursor2:
        line2.append(result["bid"])
    cursor2.close()

    cursor3 = g.conn.execute("SELECT tid FROM Trainer_Managed")
    line3 = []
    for result in cursor3:
        line3.append(result["tid"])
    cursor3.close()

    cursor4 = g.conn.execute("SELECT fname FROM Food")
    line4 = []
    for result in cursor4:
        line4.append(result["fname"])
    cursor4.close()

    if aid == '':
        message = "AID cannot be NULL"
        return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    if age == '':
        message = "Age cannot be NULL"
        return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)
    else:
        age = int(age)

    if age < 0:
        message = "Age cannot be Smaller Than 0"
        return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    if pname == ' ':
        message = "Park Name cannot be NULL"
        return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    cursor = g.conn.execute("SELECT aid FROM Animal_Founded")
    pk = []
    for result in cursor:
        pk.append(result["aid"])
    cursor.close()
    if aid in pk:
        message = "The AID Has Already Existed!"
        return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor.close()
    if pname not in aid:
        message = "The Park Name Does Not Existed! "
        return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    g.conn.execute("""INSERT INTO Animal_Founded(aid,species,age,comes_from,
                  eating_property,activity_time,lifestyle,pname)
                  VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                   aid, species, age, comesFrom,
                   eatingProperty, activityTime, lifestyle, pname)


    if bid == "Assign Breeder":
        message = "Please Choose A Breeder"
        return render_template("index.html",addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    if tid == "Assign Trainer":
        message = "Please Choose A Trainer"
        return render_template("index.html",addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    if fname=="Assign Food":
        message = "Please Choose Food"
        return render_template("index.html",addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)

    checkpk = [bid,aid]
    cursor3 = g.conn.excute("SELECT * FROM Breeded_By")
    for line in cursor3:
        newpk = list(line)
        if checkpk == newpk:
            message = "The Relationship Has Already Existed"
            return render_template("index.html",addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)
    cursor3.close()
    g.conn.execute("""INSERT INTO Breeded_By(bid, aid) VALUES(%s, %s)""",
                   bid, aid)

    checkpk2 = [tid,aid]
    cursor4 = g.conn.execute("SELECT * FROM Trained_By")
    for line in cursor4:
        newpk = list(line)
        if checkpk2 == newpk:
            message = "The Relationship Has Already Existed"
            return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)
    cursor4.close()

    if tid!=None:
        g.conn.execute("""INSERT INTO Trained_By(tid,aid) VALUES (%s, %s)""",
                       tid, aid)

    checkpk3 = [fname,aid]
    cursor5 = g.conn.execute("SELECT * Eat")
    for line in cursor4:
        newpk = list(line)
        if checkpk3 == newpk:
            message = "The Relationship Has Already Existed"
            return render_template("index.html", addMessage=message,breederMessage=line2,
                           trainerMessage=line3,foodMessage=line4)
    cursor5.close()
    g.conn.execute("""INSERT INTO Eat(fname,aid) VALUES (%s, %s)""",
                   fname, aid)
    return redirect('/')


@app.route('/deleteAnimal', methods=['POST'])
def deleteAnimal():
    aid = request.form['aid']
    
    cursor = g.conn.execute("SELECT aid FROM Animal_Founded")
    pk = []
    for result in cursor:
      pk.append(result["aid"])
    cursor.close()
    if aid not in pk:
      message = "The AID Does Not Exist!"
      return render_template("index.html", deleteMessage=message)

    g.conn.execute("""DELETE FROM Breeded_By WHERE aid=%s""",aid)

    cursor2 = g.conn.execute("SELECT aid FROM Trained_By")
    aids = []
    for result in cursor2:
        aids.append(result["aid"])
    cursor2.close()
    if aid in aids:
        g.conn.execute("DELETE FROM Trained_By WHERE aid=%s",aid)

    g.conn.execute("DELETE FROM Eat WHERE aid=%s",aid)
    
    cursor3 = g.conn.execute("SELECT aid FROM Participate_In")
    aids2 = []
    for result in cursor3:
        aids2.append(result["aid"])
    cursor3.close()
    if aid in aids2:
        g.conn.execute("DELETE FROM Participate_in WHERE aid=%s", aid)
    
    
    g.conn.execute("""DELETE FROM Animal_Founded WHERE aid = %s""", aid)
    
    return redirect('/')


@app.route('/updateAnimal', methods=['POST'])
def updateAnimal():
  aid = request.form['aid']
  species = request.form['species']
  age = request.form['age']
  comesFrom = request.form['comes_from']
  eatingProperty = request.form['eating_property']
  activityTime = request.form['activity_time']
  lifestyle = request.form['lifestyle']
  pname = request.form['parkname']
    
  if aid == '':
      message = "AID cannot be NULL"
      return render_template("index.html",updateMessage = message)

  if age != '':
      age = int(age)
  else:
      message = "Age cannot be NULL"
      return render_template("index.html",updateMessage = message)

  if age<0:
      message = "Age cannot be Smaller Than 0"
      return render_template("index.html",updateMessage = message)

  if pname == '':
      message = "Park Name cannot be NULL"
      return render_template("index.html",updateMessage = message)


  cursor = g.conn.execute("SELECT aid FROM Animal_Founded")
  pk = []
  for result in cursor:
      pk.append(result["aid"])
  cursor.close()
  if aid not in pk:
      message = "The AID Does NOT Exist!"
      return render_template("index.html",updateMessage=message)

  cursor2 = g.conn.execute("SELECT pname FROM Park")
  fk = []
  for line in cursor2:
      fk.append(line["pname"])
  cursor2.close()
  if pname not in fk:
      message = "The Park Name Does Not Exist! "
      return render_template("index.html",updateMessage=message)

  g.conn.execute("""UPDATE Animal_Founded SET (species, age, comes_from,
                  eating_property, activity_time, lifestyle, pname) = 
                  (%s, %s, %s, %s, %s, %s, %s) WHERE aid = %s""",
                 species, age, comesFrom, eatingProperty, activityTime,
                 lifestyle, pname, aid)
  return redirect('/')


@app.route('/addBreeder', methods=['POST'])
def addBreeder():
    bid = request.form['bid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    mid = request.form['mid']
    
    if bid == '':
      message = "BID cannot be NULL"
      return render_template("breeder.html", addMessage=message)

    if mid == '':
      message = "MID cannot be NULL"
      return render_template("breeder.html", addMessage=message)

    cursor = g.conn.execute("SELECT bid FROM Breeder_Managed")
    pk = []
    for result in cursor:
      pk.append(result["bid"])
    cursor.close()
    if bid in pk:
      message = "The BID Has Already Existed!"
      return render_template("breeder.html", addMessage=message)

    cursor2 = g.conn.execute("SELECT mid FROM Manager")
    fk = []
    for line in cursor2:
      fk.append(line["mid"])
    cursor2.close()
    if mid not in fk:
      message = "The MID Does NOT Exist! "
      return render_template("breeder.html", addMessage=message)
    
    g.conn.execute("""INSERT INTO Breeder_Managed(bid, first_name,
                  last_name, work_time, mid)
                  VALUES(%s, %s, %s, %s, %s)""",
                   bid, firstName, lastName, workTime, mid)
    return redirect('/breeder')


@app.route('/deleteBreeder', methods=['POST'])
def deleteBreeder():
    bid = request.form['bid']
    
    cursor = g.conn.execute("SELECT bid FROM Breeder_Managed")
    pk = []
    for result in cursor:
      pk.append(result["bid"])
    cursor.close()
    if bid not in pk:
      message = "The BID Does NOT Exist!"
      return render_template("breeder.html", deleteMessage=message)
    
    cursor2 = g.conn.execute("SELECT bid FROM Breeded_By")
    bids = []
    for result in cursor2:
        bids.append(result["bid"])
    cursor2.close()
    if bid in bids:
        g.conn.execute("DELETE FROM Breeded_By WHERE bid=%s", bid)
    
    g.conn.execute("DELETE FROM Breeder_Managed WHERE bid = %s", bid)
    return redirect('/breeder')


@app.route('/updateBreeder', methods=['POST'])
def updateBreeder():
    bid = request.form['bid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    mid = request.form['mid']
    
    if bid == '':
      message = "BID cannot be NULL"
      return render_template("breeder.html", updateMessage=message)

    if mid == '':
      message = "MID cannot be NULL"
      return render_template("breeder.html", updateMessage=message)

    cursor = g.conn.execute("SELECT bid FROM Breeder_Managed")
    pk = []
    for result in cursor:
      pk.append(result["bid"])
    cursor.close()
    if bid not in pk:
      message = "The BID Does NOT Exist!"
      return render_template("breeder.html", updateMessage=message)

    cursor2 = g.conn.execute("SELECT mid FROM Manager")
    fk = []
    for line in cursor2:
      fk.append(line["mid"])
    cursor2.close()
    if mid not in fk:
      message = "The MID Does NOT Exist! "
      return render_template("breeder.html", updateMessage=message)
    
    g.conn.execute("""UPDATE Breeder_Managed SET (first_name,
                  last_name, work_time, mid) = (%s, %s, %s, %s)
                  WHERE bid = %s""",
                   firstName, lastName, workTime, mid, bid)
    return redirect('/breeder')


@app.route('/addTrainer', methods=['POST'])
def addTrainer():
    tid = request.form['tid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    mid = request.form['mid']
    
    if tid == '':
      message = "TID cannot be NULL"
      return render_template("another.html", addMessage=message)

    if mid == '':
      message = "MID cannot be NULL"
      return render_template("another.html", addMessage=message)

    cursor = g.conn.execute("SELECT tid FROM Trainer_Managed")
    pk = []
    for result in cursor:
      pk.append(result["tid"])
    cursor.close()
    if tid in pk:
      message = "The TID Has Already Existed!"
      return render_template("another.html", addMessage=message)

    cursor2 = g.conn.execute("SELECT mid FROM Manager")
    fk = []
    for line in cursor2:
      fk.append(line["mid"])
    cursor2.close()
    if mid not in fk:
      message = "The MID Does NOT Exist! "
      return render_template("another.html", addMessage=message)

    g.conn.execute("""INSERT INTO Trainer_Managed(tid, first_name,
              last_name, work_time, mid)
              VALUES(%s, %s, %s, %s, %s)""",
                   tid, firstName, lastName, workTime, mid)
    return redirect('/another')


@app.route('/deleteTrainer', methods=['POST'])
def deleteTrainer():
    tid = request.form['tid']
    
    cursor = g.conn.execute("SELECT tid FROM Trainer_Managed")
    pk = []
    for result in cursor:
      pk.append(result["tid"])
    cursor.close()
    if tid not in pk:
      message = "The TID Does NOT Exist!"
      return render_template("another.html", deleteMessage=message)
    
    cursor2 = g.conn.execute("SELECT tid FROM Trained_By")
    tids = []
    for result in cursor2:
        tids.append(result["tid"])
    cursor2.close()
    if tid in tids:
        g.conn.execute("DELETE FROM Trained_By WHERE bid=%s", tid)

    cursor3 = g.conn.execute("SELECT tid FROM Trained_By")
    tids2 = []
    for result in cursor3:
        tids2.append(result["tid"])
    cursor3.close()
    if tid in tids2:
        g.conn.execute("DELETE FROM Participate_In WHERE bid=%s",tid)
    
    g.conn.execute("DELETE FROM Trainer_Managed WHERE tid = %s", tid)
    return redirect('/another')


@app.route('/updateTrainer', methods=['POST'])
def updateTrainer():
    tid = request.form['tid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    mid = request.form['mid']
    
    if tid == '':
      message = "TID cannot be NULL"
      return render_template("another.html", updateMessage=message)

    if mid == '':
      message = "MID cannot be NULL"
      return render_template("another.html", updateMessage=message)

    cursor = g.conn.execute("SELECT tid FROM Trainer_Managed")
    pk = []
    for result in cursor:
      pk.append(result["tid"])
    cursor.close()
    if tid not in pk:
      message = "The TID Does NOT Exist!"
      return render_template("another.html", updateMessage=message)

    cursor2 = g.conn.execute("SELECT mid FROM Manager")
    fk = []
    for line in cursor2:
      fk.append(line["mid"])
    cursor2.close()
    if mid not in fk:
      message = "The MID Does NOT Exist! "
      return render_template("another.html", updateMessage=message)
    
    g.conn.execute("""UPDATE Trainer_Managed SET (first_name,
              last_name, work_time, mid) = (%s, %s, %s, %s)
              WHERE tid = %s""",
                   firstName, lastName, workTime, mid, tid)
    return redirect('/another')


@app.route('/addFood', methods=['POST'])
def addFood():
    fname = request.form['fname']
    timePurchased = request.form['time_purchased']
    brand = request.form['brand']
    unitPrice = request.form['unit_price']
    amount = request.form['amount']
    
    if unitPrice == '':
        message = "Unit Price cannot be NULL"
        return render_template('food.html', addMessage=message)
    else:
        unitPrice = float(unitPrice)
    
    if amount == '':
        message = "Amount cannot be NULL"
        return render_template('food.html', addMessage=message)
    else:
        amount = int(amount)

    if unitPrice < 0:
        message = "Unit Price Should be Larger than 0!"
        return render_template('food.html', addMessage=message)

    if amount < 0:
        message = "Amount Should be Larger than 0!"
        return render_template('food.html', addMessgae=message)

    if fname == '':
        message = "Food Name cannot be NULL"
        return render_template("food.html", addMessage=message)

    cursor = g.conn.execute("SELECT fname FROM Food")
    pk = []
    for result in cursor:
        pk.append(result["fname"])
    cursor.close()
    if fname in pk:
        message = "The Food Has Already Existed!"
        return render_template("food.html", addMessage=message)
    
    g.conn.execute("""INSERT INTO Food(fname, time_purchased, brand,
                unit_price, amount)
                VALUES(%s, %s, %s, %s, %s)""",
                   fname, timePurchased, brand, unitPrice, amount)
    return redirect('/food')


@app.route('/deleteFood', methods=['POST'])
def deleteFood():
    fname = request.form['fname']
    
    cursor = g.conn.execute("SELECT fname FROM Food")
    pk = []
    for result in cursor:
        pk.append(result["fname"])
    cursor.close()
    if fname not in pk:
        message = "The Food Does NOT Exist!"
        return render_template("food.html", deleteMessage=message)
    
    cursor2 = g.conn.execute("SELECT fname FROM Eat")
    fnames = []
    for result in cursor2:
        fnames.append(result["fname"])
    cursor2.close()
    if fname in fnames:
        g.conn.execute("DELETE FROM Eat WHERE fname=%s",fname)
    
    g.conn.execute("""DELETE FROM Food WHERE fname = %s""", fname)
    return redirect('/food')


@app.route('/updateFood', methods=['POST'])
def updateFood():
    fname = request.form['fname']
    timePurchased = request.form['time_purchased']
    brand = request.form['brand']
    unitPrice = request.form['unit_price']
    amount = request.form['amount']
    
    if unitPrice == '':
        message = "Unit Price cannot be NULL"
        return render_template('food.html', updateMessage=message)
    else:
        unitPrice = float(unitPrice)

    if amount == '':
        message = "Amount cannot be NULL"
        return render_template('food.html', updateMessage=message)
    else:
        amount = int(amount)

    if unitPrice < 0:
        message = "Unit Price Should be Larger than 0!"
        return render_template('food.html', updateMessage=message)

    if amount < 0:
        message = "Amount Should be Larger than 0!"
        return render_template('food.html', updateMessgae=message)

    if fname == '':
        message = "Food Name cannot be NULL"
        return render_template("food.html", updateMessage=message)

    cursor = g.conn.execute("SELECT fname FROM Food")
    pk = []
    for result in cursor:
        pk.append(result["fname"])
    cursor.close()
    if fname not in pk:
        message = "The Food Does NOT Exist!"
        return render_template("food.html", updateMessage=message)
    
    g.conn.execute("""UPDATE Food SET (time_purchased, brand,
                unit_price, amount) = (%s, %s, %s, %s)
                WHERE fname = %s""",
                   timePurchased, brand, unitPrice, amount, fname)
    return redirect('/food')


@app.route('/addAnimalShow', methods=['POST'])
def addAnimalShow():
    sid = request.form['sid']
    showName = request.form['show_name']
    seat = request.form['seat']
    time = request.form['time']
    pname = request.form['pname']
    
    aid = request.form['A']
    tid = request.form['T']

    cursor2 = g.conn.execute("SELECT aid FROM Animal_Founded")
    lines2 = []
    for result in cursor2:
        lines2.append(result["aid"])
    cursor2.close()
    lines2.append(None)

    cursor3 = g.conn.execute("SELECT tid FROM Trainer_Managed")
    lines3 = []
    for result in cursor3:
        lines3.append(result["tid"])
    cursor3.close()
    lines3.append(None)

    if sid == '':
        message = "SID cannot be NULL"
        return render_template("animalShow.html", addMessage=message,animalMessage=lines2,
                           trainerMessage=lines3)

    if seat == '':
        message = "Seat cannot be NULL"
        return render_template("animalShow.html", addMessage=message,animalMessage=lines2,
                           trainerMessage=lines3)
    else:
        seat = int(seat)

    if aid == "Assign Animal":
        message = "Please choose a animal"
        return render_template("animalShow.html", addMessage=message,animalMessage=lines2,
                           trainerMessage=lines3)

    if tid == "Assign Trainer":
        message = "Please choose a trainer"
        return render_template("animalShow.html", addMessage=message,animalMessage=lines2,
                           trainerMessage=lines3)

    if aid!=None and tid!=None:
        g.conn.execute("INSERT INTO Participate_In(sid, aid, tid) VALUES (%s,%s,%s)",
                       sid, aid, tid)

    cursor = g.conn.execute("SELECT sid FROM Animal_Show_Held")
    pk = []
    for result in cursor:
        pk.append(result["sid"])
    cursor.close()
    if sid in pk:
        message = "The Show Has Already Existed!"
        return render_template("animalShow.html", addMessage=message,animalMessage=lines2,
                           trainerMessage=lines3)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor.close()
    if pname not in fk:
        message = "The Park Does NOT Exist! "
        return render_template("animalShow.html", addMessage=message,animalMessage=lines2,
                           trainerMessage=lines3)
    
    g.conn.execute("""INSERT INTO Animal_Show_Held(sid, show_name,
                seat, time, pname) VALUES(%s, %s, %s, %s, %s)""",
                   sid, showName, seat, time, pname)
    return redirect('/animalShow')


@app.route('/deleteAnimalShow', methods=['POST'])
def deleteAnimalShow():
    sid = request.form['sid']
    
    cursor = g.conn.execute("SELECT sid FROM Animal_Show_Held")
    pk = []
    for result in cursor:
      pk.append(result["sid"])
    cursor.close()
    if sid not in pk:
      message = "The Show Does NOT Exist!"
      return render_template("animalShow.html", deleteMessage=message)
    
    cursor2 = g.conn.execute("SELECT sid FROM Participate_In")
    sids = []
    for result in cursor2:
        sids.append(result["sid"])
    cursor2.close()
    if sid in sids:
        g.conn.execute("DELETE FROM Participate_In WHERE sid=%s",sid)
    
    g.conn.execute("DELETE FROM Animal_Show_Held WHERE sid = %s", sid)
    return redirect('/animalShow')


@app.route('/updateAnimalShow', methods=['POST'])
def updateAnimalShow():
    sid = request.form['sid']
    showName = request.form['show_name']
    seat = request.form['seat']
    time = request.form['time']
    pname = request.form['pname']
    
    if sid == '':
      message = "SID cannot be NULL"
      return render_template("animalShow.html", updateMessage=message)
    
    if pname == '':
      message = "Park Name cannot be NULL"
      return render_template("animalShow.html", updateMessage=message)

    if seat == '':
      message = "Seat cannot be NULL"
      return render_template("animalShow.html", updateMessage=message)
    else:
      seat = int(seat)

    cursor = g.conn.execute("SELECT sid FROM Animal_Show_Held")
    pk = []
    for result in cursor:
      pk.append(result["sid"])
    cursor.close()
    if sid not in pk:
      message = "The Show Does NOT Exist!"
      return render_template("animalShow.html", updateMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
      fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
      message = "The Park Does NOT Exist! "
      return render_template("animalShow.html", updateMessage=message)
    
    g.conn.execute("""UPDATE Animal_Show_Held SET (show_name,
                seat, time, pname) = (%s, %s, %s, %s)
                WHERE sid = %s""",
                   showName, seat, time, pname, sid)
    return redirect('/animalShow')


@app.route('/addFacility', methods=['POST'])
def addFacility():
    fid = request.form['fid']
    typee = request.form['type']
    name = request.form['name']
    openHour = request.form['open_hour']
    pname = request.form['pname']
    
    if fid == '':
        message = "FID cannot be NULL"
        return render_template("facility.html", addMessage=message)

    if pname == '':
        message = "Park Name cannot be NULL"
        return render_template("facility.html", addMessage=message)

    cursor = g.conn.execute("SELECT fid FROM Facility_Located")
    pk = []
    for result in cursor:
        pk.append(result["fid"])
    cursor.close()
    if fid in pk:
        message = "The Facility Has Already Existed!"
        return render_template("facility.html", addMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
        message = "The Park Does NOT Exist! "
        return render_template("facility.html", addMessage=message)                     
                         
    g.conn.execute("""INSERT INTO Facility_Located(fid, type, name,
                open_hour, pname) VALUES(%s, %s, %s, %s, %s)""",
                   fid, typee, name, openHour, pname)
    return redirect('/facility')


@app.route('/deleteFacility', methods=['POST'])
def deleteFacility():
    fid = request.form['fid']
    
    cursor = g.conn.execute("SELECT fid FROM Facility_Located")
    pk = []
    for result in cursor:
        pk.append(result["fid"])
    cursor.close()
    if fid not in pk:
        message = "The Facility Does NOT Exist!"
        return render_template("facility.html", addMessage=message)
    
    g.conn.execute("DELETE FROM Facility_Located WHERE fid = %s", fid)
    return redirect('/facility')


@app.route('/updateFacility', methods=['POST'])
def updateFacility():
    fid = request.form['fid']
    typee = request.form['type']
    name = request.form['name']
    openHour = request.form['open_hour']
    pname = request.form['pname']
    
    if fid == '':
        message = "FID cannot be NULL"
        return render_template("facility.html", updateMessage=message)

    if pname == '':
        message = "Park Name cannot be NULL"
        return render_template("facility.html", updateMessage=message)

    cursor = g.conn.execute("SELECT fid FROM Facility_Located")
    pk = []
    for result in cursor:
        pk.append(result["fid"])
    cursor.close()
    if fid not in pk:
        message = "The Facility Does NOT Exist!"
        return render_template("facility.html", updateMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
        message = "The Park Does NOT Exist!"
        return render_template("facility.html", updateMessage=message)
    
    g.conn.execute("""UPDATE Facility_Located SET (type, name,
                open_hour, pname) = (%s, %s, %s, %s)
                WHERE fid = %s""",
                   typee, name, openHour, pname, fid)
    return redirect('/facility')


@app.route('/addPark', methods=['POST'])
def addPark():
    pname = request.form['pname']
    openHour = request.form['open_hour']
    typee = request.form['type']
    
    if pname == '':
        message = "Park Name cannot be NULL"
        return render_template("park.html", addMessage=message)

    cursor = g.conn.execute("SELECT type FROM Park")
    pk = []
    for result in cursor:
        pk.append(result["type"])
    cursor.close()
    if typee in pk:
        message = "The Type Has Already Existed!"
        return render_template("park.html", addMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname in fk:
        message = "The Park Has Already Existed! "
        return render_template("park.html", addMessage=message)
    
    g.conn.execute("""INSERT INTO Park(pname, open_hour, type)
                VALUES (%s, %s, %s)""", pname, openHour, typee)
    return redirect('/park')


@app.route('/deletePark', methods=['POST'])
def deletePark():
    pname = request.form['pname']
    
    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
        message = "The Park Does NOT Exist! "
        return render_template("park.html", deleteMessage=message)
    
    g.conn.execute('DELETE FROM Park WHERE pname = %s', pname)
    return redirect('/park')


@app.route('/updatePark', methods=['POST'])
def updatePark():
    pname = request.form['pname']
    openHour = request.form['open_hour']
    typee = request.form['type']
    
    if pname == '':
        message = "Park Name cannot be NULL"
        return render_template("park.html", updateMessage=message)

    cursor = g.conn.execute("SELECT type FROM Park")
    pk = []
    for result in cursor:
        pk.append(result["type"])
    cursor.close()
    if typee in pk:
        message = "The Type Has Already Existed!"
        return render_template("park.html", updateMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
        message = "The Park Does NOT Existed! "
        return render_template("park.html", updateMessage=message)
    
    g.conn.execute("""UPDATE Park SET (open_hour, type)
                = (%s, %s) WHERE pname = %s""", openHour, typee, pname)
    return redirect('/park')


@app.route('/addManager', methods=['POST'])
def addManager():
    mid = request.form['mid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    
    if mid == '':
      message = "MID cannot be NULL"
      return render_template("manager.html", addMessage=message)

    cursor = g.conn.execute("SELECT mid FROM Manager")
    pk = []
    for result in cursor:
      pk.append(result["mid"])
    cursor.close()
    if mid in pk:
      message = "The MID Has Already Existed!"
      return render_template("manager.html", addMessage=message)
    
    g.conn.execute("""INSERT INTO Manager(mid, first_name, last_name, work_time)
                VALUES(%s, %s, %s, %s)""", mid, firstName, lastName, workTime)
    return redirect('/manager')


@app.route('/deleteManager', methods=['POST'])
def deleteManager():
    mid = request.form['mid']
    
    cursor = g.conn.execute("SELECT mid FROM Manager")
    pk = []
    for result in cursor:
      pk.append(result["mid"])
    cursor.close()
    if mid not in pk:
      message = "The MID Does NOT Exist!"
      return render_template("manager.html", deleteMessage=message)
    
    g.conn.execute("""DELETE FROM Manager WHERE mid = %s""", mid)
    return redirect('/manager')


@app.route('/updateManager', methods=['POST'])
def updateManager():
    mid = request.form['mid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
     
    if mid == '':
      message = "MID cannot be NULL"
      return render_template("manager.html", updateMessage=message)

    cursor = g.conn.execute("SELECT mid FROM Manager")
    pk = []
    for result in cursor:
      pk.append(result["mid"])
    cursor.close()
    if mid not in pk:
      message = "The MID Does NOT Exist!"
      return render_template("manager.html", updateMessage=message)
    
    g.conn.execute("""UPDATE Manager SET (first_name, last_name, work_time)
                = (%s, %s, %s) WHERE mid = %s""", firstName, lastName, workTime, mid)
    return redirect('/manager')


@app.route('/searchTrainer', methods=['POST'])
def searchTrainer():
    aid = request.form['aid']

    if aid == '':
        message = "AID cannot be NULL"
        return render_template('index.html', searchMessage=message)
    
    cursor0 = g.conn.execute("SELECT aid FROM Animal_Founded")
    pk = []
    for result in cursor0:
        pk.append(result["aid"])
    cursor0.close()
    if aid not in pk:
        message = "The AID Does NOT Exist!"
        return render_template("index.html", searchMessage=message)

    cursor = g.conn.execute("""SELECT tid FROM Trained_By WHERE aid=%s""", aid)
    tid = []
    for result in cursor:
        tid.append(result["tid"])
    cursor.close()
    names = []
    for t in tid:
        cursor2 = g.conn.execute("""SELECT * FROM Trainer_Managed WHERE tid=%s""", t)
        for line in cursor2:
            tidd = line["tid"]
            firstName = line["first_name"]
            lastName = line["last_name"]
            name = tidd + " " + firstName + " " + lastName
            names.append(name)
        cursor2.close()
    context = dict(data=names)
    message = ", ".join(names)
    
    cursor3 = g.conn.execute("""SELECT bid FROM Breeded_By WHERE aid=%s""", aid)
    bid = []
    for result in cursor3:
        bid.append(result["bid"])
    cursor3.close()
    namess = []
    for t in bid:
        cursor4 = g.conn.execute("""SELECT * FROM Breeder_Managed WHERE bid=%s""", t)
        for line in cursor4:
            bidd = line["bid"]
            firstName = line["first_name"]
            lastName = line["last_name"]
            name = bidd + " " + firstName + " " + lastName
            namess.append(name)
        cursor4.close()
    message2 = ", ".join(namess)
    
    return render_template("indexSearch.html", trainerMessage=message,breederMessage=message2)


@app.route('/searchFood',methods=['POST'])
def searchFood():
    aid = request.form['aid']
    if aid == '':
        message = "AID cannot be NULL"
        return render_template('index.html',searchMessage=message)
    
    cursor0 = g.conn.execute("SELECT aid FROM Animal_Founded")
    pk = []
    for result in cursor0:
        pk.append(result["aid"])
    cursor0.close()
    if aid not in pk:
        message = "The AID Does NOT Exist!"
        return render_template("index.html", searchMessage=message)

    cursor = g.conn.execute("""SELECT fname FROM Eat WHERE aid=%s""",aid)
    food = []
    for line in cursor:
        food.append(line['fname'])
    cursor.close()
    message = ', '.join(food)
    return render_template("indexSearch.html",foodMessage=message)


@app.route('/checkStorage',methods = ['POST'])
def checkStorage():
    amount = request.form['amount']
    if amount == '':
        message ="Amount cannot be NULL"
        return render_template('food.html', searchMessage=message)
    else:
        amount = int(amount)

    if amount<0:
        message = "Amount should not be smaller than 0"
        return render_template('food.html', searchMessage=message)

    cursor = g.conn.execute("""SELECT amount FROM Food WHERE amount<%s""",amount)
    res = []
    for line in cursor:
        food = line['fname']
        storage = line['amount']
        tot = food + " " + storage
        res.append(tot)
    message0 = ", ".join(res)
    return render_template("foodSearch.html", foodMessage = message0)


@app.route('/searchShow',methods=['POST'])
def searchShow():
    sid = request.form['sid']
    if sid == '':
        message = "SID cannot be empty"
        return render_template("animalShow.html", searchMessage=message)

    cursor = g.conn.execute("SELECT sid FROM Animal_Show_Held")
    pk = []
    for result in cursor:
        pk.append(result["sid"])
    cursor.close()
    if sid not in pk:
        message = "The Show Does NOT Exist!"
        return render_template("animalShow.html", searchMessage=message)

    res = []
    cursor2 = g.conn.execute("""SELECT * FROM Participate_In WHERE sid=%s""", sid)
    for line in cursor2:
        aid = line["aid"]
        tid = line["tid"]
        tot = aid + " " + tid
        res.append(tot)
    cursor2.close()
    message = ", ".join(res)
    return render_template("animalShowSearch.html",searchMessage=message)


@app.route('/findFacility',methods=['POST'])
def findFacility():
    pname = request.form['pname']
    if pname == '':
        message = "Park Name cannot be NULL"
        return render_template("park.html", searchMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
        message = "The Park Does NOT Existed! "
        return render_template("park.html", searchMessage=message)

    res = []
    cursor = g.conn.execute("SELECT * FROM Facility_Located WHERE pname=%s",pname)
    for line in cursor:
        fid = line["fid"]
        typee = line["type"]
        name = line["name"]
        tot = fid + " " + typee + " " + name
        res.append(tot)
    cursor.close()
    message = ", ".join(res)
    return render_template("parkSearch.html",facilityMessage = message)


@app.route('/findAnimal',methods=['POST'])
def findAnimal():
    pname = request.form['pname']
    if pname == '':
        message = "Park Name cannot be NULL"
        return render_template("park.html", searchMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
        message = "The Park Does NOT Existed! "
        return render_template("park.html", searchMessage=message)

    cursor = g.conn.execute("SELECT * FROM Animal_Founded WHERE pname=%s",pname)
    res = []
    for line in cursor:
        aid = line['aid']
        species = line['species']
        tot = aid + " " + species
        res.append(tot)
    cursor.close()
    message = ", ".join(res)
    return render_template("parkSearch.html",animalMessage=message)


@app.route('/findShow',methods=['POST'])
def findShow():
    pname = request.form['pname']
    if pname == '':
        message = "Park Name cannot be NULL"
        return render_template("park.html", searchMessage=message)

    cursor2 = g.conn.execute("SELECT pname FROM Park")
    fk = []
    for line in cursor2:
        fk.append(line["pname"])
    cursor2.close()
    if pname not in fk:
        message = "The Park Does NOT Existed! "
        return render_template("park.html", searchMessage=message)

    cursor = g.conn.execute("SELECT * FROM Animal_Show_Held WHERE pname=%s", pname)
    res = []
    for line in cursor:
        sid = line['sid']
        showName = line['show_name']
        if showName == None:
            showName=' '
        tot = sid + " " + showName + " "
        res.append(tot)
    cursor.close()
    message = ", ".join(res)
    return render_template("parkSearch.html", showMessage=message)


@app.route('/findPark',methods=['POST'])
def findPark():
    typee = request.form['type']
    
    if typee == "":
        message = "Type cannot be NULL"
        return render_template("facility.html",searchMessage=message)
    
    res = []
    cursor = g.conn.execute("SELECT * FROM Facility_Located WHERE type=%s",typee)
    for line in cursor:
        parkname = line['pname']
        res.append(parkname)
    cursor.close()
    message = ", ".join(res)
    return render_template("facilitySearch.html",parkMessage=message)


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python3 server.py

    Show the help text using:

        python3 server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
