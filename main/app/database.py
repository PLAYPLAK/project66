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

    def register_user(self, StudentID, FullNameTH, FullNameENG, UserID, profile, GuildID, Phone = "-", Email = "-"):
        query1 = "SELECT * FROM user WHERE UserID = %s"
        self.cursor.execute(query1, (UserID,))
        results = self.cursor.fetchall()

        if results:
            query1 = "SELECT * FROM member WHERE UserID = %s and StudentID = %s and GuildID = %s"
            self.cursor.execute(query1, (str(UserID), str(StudentID), str(GuildID)))
            result_a = self.cursor.fetchone()
            if result_a :
                query = "UPDATE member SET profilename = %s WHERE UserID = %s AND GuildID = %s"
                self.cursor.execute(query, (str(profile), str(UserID), str(GuildID)))
                self.conn.commit()
            else :
                query2 = "INSERT INTO member (  UserID, GuildID, profilename, StudentID) VALUES (%s, %s, %s, %s);"
                value = ( str(UserID), str(GuildID), str(profile), str(StudentID))
                self.cursor.execute(query2, value)
                self.conn.commit()
                print("ADD Member")
            # query1 = "SELECT * FROM member WHERE UserID = %s and StudentID = %s"
            # self.cursor.execute(query1, (str(UserID), str(StudentID)))
            # result_a = self.cursor.fetchall()

        else :

            query = "INSERT INTO user ( FullNameTH, FullNameENG, UserID, Phone, Email) VALUES (%s, %s, %s, %s, %s);"
            value = ( FullNameTH, FullNameENG, str(UserID), Phone, Email)
            self.cursor.execute(query, value)
            self.conn.commit()
            print("ADD User")

            query2 = "INSERT INTO member ( UserID, GuildID, profilename, StudentID) VALUES (%s, %s, %s, %s);"
            value = ( str(UserID), str(GuildID), str(profile), str(StudentID))
            self.cursor.execute(query2, value)
            self.conn.commit()
            print("ADD Member")

    def study_plan(self, day_name, start_time, end_time, subject, UserID, day_ID):
        times = str([start_time, end_time])        
        value = (day_name, times, subject, str(UserID), str(day_ID))
        query1 = "SELECT * FROM study_plan WHERE UserID = %s AND day_ID = %s AND time = %s"
        self.cursor.execute(query1, (UserID, day_ID, times))
        results = self.cursor.fetchall()

        if results:
            for result in results:
                planID, dayName, time, subjectName, retrieved_UserID, day_ID2 = result

                if (time == times) and (subjectName != subject) and (day_ID == day_ID2) :
                    query = "UPDATE study_plan SET subjectName = %s WHERE UserID = %s AND time = %s AND  day_ID = %s"
                    self.cursor.execute(query, (subject, str(UserID), time, str(day_ID)))
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
    def insert_alert_gui(self, GuildID, alert_Msg, adminID, roleID="0"):
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (str(GuildID),))
        results = self.cursor.fetchone()

        if results :
            query = "UPDATE guild SET Alert_Msg = %s WHERE GuildID = %s"
            self.cursor.execute(query, (str(alert_Msg), str(GuildID)))
            self.conn.commit()
            print("Update Alert")
        else :
            query = "INSERT INTO guild ( GuildID, Alert_Msg, FadminID, RoleID) VALUES (%s, %s, %s, %s);"
            value = ( str(GuildID), str(alert_Msg), str(adminID), str(roleID))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("Insert Alert")
    # check ข้อความ alert
    def check_alert_gui(self, guildID):       
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (str(guildID),))
        results = self.cursor.fetchall()
        
        if results :
            for result in results :
                GuildID, Alert_Msg, FUserID, role = result
            print(f" this : {Alert_Msg}")
            return str(Alert_Msg)

        else:
            return ""

    def insert_feedback_ch(self, FuncName, channel_reply, GuildID, roleID="0"):
        query1 = "SELECT * FROM function_ch WHERE FGuildID = %s AND FuncName = %s"
        self.cursor.execute(query1, (GuildID, str(FuncName)))
        results = self.cursor.fetchone()

        if results:
            query = "UPDATE function_ch SET CH_ReplyFuncID = %s WHERE FGuildID = %s AND FuncName = %s"
            self.cursor.execute(query, (str(channel_reply), str(GuildID), str(FuncName)))
            self.conn.commit()
            print("Update CH")
            if str(FuncName) == "register":
                query2 = "UPDATE guild SET RoleID = %s WHERE GuildID = %s"
                self.cursor.execute(query2, (str(roleID), str(GuildID)))
                self.conn.commit()
                print("Update Role")


        else :
            query = "INSERT INTO function_ch ( FuncName, CH_ReplyFuncID, FGuildID) VALUES (%s, %s, %s);"
            value = ( str(FuncName), str(channel_reply), str(GuildID))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("Insert CH")

    def check_feedback_ch(self, FuncName, GuildID):       
        query1 = "SELECT * FROM function_ch WHERE FGuildID = %s AND FuncName = %s"
        self.cursor.execute(query1, (str(GuildID), FuncName))
        results = self.cursor.fetchone()
        if results:
            funcID,funcName,CH_Reply,FguilID = results
            CH_list = ast.literal_eval(CH_Reply)
            new_CH_Reply = [int(item) for item in CH_list]
            return new_CH_Reply
        
        else:
            return []

    def profile(self, UserID, key, GuildID):
        query = "SELECT * FROM user WHERE UserID = %s"
        self.cursor.execute(query, (str(UserID),))
        result = self.cursor.fetchone()
        FullNameTH, FullNameENG, UserID, Phone, Email = result
        
        query2 = "SELECT * FROM member WHERE UserID = %s and GuildID = %s"
        self.cursor.execute(query2, (str(UserID), str(GuildID)))
        result1 = self.cursor.fetchone()
        userID, guildID, profile, StudentID = result1

        if str(key) == 'TH' :
            return str(FullNameTH)
        elif str(key) == 'ENG' :
            return str(FullNameENG)
        elif str(key) == 'ID' :
            return str(StudentID)
        elif str(key) == 'Phone' :
            return str(Phone)
        elif str(key) == 'Email' :
            return str(Email)
        else :
            return "None" 

    def question_ans(self, Word, resMsg, guildID, type_ans):
        query = "INSERT INTO response_msg ( Word, ResMsg, GuildID, type_ans) VALUES (%s, %s, %s, %s);"
        value = ( str(Word), str(resMsg), str(guildID), str(type_ans))
        self.cursor.execute(query, value)
        self.conn.commit()
        print("Insert QA")

    def check_question_ans(self, GuildID):
        query1 = "SELECT * FROM response_msg WHERE GuildID = %s"
        self.cursor.execute(query1, (str(GuildID), ))
        results = self.cursor.fetchall()
        resIDs = []
        words = []
        answers = []
        types = []
        if results:
            for result in results :
                resID, word, resMsg, fguildID, type_ans = result
                resIDs.append(resID)
                words.append(word)
                answers.append(resMsg)
                types.append(type_ans)

            return words, answers, types, resIDs

        else :
            return [], [], [], []
        
    def delete_question(self,resID):
        query = "DELETE FROM response_msg WHERE resID = %s"
        self.cursor.execute(query, (str(resID), ))
        self.conn.commit()

    def add_guild(self, GuildID, FadminID, Alert_Msg="", roleID="0"):
        print(f"GUILD : {GuildID}")
        print(f"UserID : {FadminID}")
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (str(GuildID), ))
        result = self.cursor.fetchone()

        if result is not None:
            print("NOT ADD GUILD")

        else:
            query = "INSERT INTO guild ( GuildID, Alert_Msg, FadminID, RoleID) VALUES (%s, %s, %s, %s);"
            value = ( str(GuildID), str(Alert_Msg), str(FadminID), str(roleID))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("ADD GUILD")

    def check_guild(self, GuildID):
        print(GuildID)
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (str(GuildID), ))
        result = self.cursor.fetchall()
        print(len(result))
        if len(result) > 0:
            return True
        else:
            return False

    def add_admin(self, adminID, Name):
        query1 = "SELECT * FROM admin WHERE adminID = %s"
        self.cursor.execute(query1, (str(adminID), ))
        result = self.cursor.fetchall()
    
        if result:
            print("NOT ADD ADMIN")

        else:
            query = "INSERT INTO admin ( adminID, name) VALUES (%s, %s);"
            value = ( str(adminID), str(Name))
            self.cursor.execute(query, value)
            self.conn.commit()
            print("ADD ADMIN")

    def check_admin(self, adminID):
        query1 = "SELECT * FROM admin WHERE adminID = %s"
        self.cursor.execute(query1, (str(adminID), ))
        result = self.cursor.fetchall()
        if result:
            return True
        else:
            return False

    def get_role(self, guildID):
        query1 = "SELECT * FROM guild WHERE GuildID = %s"
        self.cursor.execute(query1, (str(guildID), ))
        result = self.cursor.fetchone()

        if result:
            GuildID, Alert_Msg, FUserID, role = result
            print(role)
            return int(role)
        else :
            return 0
