# coding=utf-8


languages = {
    1: {
        "name": "c",
        "src_name": "main.c",
        "code": 1,
        "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -std=c99 {src_path} -lm -o {exe_path}/main",
        "execute_command": "{exe_path}/main"
    },
    2: {
        "name": "cpp",
        "src_name": "main.cpp",
        "code": 2,
        "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -std=c++11 {src_path} -lm -o {exe_path}/main",
        "execute_command": "{exe_path}/main"
    },
    3: {
        "name": "java",
        "src_name": "Main.java",
        "code": 3,
        "compile_command": "/usr/bin/javac {src_path} -d {exe_path}",
        "execute_command": "/usr/bin/java -cp {exe_path} -Djava.security.manager -Djava.security.policy==policy Main"
    }
}


