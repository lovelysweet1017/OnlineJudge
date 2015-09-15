require(["jquery", "codeMirror", "csrfToken", "bsAlert", "ZeroClipboard"],
    function ($, codeMirror, csrfTokenHeader, bsAlert, ZeroClipboard) {
        // 复制样例需要 Flash 的支持 检测浏览器是否安装了 Flash
        function detect_flash() {
            var ie_flash;
            try {
                ie_flash = (window.ActiveXObject && (new ActiveXObject("ShockwaveFlash.ShockwaveFlash")) !== false)
            } catch (err) {
                ie_flash = false;
            }
            var _flash_installed = ((typeof navigator.plugins != "undefined" && typeof navigator.plugins["Shockwave Flash"] == "object") || ie_flash);
            return _flash_installed;
        }

        if(detect_flash()) {
            // 提供点击复制到剪切板的功能
            ZeroClipboard.config({swfPath: "/static/img/ZeroClipboard.swf"});
            new ZeroClipboard($(".copy-sample"));
        }
        else{
            $(".copy-sample").hide();
        }

        var codeEditorSelector = $("#code-editor")[0];
        // 部分界面逻辑会隐藏代码输入框，先判断有没有。
        if (codeEditorSelector == undefined) {
            return;
        }

        var codeEditor = codeMirror(codeEditorSelector, "text/x-csrc");
        var language = $("input[name='language'][checked]").val();
        var submissionId;

        $("input[name='language']").change(function () {
            language = this.value;
            var languageTypes = {"1": "text/x-csrc", "2": "text/x-c++src", "3": "text/x-java"};
            codeEditor.setOption("mode", languageTypes[language]);
        });

        $("#show-more-btn").click(function () {
            $(".hide").attr("class", "problem-section");
            $("#show-more-btn").hide();
        });

        function showLoading() {
            $("#submit-code-button").attr("disabled", "disabled");
            $("#loading-gif").show();
        }

        function hideLoading() {
            $("#submit-code-button").removeAttr("disabled");
            $("#loading-gif").hide();
        }

        function getResultHtml(data) {
            // 0 结果正确 1 运行错误 2 超时 3 超内存 4 编译错误
            // 5 格式错误 6 结果错误 7 系统错误 8 等待判题
            var results = {
                0: {"alert_class": "success", message: "Accepted"},
                1: {"alert_class": "danger", message: "Runtime Error"},
                2: {"alert_class": "warning", message: "Time Limit Exceeded"},
                3: {"alert_class": "warning", message: "Memory Limit Exceeded"},
                4: {"alert_class": "danger", message: "Compile Error"},
                5: {"alert_class": "warning", message: "Format Error"},
                6: {"alert_class": "danger", message: "Wrong Answer"},
                7: {"alert_class": "danger", message: "System Error"},
                8: {"alert_class": "info", message: "Waiting"}
            };

            var html = '<div class="alert alert-' +
                results[data.result].alert_class + ' result"' +
                ' role="alert">' +
                '<div class="alert-link">' +
                results[data.result].message +
                '!&nbsp;&nbsp; ';
            if (!data.result) {
                html += "CPU time: " + data.accepted_answer_time + "ms &nbsp;&nbsp;";
            }
            html += ('<a href="/submission/' + submissionId + '/" target="_blank">查看详情</a></div> </div>');

            return html;
        }

        var counter = 0;

        function getResult() {
            if (counter++ > 10) {
                hideLoading();
                bsAlert("抱歉，服务器可能出现了故障，请稍后到我的提交列表中查看");
                counter = 0;
                return;
            }
            $.ajax({
                url: "/api/submission/?submission_id=" + submissionId,
                method: "get",
                dataType: "json",
                success: function (data) {
                    if (!data.code) {
                        // 8是还没有完成判题
                        if (data.data.result == 8) {
                            // 1秒之后重新去获取
                            setTimeout(getResult, 1000);
                        }
                        else {
                            counter = 0;
                            hideLoading();
                            $("#result").html(getResultHtml(data.data));
                        }
                    }
                    else {
                        bsAlert(data.data);
                        hideLoading();
                    }
                }
            })
        }

        function guessLanguage(code) {
            //cpp
            if (code.indexOf("using namespace std") > -1) {
                return "2";
            }

            //java
            if (code.indexOf("public class Main")) {
                return "3";
            }
        }

        $("#submit-code-button").click(function () {

            var code = codeEditor.getValue();

            if (!code.trim()) {
                bsAlert("请填写代码！");
                hideLoading();
                return false;
            }

            if (guessLanguage(code) != language) {
                if (!confirm("您选择的代码语言可能存在错误，是否继续提交？")) {
                    return;
                }
            }

            if (language < 3) {
                if (code.indexOf("__int64") > -1) {
                    if (!confirm("您是否在尝试使用'__int64'类型? 这不是 c/c++ 标准并将引发编译错误可以使用 'long long' 代替(详见关于->帮助)，是否仍然提交？")) {
                        return;
                    }
                }
                if (code.indexOf("__int64") > -1) {
                    if (!confirm("您是否在尝试用'%I64d'做long long类型的I/O? 这不是 c/c++ 标准并将引发编译错误可以使用 '%lld' 代替(详见关于->帮助)，是否仍然提交？")) {
                        return;
                    }
                }
            }

            if (location.href.indexOf("contest") > -1) {
                var problemId = location.pathname.split("/")[4];
                var contestId = location.pathname.split("/")[2];
                var url = "/api/contest/submission/";
                var data = {
                    problem_id: problemId,
                    language: language,
                    code: code,
                    contest_id: contestId
                };
            }
            else {
                var problemId = window.location.pathname.split("/")[2];
                var url = "/api/submission/";
                var data = {
                    problem_id: problemId,
                    language: language,
                    code: code
                };
            }

            showLoading();

            $("#result").html("");

            $.ajax({
                beforeSend: csrfTokenHeader,
                url: url,
                method: "post",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function (data) {
                    if (!data.code) {
                        submissionId = data.data.submission_id;
                        // 获取到id 之后2秒去查询一下判题结果
                        setTimeout(getResult, 2000);
                    }
                    else {
                        bsAlert(data.data);
                        hideLoading();
                    }
                }
            });

        });

        $.ajax({
            url: "/api/user/",
            method: "get",
            dataType: "json",
            success: function (data) {
                if (data.code) {
                    $("#submit-code-button").attr("disabled", "disabled");
                    $("#result").html('<div class="alert alert-danger" role="alert"><div class="alert-link">请先<a href="/login/" target="_blank">登录</a>!</div> </div>');
                }
            }
        })
    });