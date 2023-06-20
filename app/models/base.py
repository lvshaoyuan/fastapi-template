from tortoise import Model, fields


class CoreModel(Model):
    """
    核心标准抽象模型模型,可直接继承使用
    增加审计字段, 覆盖字段时, 字段名称请勿修改, 必须统一审计字段名称
    """
    id = fields.BigIntField(pk=True, index=True, description='主键id')
    creator = fields.BigIntField(null=True, verbose_name='创建者', description='创建者')
    modifier = fields.BigIntField(null=True, verbose_name='修改者', description='修改者')
    create_datetime = fields.DatetimeField(auto_now_add=True, verbose_name='创建时间', description='创建时间')
    update_datetime = fields.DatetimeField(auto_now=True, verbose_name='更新时间', description='更新时间')
    belong_dept = fields.BigIntField(null=True, verbose_name='数据归属部门', description='数据归属部门')
    sort = fields.IntField(default=1, null=True, verbose_name='显示排序', description='显示排序')

    class Meta:
        table = ''
        abstract = True
