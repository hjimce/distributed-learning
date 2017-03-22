#coding=utf-8
#多台机器，每台机器有一个显卡、或者多个显卡，这种训练叫做分布式训练
import  tensorflow as tf
#现在假设我们有A、B、C、D四台机器，首先需要在各台机器上写一份代码，并跑起来，各机器上的代码内容大部分相同
# ，除了开始定义的时候，需要各自指定该台机器的task之外。以机器A为例子，A机器上的代码如下：
cluster=tf.train.ClusterSpec({
    "worker": [
        "A_IP:2222",#格式 IP地址：端口号，第一台机器A的IP地址 ,在代码中需要用这台机器计算的时候，就要定义：/job:worker/task:0
        "B_IP:1234"#第二台机器的IP地址 /job:worker/task:1
        "C_IP:2222"#第三台机器的IP地址 /job:worker/task:2
    ],
    "ps": [
        "D_IP:2222",#第四台机器的IP地址 对应到代码块：/job:ps/task:0
    ]})

#不同的机器，下面这一行代码各不相同，server可以根据job_name、task_index两个参数，查找到集群cluster中对应的机器
tf.train.Server(cluster,job_name='worker',task_index=0)#找到‘worker’名字下的，task0，也就是机器A


with tf.device('/job:ps/task:0'):#参数定义在机器D上
	w=tf.get_variable('w',(2,2),tf.float32,initializer=tf.constant_initializer(2))
	b=tf.get_variable('b',(2,2),tf.float32,initializer=tf.constant_initializer(5))

with tf.device('/job:worker/task:0/cpu:0'):#在机器A cpu上运行
	addwb=w+b
with tf.device('/job:worker/task:1/cpu:0'):#在机器B cpu上运行
	mutwb=w*b
with tf.device('/job:worker/task:2/cpu:0'):#在机器C cpu上运行
	divwb=w/b

tf.get_default_graph().finalize()
ini=tf.initialize_all_variables()
with tf.Session() as sess:
	sess.run(ini)
	while 1:
		print sess.run([addwb,mutwb,divwb])

#定义了一个集群，该集群包含了两个job
#第一个层次就是job 名字，包含了两个job，名字分别为：worker、ps，当然也可以自己定义其它的job名字
#然后再每个job下面有一系列的task，按照顺序来，task的索引从0开始递增，比如下面的电脑C就是要用于计算，tensorflow图程序代码块中的task2




