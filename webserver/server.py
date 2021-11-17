
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
  return render_template("index.html", **context)

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
    return render_template("animalShow.html", **context)


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

# Example of adding new data to the database
#@app.route('/add', methods=['POST'])
#def add():
#  name = request.form['name']
#  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#  return redirect('/')

@app.route('/addAnimal',methods=['POST'])
def addAnimal():
  aid = request.form['aid']
  species = request.form['species']
  age = int(request.form['age'])
  comesFrom = request.form['comes_from']
  eatingProperty = request.form['eating_property']
  activityTime = request.form['activity_time']
  lifestyle = request.form['lifestyle']
  pname = request.form['parkname']
  g.conn.execute("""INSERT INTO Animal_Founded(aid,species,age,comes_from,
                  eating_property,activity_time,lifestyle,pname)
                  VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""", 
                 aid, species, age, comesFrom,
                 eatingProperty, activityTime, lifestyle, pname)
  return redirect('/')


@app.route('/deleteAnimal', methods=['POST'])
def deleteAnimal():
    aid = request.form['aid']
    g.conn.execute("""DELETE FROM Animal_Founded WHERE aid = %s""", aid)
    return redirect('/')


@app.route('/updateAnimal', methods=['POST'])
def updateAnimal():
  aid = request.form['aid']
  species = request.form['species']
  age = int(request.form['age'])
  comesFrom = request.form['comes_from']
  eatingProperty = request.form['eating_property']
  activityTime = request.form['activity_time']
  lifestyle = request.form['lifestyle']
  pname = request.form['parkname']
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
    g.conn.execute("""INSERT INTO Breeder_Managed(bid, first_name,
                  last_name, work_time, mid)
                  VALUES(%s, %s, %s, %s, %s)""",
                   bid, firstName, lastName, workTime, mid)
    return redirect('/breeder.html')


@app.route('/deleteBreeder', methods=['POST'])
def deleteBreeder():
    bid = request.form['bid']
    g.conn.execute("DELETE FROM Breeder_Managed WHERE bid = %s", bid)
    return redirect('/breeder.html')


