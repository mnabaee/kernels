#!/usr/bin/python3

import sys
task_num = int(sys.argv[1])
import tensorflow as tf

cluster = tf.train.ClusterSpec({"tfworker":["localhost:2222", "localhost:2223", "localhost:2224", "localhost:2225"]})
server = tf.train.Server( cluster, job_name = "tfworker", task_index = task_num )

print("Starting server " + str(task_num))
server.start()
server.join()
