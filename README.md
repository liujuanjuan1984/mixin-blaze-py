# Mixin Bot 消息监听与存储服务

mixin blaze bot with python; blaze the messages and store to db.

一个依赖 [mixinsdk](https://pypi.org/project/mixinsdk/0.1.4/) 的 blaze bot 服务，用于监听 mixin bot 的消息，并把消息写入数据库， 同时封装了数据查询和新增的接口。

### 如何部署？

拷贝源码：

```bash
git clone https://github.com/liujuanjuan1984/mixin-blaze-py.git
cd mixin-blaze-py
```


安装依赖：

```bash
pipenv install
```

更新配置文件 blaze/config.py

- 申请 mixin bot，并把 session key 信息更新到 MIXIN_KEYSTORE 
- 修改 DB_NAME

启动 blaze 服务

```bash
pipenv run python blaze/do_blaze.py
```

### 如何使用？

监听并存储消息，提供消息状态表，是为了对消息做进一步处理。

比如：

- 对特定文本回复特定消息。
- 把消息发送到 Rum Group。

简单参考 example_db.py ，查询消息、状态，然后更新状态。

### 代码格式化

Install:

```bash
pip install black
pip install isort
```

Format:

```bash
isort .
black -l 120 -t py37 -t py38 -t py39 -t py310 .

```