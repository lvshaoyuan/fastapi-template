import os

from pathlib import Path

# 获取项目根目录
# 或使用绝对路径，指到目录fastapi-template为止：BasePath =/Users/oldlv/Documents/fastapi项目/fastapi-template
BasePath = Path(__file__).resolve().parent.parent.parent

# 日志文件路径
LogPath = os.path.join(BasePath, 'app', 'log')

# 图片上传存放路径: /static/media/uploads/
ImgPath = os.path.join(BasePath, 'app', 'static', 'media', 'uploads')

# 头像上传存放路径: /static/media/uploads/avatars/
AvatarPath = os.path.join(ImgPath, 'avatars', '')
