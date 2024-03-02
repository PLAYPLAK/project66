from mysql import connector
import ast

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

    def study_plan(self, day_name, start_time, end_time, day_ID, subject, UserID):
        times = str([start_time, end_time])        
        value = (day_name, times, subject, int(UserID), int(day_ID))
        query1 = "SELECT * FROM study_plan WHERE UserID = %s AND day_ID = %s AND time = %s"
        self.cursor.execute(query1, (UserID, day_ID, times))
        results = self.cursor.fetchall()

        if results:
            for result in results:
                planID, dayName, time, subjectName, retrieved_UserID, day_ID2 = result

                if (time == times) and (subjectName != subject) and (day_ID == day_ID2) :
                    query = "UPDATE study_plan SET subjectName = %s WHERE UserID = %s AND time = %s AND  day_ID = %s"
                    self.cursor.execute(query, (subject, UserID, time, day_ID))
                    self.conn.commit()
                    print("Update")
                    break

        else :
            query = "INSERT INTO study_plan ( dayName, time, subjectName, UserID, day_ID) VALUES ( %s, %s, %s, %s, %s)"
            self.cursor.execute(query, value)
            self.conn.commit()
            print(f"User with ID {UserID} inserted successfully.")


    def study_plan_view(self, UserID, day_ID):

        day = []
        times = []
        subject = []
        day_num = [] 

        if int(day_ID) == 8 :
            print("yess")
            query = "SELECT * FROM study_plan WHERE UserID = %s"
            self.cursor.execute(query, (UserID, ))
            results = self.cursor.fetchall()


            for result in results :
                planID, dayName, time, subjectName, retrieved_UserID, day_ID2 = result
                day.append(dayName)
                times.append(time)
                subject.append(subjectName)
                day_num.append(day_ID2)
                
            # Combine lists into a list of tuples
            data = list(zip(day, times, subject, day_num))

            # Sort the list of tuples by day_num and then times
            sorted_data = sorted(data, key=lambda x: (x[3], eval(x[1])))

            # Unpack the sorted data into separate lists
            sorted_day, sorted_times, sorted_subject, sorted_day_num = zip(*sorted_data)

            return sorted_day, sorted_times, sorted_subject, sorted_day_num

        else :
            query = "SELECT * FROM study_plan WHERE UserID = %s AND day_ID = %s "
            self.cursor.execute(query, (UserID, day_ID))
            results = self.cursor.fetchall()
            for result in results :
                planID, dayName, time, subjectName, retrieved_UserID, day_ID2 = result
                day.append(dayName)
                times.append(time)
                subject.append(subjectName)
                day_num.append(day_ID2)

        # Zip the lists into pairs 
        pairs = list(zip(day, times, subject, day_num))

        # Custom key function to extract the starting time from the time range string
        def start_time_key(pair):
            start_time = eval(pair[1])[0]
            return start_time

        # Sort the pairs based on the starting time
        sorted_pairs = sorted(pairs, key=start_time_key)
        # Unzip the sorted pairs
        sorted_day, sorted_times, sorted_subject, sorted_day_num = zip(*sorted_pairs)

        return sorted_day, sorted_times, sorted_subject, sorted_day_num

    def insert_feedback_gui(self, GuildID, channel_reply):
        query = "INSERT INTO user ( StudentID, FullNameTH, FullNameENG, UserID, Phone, Email) VALUES (%s, %s, %s, %s, %s, %s);"
        value = ( int(StudentID), FullNameTH, FullNameENG, int(UserID), Phone, Email)
        self.cursor.execute(query, value)
        self.conn.commit()
        pass

    def check_feedback_gui(self):       
        value = (day_name, times, subject, int(UserID), int(day_ID))
        query1 = "SELECT * FROM study_plan WHERE UserID = %s AND day_ID = %s AND time = %s"
        self.cursor.execute(query1, (UserID, day_ID, times))
        results = self.cursor.fetchall()
        pass

    def insert_feedback_ch(self):
        query = "INSERT INTO user ( StudentID, FullNameTH, FullNameENG, UserID, Phone, Email) VALUES (%s, %s, %s, %s, %s, %s);"
        value = ( int(StudentID), FullNameTH, FullNameENG, int(UserID), Phone, Email)
        self.cursor.execute(query, value)
        self.conn.commit()
        pass

    def check_feedback_ch(self, function):       
        value = (day_name, times, subject, int(UserID), int(day_ID))
        query1 = "SELECT * FROM study_plan WHERE UserID = %s AND day_ID = %s AND time = %s"
        self.cursor.execute(query1, (UserID, day_ID, times))
        results = self.cursor.fetchall()
        pass

    def profile(self, memberID, key):
        query = "SELECT * FROM user WHERE UserID = %s"
        self.cursor.execute(query, (int(memberID),))
        result = self.cursor.fetchone()
        StudentID, FullNameTH, FullNameENG, UserID, Phone, Email = result

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



db = Database()



