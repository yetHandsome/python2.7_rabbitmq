#-*- coding:utf-8 –*-
#!/usr/bin/env python
import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
#建立连接、通道并且为回复（replies）声明独享的回调队列
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue) #订阅这个回调队列，以便接收RPC的响应

# on_response回调函数对每一个响应执行一个非常简单的操作，检查每一个响应消息的correlation_id属性是否与我们期待的一致，如果一致，将响应结果赋给self.response，然后跳出consuming循环
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

#接下来，我们定义我们的主要方法 call 方法。它执行真正的RPC请求。
#在这个方法中，首先我们生成一个唯一的 correlation_id，值并且保存起来，'on_response'回调函数会用它来获取符合要求的响应。
#接下来，我们将带有 reply_to 和 correlation_id 属性的消息发布出去
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events() #将响应返回给用户
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print " [x] Requesting fib(30)"
response = fibonacci_rpc.call(30)
print " [.] Got %r" % (response,)
