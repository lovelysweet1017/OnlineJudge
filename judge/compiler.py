# coding=utf-8
import time
import os
import judger
import commands
from judge_exceptions import CompileError, JudgeClientError
from logger import logger
from settings import judger_workspace


def compile_(language_item, src_path, exe_path):
    compile_command = language_item["compile_command"].format(src_path=src_path, exe_path=exe_path).split(" ")
    compiler = compile_command[0]
    compile_args = compile_command[1:]
    compiler_output_file = os.path.join(judger_workspace, str(time.time()) + ".out")

    compile_result = judger.run(exe_path=compiler,
                                in_file="/dev/null",
                                out_file=compiler_output_file,
                                max_cpu_time=2000,
                                max_memory=200000000,
                                args=compile_args,
                                env=["PATH=" + os.environ["PATH"]],
                                use_sandbox=False)

    compile_output_handler = open(compiler_output_file)
    compile_output = compile_output_handler.read()
    compile_output_handler.close()
    os.remove(compiler_output_file)

    if compile_result["flag"] != 0:
        logger.error("Compiler error")
        logger.error(compile_output)
        logger.error(str(compile_result))
        raise CompileError("Compile error")
    else:
        if "error" in compile_output:
            raise CompileError(compile_output)
        return exe_path
