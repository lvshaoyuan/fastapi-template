# Fastapi demo

## 技术栈

- fastapi
- tortoise-orm
- aerich
- redis
- mysql
- ....

## 使用说明
1. 安装依赖
    ```shell
    pip install -r requirements.txt
    ```
2. 创建数据库 fastapi, 选择 utf8mb4 编码
3. 新建 app/config.py 配置文件， 填入以下信息
    ```python
   environment_config = 'dev'
   # 那么读取的就是dev.ini文件中的配置信息
   ```
4. app/conf/dev.ini 文件中修改配置信息，包括刚才新建的数据库配置信息
5. 执行数据库迁移
    ```shell
    cd app/aerich
    
    # demo中可省略两步
    # aerich init -t env.TORTOISE_ORM  
    
    aerich init-db

    aerich upgrade
    
    # 当更新数据库 model 后，执行下面两个命令进行迁移
    aerich migrate
    
    aerich upgrade
    ```
6. 启动 redis
7. 修改dev.ini中的redis配置信息
8. 执行 app/main.py 文件启动服务
9. 访问 http://127.0.0.1:3002/v1/docs
10. 初始化测试数据
    ```shell
    cd app
    
    执行 init_data.py 文件 初始化管理员用户
    ```