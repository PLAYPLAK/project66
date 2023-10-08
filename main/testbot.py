from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a chatbot instance
chatbot = ChatBot('ThaiDataBot')

# Create a new trainer for the chatbot
trainer = ListTrainer(chatbot)

# Define your custom dataset as conversation pairs in Thai
custom_data_thai = [
    'สวัสดี', 'สวัสดีครับ',
    'ทำอะไร', 'กำลังเรียนรู้เพิ่มเติม',
    'ยินดีที่ได้พบคุณ', 'ยินดีด้วยครับ',
    'สุขสันต์วันเกิด', 'ขอบคุณมากครับ',
    'อากาศวันนี้เป็นอย่างไร', 'อากาศดีมากครับ',
    'คุณชอบกินอาหารชาบูหรือยำแซลมอน?', 'ชอบกินยำแซลมอนครับ',
    'มีแหวกมีกัด', 'เราไม่ควรแหวกมีกัด',
    'คุณอายุเท่าไหร่', 'ผมยังเป็นโมเดลภาษาที่เรียนรู้เท่านั้น',
    'คุณชอบดูภาพยนตร์หรืออ่านหนังสือมากกว่ากัน', 'ฉันไม่มีความสามารถในการดูหนังหรืออ่านหนังสือ',
    'มีแนวทางในการเริ่มต้นการเรียนภาษาไทยหรือไม่', 'ควรเริ่มต้นด้วยการฝึกพูดและฟัง',
]
#พูดคุยลงทะเบียน
dataset_01 = []
#เกี่ยวกับสอบถามข้อมูล
dataset_02 = []
#เกี่ยวกับขอช่องทางการติดต่อ
dataset_03 = []
#เกี่ยวกับรายวิชา
dataset_04 = []


# Train the chatbot on the custom dataset
trainer.train(custom_data_thai)

# Start a conversation with the chatbot
print("Bot: สวัสดีครับ! ผมคือ ThaiDataBot คุณสามารถสนทนากับผมได้")


def chattotalk(text):
    user_input = text
    
    # Exit the loop if the user says "exit"
    if user_input.lower() == 'exit':
        print("Bot: ลาก่อยครับ!")

    # Get the chatbot's response
    response = chatbot.get_response(user_input)
    #print("Bot:", response)

    return response