@app.route('/updateBreeder', methods=['POST'])
def updateBreeder():
    bid = request.form['bid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    mid = request.form['mid']
    g.conn.execute("""UPDATE Breeder_Managed SET (first_name,
                  last_name, work_time, mid) = (%s, %s, %s, %s)
                  WHERE bid = %s""",
                   firstName, lastName, workTime, mid, bid)
    return redirect('/breeder.html')


@app.route('/addTrainer', methods=['POST'])
def addTrainer():
    tid = request.form['tid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    mid = request.form['mid']
    g.conn.execute("""INSERT INTO Trainer_Managed(tid, first_name,
              last_name, work_time, mid)
              VALUES(%s, %s, %s, %s, %s)""",
                   tid, firstName, lastName, workTime, mid)
    return redirect('/another.html')


@app.route('/deleteTrainer', methods=['POST'])
def deleteTrainer():
    tid = request.form['tid']
    g.conn.execute("DELETE FROM Trainer_Managed WHERE tid = %s", tid)
    return redirect('/another.html')


@app.route('/updateTrainer', methods=['POST'])
def updateTrainer():
    tid = request.form['tid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    mid = request.form['mid']
    g.conn.execute("""UPDATE Trainer_Managed SET (first_name,
              last_name, work_time, mid) = (%s, %s, %s, %s)
              WHERE tid = %s""",
                   firstName, lastName, workTime, mid, tid)
    return redirect('/another.html')


@app.route('/addFood', methods=['POST'])
def addFood():
    fname = request.form['fname']
    timePurchased = request.form['time_purchased']
    brand = request.form['brand']
    unitPrice = request.form['unit_price']
    amount = request.form['amount']
    g.conn.execute("""INSERT INTO Food(fname, time_purchased, brand
                unit_price, amount)
                VALUES(%s, %s, %s, %s, %s)""",
                   fname, timePurchased, brand, unitPrice, amount)
    return redirect('/food.html')


@app.route('/deleteFood', methods=['POST'])
def deleteFood():
    fname = request.form['fname']
    g.conn.execute("""DELETE FROM Food WHERE fname = %s""", fname)
    return redirect('/food.html')


@app.route('/updateFood', methods=['POST'])
def updateFood():
    fname = request.form['fname']
    timePurchased = request.form['time_purchased']
    brand = request.form['brand']
    unitPrice = request.form['unit_price']
    amount = request.form['amount']
    g.conn.execute("""UPDATE Food SET (time_purchased, brand
                unit_price, amount) = (%s, %s, %s, %s)
                WHERE fname = %s""",
                   timePurchased, brand, unitPrice, amount, fname)
    return redirect('/food.html')


@app.route('/addAnimalShow', methods=['POST'])
def addAnimalShow():
    sid = request.form['sid']
    showName = request.form['show_name']
    seat = request.form['seat']
    time = request.form['time']
    pname = request.form['pname']
    g.conn.execute("""INSERT INTO Animal_Show_Held(sid, show_name,
                seat, time, pname) VALUES(%s, %s, %s, %s, %s)""",
                   sid, showName, seat, time, pname)
    return redirect('/animalShow.html')


@app.route('/deleteAnimalShow', methods=['POST'])
def deleteAnimalShow():
    sid = request.form['sid']
    g.conn.execute("DELETE FROM Animal_Show_Held WHERE sid = %", sid)
    return redirect('/animalShow.html')


@app.route('/updateAnimalShow', methods=['POST'])
def updateAnimalShow():
    sid = request.form['sid']
    showName = request.form['show_name']
    seat = request.form['seat']
    time = request.form['time']
    pname = request.form['pname']
    g.conn.execute("""UPDATE Animal_Show_Held SET (show_name,
                seat, time, pname) = (%s, %s, %s, %s)
                WHERE sid = %s""",
                   showName, seat, time, pname, sid)
    return redirect('/animalShow.html')


@app.route('/addFacility', methods=['POST'])
def addFacility():
    fid = request.form['fid']
    type = request.form['type']
    name = request.form['name']
    openHour = request.form['open_hour']
    pname = request.form['pname']
    g.conn.execute("""INSERT INTO Facility_Located(fid, type, name,
                open_hour, pname) VALUES(%s, %s, %s, %s, %s)""",
                   fid, type, name, openHour, pname)
    return redirect('/facility.html')


@app.route('/deleteFacility', methods=['POST'])
def deleteFacility():
    fid = request.form['fid']
    g.conn.execute("DELETE FROM Facility_Located WHERE fid = %s", fid)
    return redirect('/facility.html')


@app.route('/updateFacility', methods=['POST'])
def updateFacility():
    fid = request.form['fid']
    type = request.form['type']
    name = request.form['name']
    openHour = request.form['open_hour']
    pname = request.form['pname']
    g.conn.execute("""UPDATE Facility_Located SET (type, name,
                open_hour, pname) = (%s, %s, %s, %s)
                WHERE fid = %s""",
                   type, name, openHour, pname, fid)
    return redirect('/facility.html')


@app.route('/addPark', methods=['POST'])
def addPark():
    pname = request.form['pname']
    openHour = request.form['open_hour']
    type = request.form['type']
    g.conn.execute("""INSERT INTO Park(pname, open_hour, type)
                VALUES (%s, %s, %s)""", pname, openHour, type)
    return redirect('/park.html')


@app.route('/deletePark', methods=['POST'])
def deletePark():
    pname = request.form['pname']
    g.conn.execute('DELETE FROM Park WHERE pname = %s', pname)
    return redirect('/park.html')


@app.route('/updatePark', methods=['POST'])
def updatePark():
    pname = request.form['pname']
    openHour = request.form['open_hour']
    type = request.form['type']
    g.conn.execute("""UPDATE Park(open_hour, type)
                = (%s, %s) WHERE pname = %s""", openHour, type, pname)
    return redirect('/park.html')


@app.route('/addManager', methods=['POST'])
def addManager():
    mid = request.form['mid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    g.conn.execute("""INSERT INTO Manager(mid, first_name, last_name, work_time)
                VALUES(%s, %s, %s, %s)""", mid, firstName, lastName, workTime)
    return redirect('/manager.html')


@app.route('/deleteManager', methods=['POST'])
def deleteManager():
    mid = request.form['mid']
    g.conn.execute("""DELETE FROM Manager WHERE mid = %s""", mid)
    return redirect('/manager.html')


@app.route('/updateManager', methods=['POST'])
def updateManager():
    mid = request.form['mid']
    firstName = request.form['first_name']
    lastName = request.form['last_name']
    workTime = request.form['work_time']
    g.conn.execute("""UPDATE Manager(first_name, last_name, work_time)
                = (%s, %s, %s) WHERE mid = %s""", firstName, lastName, workTime, mid)
    return redirect('/manager.html')


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
