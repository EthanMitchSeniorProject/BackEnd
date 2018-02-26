import pyodbc

class DatabaseConnection:
    @staticmethod
    def getConnection():
        server = 'calvinscoutingreport.database.windows.net'
        database = 'ScoutingReport'
        username = 'athlete'
        password = 'calvinscoutingreport123!'
        driver = '{ODBC Driver 13 for SQL Server}'
        connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;Server='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
        return connection