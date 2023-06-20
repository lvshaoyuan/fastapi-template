from tortoise import fields, Model


class Users(Model):
    id = fields.BigIntField(pk=True, index=True, description='主键id')
    username = fields.CharField(max_length=64, unique=True, description='用户名', index=True)
    password = fields.CharField(max_length=255, null=True, description='密码')
    email = fields.CharField(max_length=255, null=True, description='邮箱')
    mobile = fields.CharField(max_length=11, null=True, description='手机号')
    avatar = fields.CharField(max_length=255, null=True, description='头像')
    name = fields.CharField(max_length=64, null=True, description='姓名')
    status = fields.IntField(default=1, description='状态: 1-正常, 0-禁用')
    gender = fields.IntField(default=1, description='性别: 1-男, 0-女')
    user_type = fields.IntField(default=1, description='用户类型: 1-前台用户, 0-后台用户')
    is_superuser = fields.BooleanField(default=False, description='是否超级管理员')
    is_active = fields.BooleanField(default=True, description='是否激活')
    last_login = fields.DatetimeField(null=True, description='上次登录时间')
    create_datetime = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_datetime = fields.DatetimeField(auto_now=True, description='更新时间')

    class Meta:
        table = 'users'
        table_description = '用户表'
        ordering = ['-id']

    def __str__(self):
        return self.username


