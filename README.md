# python2.7_rabbitmq
```
####环境
vagrant init ubuntu/trusty64

sudo apt-get install python-pip git-core  # 安装所需要的依赖，未能成功安装，请 update 后进行安装。
sudo pip install pika==0.9.5

下面每个实验多用下面指令查看绑定情况
sudo rabbitmqctl list_bindings

####实验1
#注意要先启动服务：
sudo service rabbitmq-server start

#然后，用 send.py 发送一条消息：
python send.py

#生产者（producer）程序 send.py 每次运行之后就会停止。现在我们就来接收消息：
python receive.py

####实验2

sudo service rabbitmq-server start # 确保服务已打开
shell1$ python worker.py # 第一个终端
shell2$ python worker.py # 第二个终端

第三个终端，我们用来发布新任务。你可以发送一些消息给消费者（consumers）

shell3$ python new_task.py First message.
shell4$ python new_task.py Second message..
shell5$ python new_task.py Third message...
shell6$ python new_task.py Fourth message....
shell7$ python new_task.py Fifth message.....

####实验3 -- 发布于订阅
rabbitmqctl 能够列出服务器上所有的交换机：

sudo service rabbitmq-server start
sudo rabbitmqctl list_exchanges

python receive_logs.py > logs_from_rabbit.log #把日志保存到 log 文件里
python receive_logs.py    #在屏幕上查看日志
python emit_log.py    # 发送日志

####实验4 -- 路由


如果你希望只是保存warning和error级别的日志到文件，只需要打开控制台进入代码的目录并输入：

sudo service rabbitmq-server start  #先确保服务已经开启
sudo python receive_logs_direct.py warning error > logs_from_rabbit.log
如果你希望所有的日志信息都输出到屏幕中，打开一个新的终端，然后输入：

python receive_logs_direct.py info warning error
如果要触发 error ,warning 级别的日志，只需要输入：

python emit_log_direct.py error "Run. Run. Or it will explode 1."
python emit_log_direct.py warning "Run. Run. Or it will explode 2."
然后我们再触发其他类型的日志：

python emit_log_direct.py pub  "Run. Run. Or it will explode 3."
python emit_log_direct.py info "Run. Run. Or it will explode 4."
python emit_log_direct.py msg  "Run. Run. Or it will explode 5."
这样，我们就只在文件里放入了 error 和 warning 类型的日志。


####实验5 -- 主题交换机
>发送到主题交换机（topic exchange）的消息不可以携带随意什么样子的路由键（routing_key），它的路由键 必须是一个由.分隔开的词语列表。这些单词随便是什么都可以，但是最好是跟携带它们的消息有关系的词汇。以下是 几个推荐的例子："stock.usd.nyse", "nyse.vmw", "quick.orange.rabbit"。词语的个数可以随意， 但是不要超过255字节。

* 用来表示一个单词
# 用来表示任意数量（零个或多个）单词


执行命令之前，先确保服务已经开启
sudo service rabbitmq-server start  
执行下边命令 接收所有日志：
python receive_logs_topic.py "#"


执行下边命令 接收来自”kern“设备的日志：
python receive_logs_topic.py "kern.*"


执行下边命令 只接收严重程度为”critical“的日志：
python receive_logs_topic.py "*.critical"


执行下边命令 建立多个绑定：
python receive_logs_topic.py "kern.*" "*.critical"


执行下边命令 发送路由键为 "kern.critical" 的日志：
python emit_log_topic.py "kern.critical" "A critical kernel error"


####实验6 -- 远程过程调用

我们的 RPC 服务已经准备就绪了，现在启动服务器端：

sudo service rabbitmq-server start  #先确保服务已经开启
python rpc_server.py                # 打开第一个终端输入
python rpc_server.py                # 打开第二个终端输入




运行客户端，请求一个fibonacci队列。

python rpc_client.py        # 多运行几次客户端，看看 rabbitmq 是否会自动选择闲置的服务端，提高效率
python rpc_client.py
python rpc_client.py


此处呈现的设计并不是实现RPC服务的唯一方式，但是他有一些重要的优势：

1 如果RPC服务器运行的过慢的时候，你可以通过运行另外一个服务器端轻松扩展它。试试在控制台中运行第二个 `rpc_server.py`  。
2 在客户端， RPC 请求只发送或接收一条消息。不需要像 queue_declare 这样的异步调用。所以 RPC 客户端的单个请求只需要一个网络往返。
我们的代码依旧非常简单，而且没有试图去解决一些复杂（但是重要）的问题，如：

当没有服务器运行时，客户端如何作出反映。
客户端是否需要实现类似 RPC 超时的东西。
如果服务器发生故障，并且抛出异常，应该被转发到客户端吗？
在处理前，防止混入无效的信息（例如检查边界）
```
