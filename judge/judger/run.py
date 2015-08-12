# coding=utf-8
import sys
import pymongo

from bson.objectid import ObjectId

from client import JudgeClient
from language import languages
from compiler import compile_
from result import result
from settings import judger_workspace

from oj import settings

# 简单的解析命令行参数
# 参数有 -solution_id -time_limit -memory_limit -test_case_id
# 获取到的值是['xxx.py', '-solution_id', '1111', '-time_limit', '1000', '-memory_limit', '100', '-test_case_id', 'aaaa']
args = sys.argv
solution_id = args[2]
time_limit = args[4]
memory_limit = args[6]
test_case_id = args[8]


mongodb_setting = settings.DATABASES["mongodb"]
connection = pymongo.MongoClient(host=mongodb_setting["HOST"], port=mongodb_setting["PORT"])
collection = connection["oj"]["oj_submission"]

submission = collection.find_one({"_id": ObjectId(solution_id)})
if not submission:
    exit()


# 将代码写入文件
language = languages[submission["language"]]
src_path = judger_workspace + "run/" + language["src_name"]
f = open(src_path, "w")
f.write(submission["code"])
f.close()

# 编译
try:
    exe_path = compile_(language, src_path, judger_workspace + "run/")
except Exception as e:
    print e
    print [{"result": result["compile_error"]}]
    exit()

client = JudgeClient(language_code=language,
                     exe_path=exe_path,
                     max_cpu_time=int(time_limit),
                     max_real_time=int(time_limit) * 2,
                     max_memory=int(memory_limit),
                     test_case_dir="/var/judger/test_case/" + str(test_case_id) + "/")
print client.run()


