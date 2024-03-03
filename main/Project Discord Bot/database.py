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

    def register_user(self, StudentID, FullNameTH, FullNameENG, UserID, GuildID, profile, Phone = "-", Email = "-"):
        query1 = "SELECT * FROM user WHERE UserID = %s"
        self.cursor.execute(query1, (UserID,))
        results = self.cursor.fetchall()

        if results:
            query2 = "INSERT INTO member ( EuserID, EguilID, profilename, StudentID) VALUES (%s, %s, %s, %s);"
            value = ( int(UserID), int(GuildID), str(profile), int(StudentID))
            self.cursor.execute(query2, value)
            self.conn.commit()
            print("ADD Member")


        else :

            query = "INSERT INTO user ( FullNameTH, FullNameENG, UserID, Phone, Email) VALUES (%s, %s, %s, %s, %s);"
            value = ( FullNameTH, FullNameENG, int(UserID), Phone, Email)
            self.cursor.execute(query, value)
            self.conn.commit()
            print("ADD User")

            query2 = "INSERT INTO member ( EuserID, EguilID, profilename, StudentID) VALUES (%s, %s, %s, %s);"
            value = ( int(UserID), int(GuildID), str(profile), int(StudentID))
            self.cursor.execute(query2, value)
            self.conn.commit()
            print("ADD Member")


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


        query = "SELECT * FROM study_plan WHERE UserID = %s AND day_ID = %s "
        self.cursor.execute(query, (UserID, day_ID))
        results = self.cursor.fetchall()


        if results :
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
        
        else :
            return None,None,None,None
    # insert ข้อความ alert
    def insert_alert_gui(self, GuildID, alert_Msg, adminID):
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (int(GuildID),))
        results = self.cursor.fetchone()

        if results :
            query = "UPDATE guild SET Alert_Msg = %s WHERE GuildID = %s"
            self.cursor.execute(query, (str(alert_Msg), int(GuildID)))
            self.conn.commit()
            print("Update Alert")
        else :
            query = "INSERT INTO guild ( GuildID, Alert_Msg, FadminID) VALUES (%s, %s, %s);"
            value = ( int(GuildID), str(alert_Msg), int(adminID))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("Insert Alert")

    # check ข้อความ alert
    def check_alert_gui(self, guildID):       
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (guildID,))
        results = self.cursor.fetchall()
        
        if results :
            GuildID, GuilName, Alert_Msg, FUserID = results
            return str(Alert_Msg)

        else:
            return ""

    def insert_feedback_ch(self, FuncName, channel_reply, GuildID):
        query1 = "SELECT * FROM function_ch WHERE FGuildID = %s AND FuncName = %s"
        self.cursor.execute(query1, (GuildID, str(FuncName)))
        results = self.cursor.fetchone()

        if results:
            query = "UPDATE function_ch SET CH_ReplyFuncID = %s WHERE FGuildID = %s AND FuncName = %s"
            self.cursor.execute(query, (str(channel_reply), int(GuildID), str(FuncName)))
            self.conn.commit()
            print("Update CH")

        else :
            query = "INSERT INTO function_ch ( FuncName, CH_ReplyFuncID, FGuildID) VALUES (%s, %s, %s);"
            value = ( str(FuncName), str(channel_reply), int(GuildID))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("Insert CH")

    def check_feedback_ch(self, FuncName, GuildID):       
        query1 = "SELECT * FROM function_ch WHERE FGuildID = %s AND FuncName = %s"
        self.cursor.execute(query1, (GuildID, FuncName))
        results = self.cursor.fetchone()

        if results:
            funcID,funcName,CH_Reply,FguilID = results
            return list(CH_Reply)
        
        else:
            return []

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

    def question_ans(self, Word, resMsg, guildID, type_ans):

        query = "INSERT INTO response_msg ( Word, ResMsg, FGuildID, type_ans) VALUES (%s, %s, %s, %s);"
        value = ( str(Word), str(resMsg), int(guildID), int(type_ans))
        self.cursor.execute(query, value)
        self.conn.commit()
        print("Insert QA")


    def check_question_ans(self, GuildID):
        query1 = "SELECT * FROM response_msg WHERE FGuildID = %s"
        self.cursor.execute(query1, (int(GuildID), ))
        results = self.cursor.fetchall()
        words = []
        answers = []
        types = []
        if results:
            for result in results :
                resID, word, resMsg, fguildID, type_ans = result
                words.append(word)
                answers.append(resMsg)
                types.append(type_ans)

            return words, answers, type_ans

        else :
            return [], [], []
        
    def delete_question(self,):
        pass

    def add_guild(self, GuildID, FadminID, Alert_Msg=""):
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (int(GuildID), ))
        result = self.cursor.fetchone()

        if result is not None:
            print("NOT ADD GUILD")

        else:
            query = "INSERT INTO guild ( GuildID, Alert_Msg, FadminID) VALUES (%s, %s, %s);"
            value = ( int(GuildID), str(Alert_Msg), int(FadminID))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("ADD GUILD")

    def add_admin(self, adminID, Name):
        query1 = "SELECT * FROM admin WHERE adminID = %s"
        self.cursor.execute(query1, (int(adminID), ))
        result = self.cursor.fetchone()
    
        if result is not None:
            print("NOT ADD ADMIN")

        else:
            query = "INSERT INTO admin ( adminID, name) VALUES (%s, %s);"
            value = ( int(adminID), str(Name))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("ADD ADMIN")



db = Database()

