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

    def study_plan(self, day_name, start_time, end_time, subject, StudentID, UserID):        
        value = (day_name, start_time, end_time, subject, int(StudentID), int(UserID))
        query = "SELECT * FROM study_plan WHERE StudentID = %s"
        self.cursor.execute(query, (StudentID,))
        result = self.cursor.fetchone()

        if result is not None:
            planID, dayName, time_Start, time_End, subjectName, retrieved_StudentID, retrieved_UserID = result

            if len(start_time) and len(time_End) and len(subject) == 2 :

                n1 = str([ time_Start[1], start_time])
                n2 = str([ time_End[1], end_time])
                n3 = str([ subjectName[1], subject])
            else :
                n1 = str([ time_Start, start_time])
                n2 = str([ time_End, end_time])
                n3 = str([ subjectName, subject])

        if not result is not None :
            query = "INSERT INTO study_plan ( dayName, time_Start, time_End, subjectName, StudentID, UserID) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, value)
            self.conn.commit()
            print(f"User with ID {StudentID} inserted successfully.")
        else :
            # If the user already exists, perform an update
            # query = "UPDATE study_plan SET time_Start = %s, time_End = %s, subjectName = %s WHERE StudentID = %s"
            query = "UPDATE study_plan SET time_Start = COALESCE(%s, time_Start), time_End = COALESCE(%s, time_End), subjectName = COALESCE(%s, subjectName) WHERE StudentID = %s"
            # data = (str([time_Start, start_time]), str([time_End,end_time]), str([ subjectName, subject]), StudentID)
            data = (str(n1), str(n2), str(n3), StudentID)
            self.cursor.execute(query, data)
            self.conn.commit()
            print(f"User with ID {StudentID} updated successfully.")


    

    def study_plan_view(self, ID):
        query = "SELECT * FROM study_plan WHERE StudentID = %s"
        self.cursor.execute(query, (ID,))
        result = self.cursor.fetchone()
        planID, dayName, time_Start, time_End, subjectName, retrieved_StudentID, retrieved_UserID = result

        return dayName 

    def insert_feedback_gui(self):
        pass

    def check_feedback_gui(self):
        pass

    def insert_feedback_ch(self):
        pass

    def check_feedback_ch(self, function):
        pass

    def profile(self, memberID, key):
        query = "SELECT * FROM user WHERE UserID = %s"
        self.cursor.execute(query, (int(memberID),))
        result = self.cursor.fetchone()
        StudentID, FullNameTH, FullNameENG, UserID, Phone, Email =result

        if str(key) == "TH" :
            return str(FullNameTH)
        elif str(key) == "ENG" :
            return str(FullNameENG)
        elif str(key) == "ID" :
            return str(StudentID)
        elif str(key) == "Phone" :
            return str(Phone)
        elif str(key) == "Email" :
            return str(Email)
        else :
            return "None"    

    # def delete_user(self, uid):
    #     qurey = "DELETE FROM tableclassup WHERE id = %s;"
    #     self.cursor.execute(qurey, (uid,))
    #     self.conn.commit()

db = Database()
# db.register_user(64015134, "ศรัณญ์", "Saran", 12345679, "0902349731", "Plak@gmail.com")
# # db.study_plan( "วันจันทร์","08:00", "16:00", "ภาษาไทย", 64015134, 12345678)
# # db.study_plan( "วันจันทร์","08:30", "10:30", "ภาษาไทย", 64015134, 12345678)
# db.study_plan( "🔴 Sunday - วันอาทิตย์","08:30", "10:30", "ภาษาไทย", 64015135, 12345679)
# db.study_plan( "🔴 Sunday - วันอาทิตย์","13:00", "16:00", "ภาษาไทย2", 64015135, 12345679)

print(db.profile(12345678,"TH"))