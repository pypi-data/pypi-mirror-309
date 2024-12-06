# Import SQLITE Module
import sqlite3

__version__ = '1.1.1'

class Database:

    # Connection to Database
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    # Execution of SQL Commands
    def execute(self, command, *args):

        try:
            # .schema Command
            if command == ".schema;":

                # return Value
                rV = []

                # Return Dictionary with Name of Row & Value
                self.conn.row_factory = sqlite3.Row

                # Create A Cursor
                c = self.conn.cursor()
                # Execute Command
                c.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
                
                # Fetch All The Tables
                rows = c.fetchall()

                # Return a List of Dictionary Values
                for row in rows:
                    rV.append(dict(row))

                # Commit the Command
                self.conn.commit()

                # Print Value if its Main File
                if __name__ == '__main__':
                    print(rV)

                # Return The Return Value List if it has atleast 1 element and the status of command
                return (rV if len(rV) != 0 else None), "Output Returned"


            # For SELECT Commands
            elif "SELECT" in command[0:8].upper():

                # return Value initialization
                rV = []

                # Return Dictionary with Name of Row & Value
                self.conn.row_factory = sqlite3.Row

                # Create A Cursor
                c = self.conn.cursor()
                # Execute Command
                c.execute(command, *args)

                # Fetch All the Rows
                rows = c.fetchall()

                # Append the rows to return Value as dict
                for row in rows:
                    rV.append(dict(row))

                # Commit the Command
                self.conn.commit()

                # Print Return Value if it is main file
                if __name__ == '__main__':
                    print(rV)

                # Return the return value if it has atleast 1 element and the status
                return (rV if len(rV) != 0 else None), "Output Returned"

            elif "RETURNING" in command.upper():
                # return Value initialization
                rV = []
                
                c = self.conn.cursor()
                c.execute(command, *args)
                # Fetch All the Rows
                rows = c.fetchall()
                self.conn.commit()

                # Append the rows to return Value as dict
                for row in rows:
                    rV.append(dict(row))

                # Return the return value if it has at least 1 element and the status
                return (rV if len(rV) != 0 else None), "Command Executed"
            
            else:
                c = self.conn.cursor()
                c.execute(command, *args)
                self.conn.commit()
                return None, "Command Executed"

        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
            raise Exception(e)


    def __del__(self):
        self.conn.close()


# If this is the main file
if __name__ == '__main__':

    db = Database(input("Enter File Name: "))
    try:
        while True:
            db.execute(input(">>> "))

    except KeyboardInterrupt:
        quit()
