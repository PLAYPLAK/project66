



class GroupworkView(discord.ui.View):
    def __init__(self, topic : str, member_amount : int):
        super().__init__()

        self.topic = topic
        self.member_amount = member_amount

    @discord.ui.button(label='Join', style=discord.ButtonStyle.green)
    async def join(self, button : discord.ui.Button, interaction : discord.Interaction):
        await interaction.response.send_message(f'{self.topic} คุณได้เข้าร่วมกลุ่มแล้ว')


#groupwork
    @bot.tree.command(description='find groupwork') #คำอธิบายของคำสั่ง
    @app_commands.describe(topic = 'รายละเอียดหัวข้อของกลุ่มที่จะสร้าง', member_amount = 'จำนวนสมาชิกในกลุ่ม') #คำอธิบายของตัวเลือกย่อย
    async def group(interaction : discord.Interaction, topic : str , member_amount : int):
        group_view = GroupworkView(topic, member_amount)
        await interaction.response.send_message(view=group_view)