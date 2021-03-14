import os

exec_content = 'python.exe '
object_content = 'split.py'
f = os.popen(exec_content + object_content, 'r')
f.read()
print("Split completed")
object_content = 'aggregate.py'
f = os.popen(exec_content + object_content, 'r')
f.read()
print("Aggregation completed")
object_content = 'stop_removal.py'
f = os.popen(exec_content + object_content, 'r')
f.read()
print("Stop removal completed")
object_content = 'word_count.py'
f = os.popen(exec_content + object_content, 'r')
f.read()
print("Word counting completed")
object_content = 'NB.py'
f = os.popen(exec_content + object_content, 'r')
r = f.read()
print(r)
