#-*- coding:utf-8 –*-
#!/usr/bin/env python
import pika

#像往常一样，我们建立连接，声明队列
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

#声明我们的fibonacci函数，它假设只有合法的正整数当作输入。
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

#为 basic_consume 声明了一个回调函数，这是RPC服务器端的核心。它执行实际的操作并且作出响应。
def on_request(ch, method, props, body):
    n = int(body)

    print " [.] fib(%s)"  % (n,)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

#或许我们希望能在服务器上多开几个线程。
#为了能将负载平均地分摊到多个服务器，我们需要将 prefetch_count 设置好
channel.basic_qos(prefetch_count=1)

channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()
