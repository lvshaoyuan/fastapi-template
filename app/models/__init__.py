from app.models import user
from app.models import conversation

# 新增model后，在list引入文件，而不是model类
models = [conversation, user]
