from mysql import connector

PASSWORD = '' 
HOST = '127.0.0.1'
USERNAME = 'root'
PORT = 3306
DATABASE_NAME = 'classup'

class Database:
    def __init__(self):
        try:
            self.conn = connector.connect(
                host=HOST,
                user=USERNAME,  
                password=PASSWORD,
                database=DATABASE_NAME,
                port=PORT,
            )
            self.cursor = self.conn.cursor()
            print("Connected to the database")
        except connector.Error as err:
            print(f"Error: {err}")
            raise  # Re-raise the exception to indicate the failure

    def close_connection(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Connection closed")

    def register_user(self, StudentID, FullNameTH, FullNameENG, UserID, Phone = "-", Email = "-"):
        query = "INSERT INTO user ( StudentID, FullNameTH, FullNameENG, UserID, Phone, Email) VALUES (%s, %s, %s, %s, %s, %s);"
        value = ( int(StudentID), FullNameTH, FullNameENG, int(UserID), Phone, Email)
        self.cursor.execute(query, value)
        self.conn.commit()

    def study_plan(self,):
        pass



    # def delete_user(self, uid):
    #     qurey = "DELETE FROM tableclassup WHERE id = %s;"
    #     self.cursor.execute(qurey, (uid,))
    #     self.conn.commit()

# db = Database()
# db.register_user(64015135, "ศรัณญ์", "Saran", 223456789, "0902349731", "Plak@gmail.com")