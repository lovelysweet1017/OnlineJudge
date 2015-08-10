require(["jquery", "avalon", "editor", "uploader", "bs_alert", "csrf", "tagEditor", "validation", "jqueryUI"],
    function ($, avalon, editor, uploader, bs_alert, csrfHeader) {
        avalon.vmodels.add_problem = null;
        $("#add-problem-form")
            .formValidation({
                framework: "bootstrap",
                fields: {
                    title: {
                        validators: {
                            notEmpty: {
                                message: "请填写题目名称"
                            },
                            stringLength: {
                                min: 1,
                                max: 30,
                                message: "名称不能超过30个字"
                            }
                        }
                    },
                    cpu: {
                        validators: {
                            notEmpty: {
                                message: "请输入时间限制"
                            },
                            integer: {
                                message: "请输入一个合法的数字"
                            },
                            between: {
                                inclusive: true,
                                min: 1,
                                max: 5000,
                                message: "只能在1-5000之间"
                            }
                        }
                    },
                    memory: {
                        validators: {
                            notEmpty: {
                                message: "请输入内存限制"
                            },
                            integer: {
                                message: "请输入一个合法的数字"
                            }
                        }
                    },
                    difficulty: {
                        validators: {
                            notEmpty: {
                                message: "请输入难度"
                            },
                            integer: {
                                message: "难度用一个整数表示"
                            }
                        }
                    },
                    source: {
                        validators: {
                            notEmpty: {
                                message: "请输入题目来源"
                            }
                        }
                    }
                }
            })
            .on("success.form.fv", function (e) {
                e.preventDefault();
                if (vm.test_case_id == '')
                {
                    bs_alert("你还没有上传测试数据!");
                    return;
                }
                if (vm.description == '')
                {
                    bs_alert("题目描述不能为空!");
                    return;
                }
                if (vm.hint == '')
                {
                    bs_alert("提示不能为空!");
                    return;
                }
                var ajaxData = {
                    title: vm.title,
                    description: vm.description,
                    time_limit: vm.cpu,
                    memory_limit: vm.memory,
                    samples: [],
                    test_case_id: vm.test_case_id,
                    hint: vm.hint,
                    source: vm.source,
                    tags: [],
                    difficulty: vm.difficulty
                };
                if (vm.samples.length == 0)
                {
                    bs_alert("请至少添加一组样例!");
                    return;
                }
                var tags = $("#tags").tagEditor("getTags")[0].tags;
                if (tags.length == 0)
                {
                    bs_alert("请至少添加一个标签，这将有利于用户发现你的题目!");
                    return;
                }
                for (key in vm.samples.length) {
                    ajaxData.samples.push({input: vm.samples[key].input, output: vm.samples[key].output});
                }
                for (key in tags) {
                    ajaxData.tags.push(tags[key].tag);
                }
                console.log(ajaxData);
                $.ajax({
                    beforeSend: csrfHeader,
                    url: "/api/admin/problem/",
                    dataType: "json",
                    data:ajaxData,
                    method: "post",
                    success: function (data) {
                        if (!data.code) {
                            bs_alert("successful!");
                            console.log(data);
                        }
                        else {
                            bs_alert(data.data);
                        }
                    }

                })
            });
        var problemDiscription = editor("#problemDescription");
        var testCaseUploader = uploader("#testCaseFile", "/api/admin/test_case_upload/", function (file, respond) {
            if (respond.code)
                bs_alert(respond.data);
            else {
                vm.test_case_id = respond.data.test_case_id;
                vm.uploadSuccess = true;
                vm.testCaseList = [];
                for (var i = 0; i < respond.data.file_list.input.length; i++) {
                    vm.testCaseList.push({
                        input: respond.data.file_list.input[i],
                        output: respond.data.file_list.output[i]
                    });
                }
            }
        });
        var hinteditor = editor("#hint");
        var tagList = [], completeList = [];
        var vm = avalon.define({
            $id: "add_problem",
            title: "",
            description: "",
            cpu: 1000,
            memory: 256,
            samples: [],
            hint: "",
            visible: false,
            difficulty: 0,
            tags: [],
            tag: "",
            test_case_id: "",
            testCaseList: [],
            uploadSuccess: false,
            source: "",
            add_sample: function () {
                vm.samples.push({input: "", output: "", "visible": true});
            },
            del_sample: function (sample) {
                if (confirm("你确定要删除么?")) {
                    vm.samples.remove(sample);
                }
            },
            toggle_sample: function (sample) {
                sample.visible = !sample.visible;
            },
            getBtnContent: function (item) {
                if (item.visible)
                    return "折叠";
                return "展开";
            }
        });

        $.ajax({
            beforeSend: csrfHeader,
            url: "/api/admin/tag/",
            dataType: "json",
            method: "get",
            success: function (data) {
                if (!data.code) {
                    tagList = data.data;
                    completeList = [];
                    for (key in tagList) {
                        completeList.push(tagList[key].name);
                    }
                    $("#tags").tagEditor({
                        autocomplete: {
                            delay: 0, // show suggestions immediately
                            position: {collision: 'flip'}, // automatic menu position up/down
                            source: completeList
                        }
                    });
                }
                else {
                    bs_alert(data.data);
                }
            }

        });
        avalon.scan();
    });