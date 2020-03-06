from PySide import QtGui, QtCore
import sys
import psycopg2
class QueryDB(QtGui.QMainWindow):
   def __init__(self):
      QtGui.QMainWindow.__init__(self)
      # Step 5
      self.conn_string=""
      self.initMenu()
      self.initUI()
      self.setGeometry(50,50,700,600)
      self.setWindowTitle("Database Query Tool")
      self.show()

   def initUI(self):
      self.tabwidget = QtGui.QTabWidget()
      self.setCentralWidget(self.tabwidget)
      self.tab1 = QtGui.QWidget()
      self.tab2 = QtGui.QWidget()
      self.tabwidget.addTab(self.tab1,"Set Database")
      self.tabwidget.addTab(self.tab2,"Query Database")
      self.initTab1()
      self.initTab2()

   def initTab2(self):
      tab2Layout = QtGui.QVBoxLayout()
      self.tab2.setLayout(tab2Layout)
      splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
      splitter.setLayout(QtGui.QVBoxLayout())
      top = QtGui.QFrame(self)
      top.setFrameShape(QtGui.QFrame.StyledPanel)
      topLayout = QtGui.QVBoxLayout()
      top.setLayout(topLayout)
      self.text_area = QtGui.QTextEdit(self)
      self.text_area.setMaximumHeight(70)
      topLayout.addWidget(self.text_area)
      button_area = QtGui.QFrame(self)
      button_areaLayout = QtGui.QHBoxLayout()
      button_areaLayout.addStretch(1)
      button_area.setLayout(button_areaLayout)
      ok_button2 = QtGui.QPushButton("OK",self)
      ok_button2.clicked.connect(self.runQuery)
      button_areaLayout.addWidget(ok_button2)
      topLayout.addWidget(button_area)
      bottom = QtGui.QFrame(self)
      bottomLayout2 = QtGui.QVBoxLayout()
      bottom.setLayout(bottomLayout2)
      self.table = QtGui.QTableWidget(1,4)
      bottomLayout2.addWidget(self.table)
      splitter.addWidget(top)
      splitter.addWidget(bottom)
      tab2Layout.addWidget(splitter)
      splitter.setStretchFactor(1,10)

   def runQuery(self):
      sql = self.text_area.toPlainText()
      cursor = self.conn.cursor()
      cursor.execute(sql)
      results = cursor.fetchall()
      #self.text_area.setPlainText(str(results))
      columnLabels = [desc[0] for desc in cursor.description]
      self.table.setColumnCount(len(columnLabels))
      self.table.setHorizontalHeaderLabels(columnLabels)
      self.table.setRowCount(len(results))
      for i in range(0, len(results)):
         for j in range(0, len(results[i])):
            val = str(results[i][j])
            item = QtGui.QTableWidgetItem(val)
            self.table.setItem(i, j,item)
      self.table.resizeColumnsToContents()

   def initTab1(self):
      tab1Layout = QtGui.QVBoxLayout()
      self.tab1.setLayout(tab1Layout)
      splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
      splitter.setLayout(QtGui.QVBoxLayout())
      tab1Layout.addWidget(splitter)
      top = QtGui.QFrame(self)
      gridLayout = QtGui.QGridLayout()
      gridLayout.setHorizontalSpacing(20)
      top.setLayout(gridLayout)
      host_label = QtGui.QLabel("Host: ")
      gridLayout.addWidget(host_label,0,0)
      self.host_edit = QtGui.QLineEdit(self)
      self.host_edit.setText("localhost")
      gridLayout.addWidget(self.host_edit,0,1)
      gridLayout.addWidget(QtGui.QLabel("dbname:"),1,0)
      self.dbname_edit = QtGui.QLineEdit(self)
      gridLayout.addWidget(self.dbname_edit,1,1)
      gridLayout.addWidget(QtGui.QLabel("user:"),2,0)
      self.user_edit = QtGui.QLineEdit(self)
      gridLayout.addWidget(self.user_edit,2,1)
      gridLayout.addWidget(QtGui.QLabel("password"),3,0)
      self.password_edit = QtGui.QLineEdit(self);
      self.password_edit.setEchoMode(QtGui.QLineEdit.Password)
      gridLayout.addWidget(self.password_edit,3,1)
      ok_button = QtGui.QPushButton("OK",self)
      ok_button.clicked.connect(self.setDatabase)
      gridLayout.addWidget(ok_button,4,1)
      self.dbstatus = QtGui.QLabel("Not connected")
      gridLayout.addWidget(self.dbstatus,4,2)
      bottom = QtGui.QFrame(self)
      bottomLayout = QtGui.QVBoxLayout()
      bottom.setLayout(bottomLayout)
      bottomLayout.addWidget(QtGui.QLabel("Tables and Views"))
      self.table_area = QtGui.QTextEdit(self)
      bottomLayout.addWidget(self.table_area)
      splitter.addWidget(top)
      splitter.addWidget(bottom)
      splitter.setStretchFactor(1,1)

   def setDatabase(self):
      host = self.host_edit.text()
      dbname = self.dbname_edit.text()
      user = self.user_edit.text()
      password = self.password_edit.text()
      self.conn_string = "host='" + host.strip()
      self.conn_string += "' dbname='" + dbname.strip()
      self.conn_string += "' user='" + user.strip()
      self.conn_string += "' password='" + password.strip()
      self.conn_string += "'"
      self.table_area.setText("conn_string: " +
         self.conn_string)
      try:
         self.conn = psycopg2.connect(self.conn_string)
         self.dbstatus.setText("Connected to " + dbname)
         cursor = self.conn.cursor()
         sql = "select tablename from pg_catalog.pg_tables "
         sql += " where schemaname='public'"
         cursor.execute(sql)
         table_results = cursor.fetchall()
         sql = "select viewname from pg_catalog.pg_views "
         sql += " where schemaname='public'"
         cursor.execute(sql)
         view_results = cursor.fetchall()
         table_text = "tables:\n"
         for i in range(0, len(table_results)):
            table_text += table_results[i][0]
            if (i < len(table_results) - 1):
               table_text += ","
         table_text += "\n"
         self.table_area.setText(table_text)
         view_text = "\nviews:\n"
         for i in range(0, len(view_results)):
            view_text += view_results[i][0]
            if (i < len(view_results) - 1):
               view_text += ","
         self.table_area.append(view_text)
      except psycopg2.DatabaseError:
         self.dbstatus.setText("Error Connecting")
         self.table_area.setText("Could not connect to database")
         
   # Step 6
   def initDatabase(self):
      print("Inside initDatabase")
      if self.conn_string=="":
         self.msg = QtGui.QMessageBox(self)
         self.msg.setText("Connect to database first")
         self.msg.exec_()
      else:
         print("Initializing")
         filename,_=QtGui.QFileDialog.getOpenFileName(self,"Open File",".")
         conn = psycopg2.connect(self.conn_string)
         cursor = conn.cursor()
         infile = open(filename,"r")
         sql = infile.read()
         infile.close()
         cursor.execute(sql)
         conn.commit()
         conn.close()
         # Call setDatabase to allow the table names to show up on the GUI
         self.setDatabase
         self.msg = QtGui.QMessageBox(self)
         self.msg.setText("Database Initialized Successfully.")
         self.msg.exec_()
		

   def initMenu(self):
      menubar = self.menuBar()
      fileMenu = menubar.addMenu("File")
      # Step 1 
      # Create an action item
      createDB = QtGui.QAction("Create DB",self)
      # Associate a function with the action item
      createDB.triggered.connect(self.createDatabase)
      # Add item to file menu
      fileMenu.addAction(createDB)
      # step 4
      initDB = QtGui.QAction("Initialize DB",self)
      initDB.triggered.connect(self.initDatabase)
      fileMenu.addAction(initDB)
      
      
      quit = QtGui.QAction("Quit",self)
      quit.triggered.connect(self.close)
      fileMenu.addAction(quit)
      
   # step 3
   def create(self):
	   if self.dbBox.text().strip()=="" :
		   self.msg = QtGui.QMessageBox(self)
		   self.msg.setText("Empty name is not allowed")
		   self.msg.exec_()
	   else: 
		   print("Creating " +self.dbBox.text().strip()+" database")
		   self.myDialog.done(0)
		   conn_string = "host='localhost' dbname='cent280db' "
		   conn_string += "user='cent280man' password='pgsql_man'"
		   conn = psycopg2.connect(conn_string)
		   conn.autocommit = True
		   cursor = conn.cursor()
		   sql = "drop database if exists " +self.dbBox.text().strip()+";"
		   cursor.execute(sql)
		   sql = "create database " +self.dbBox.text().strip()+ " owner bob;"
		   cursor.execute(sql)
		   conn.close()
		   self.msg = QtGui.QMessageBox(self)
		   self.msg.setText("Database has been created.")
		   self.msg.exec_()
		   
   
      
   def createDatabase(self):
	   #Step 2
	   print("In create database")
	   # Create a dialog box
	   self.myDialog = QtGui.QDialog(self)
	   self.myDialog.setWindowTitle("Create Database")
	   # Create a grid layout
	   layout = QtGui.QGridLayout()
	   label = QtGui.QLabel("Give a name:")
	   self.dbBox = QtGui.QLineEdit()
	   layout.addWidget(label,0,0)
	   layout.addWidget(self.dbBox,0,1)
	   # Add Ok and Cancel buttons
	   buttons = QtGui.QDialogButtonBox()
	   buttons.setOrientation(QtCore.Qt.Horizontal)
	   buttons.addButton("Cancel",QtGui.QDialogButtonBox.RejectRole)
	   buttons.addButton("Ok",QtGui.QDialogButtonBox.AcceptRole)
	   # Connect the Ok button to create function
	   self.myDialog.connect(buttons,QtCore.SIGNAL("accepted()"),self.create)
	   # Connect the Cancel with closing the dialog
	   self.myDialog.connect(buttons,QtCore.SIGNAL("rejected()"),self.myDialog.close)
	   # Add buttons to the dialog box at row 1 column 0 with rowspan 1 and columnspan 1
	   layout.addWidget(buttons,1,0,1,1,QtCore.Qt.AlignCenter)
	   # Add layout to dialog
	   self.myDialog.setLayout(layout)
	   # Run the dialog
	   self.myDialog.exec_()
	   

app = QtGui.QApplication(sys.argv)
mygui = QueryDB()
sys.exit(app.exec_())
