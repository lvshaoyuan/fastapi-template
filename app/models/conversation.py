"""
@Time : 2023/4/12 15:11 
@Author : oldlv
@File : conversation.py 
@Description:
"""

from tortoise import fields, Model


class Conversation(Model):
    id = fields.BigIntField(pk=True, description='主键')
    item_id = fields.CharField(max_length=512, description='聊天id')
    user_id = fields.BigIntField(null=True, verbose_name='会话id', description='会话主id')
    title = fields.TextField(description='会话标题')
    contents = fields.JSONField(description='会话内容')
    create_datetime = fields.DatetimeField(auto_now_add=True, verbose_name='创建时间', description='创建时间')
    update_datetime = fields.DatetimeField(auto_now=True, verbose_name='更新时间', description='更新时间')
    consume_token = fields.JSONField(description='消耗的token')

    class Meta:
        table = 'conversation'
        table_description = '聊天记录表'
