({
	// RequireJS 通过一个相对的路径 baseUrl来加载所有代码。baseUrl通常被设置成data-main属性指定脚本的同级目录。
	baseUrl: "js/",
	// 第三方脚本模块的别名,jquery比libs/jquery-1.11.1.min.js简洁明了；
    paths: {
        jquery: "lib/jquery/jquery",
        avalon: "lib/avalon/avalon",
        editor: "utils/editor",
        uploader: "utils/uploader",
        formValidation: "utils/formValidation",
        codeMirror: "utils/codeMirror",
        bsAlert: "utils/bsAlert",
        problem: "app/oj/problem/problem",
        contest: "app/admin/contest/contest",
        csrfToken: "utils/csrfToken",
        admin: "app/admin/admin",
        chart: "lib/chart/Chart",
        tagEditor: "lib/tagEditor/jquery.tag-editor.min",
        jqueryUI: "lib/jqueryUI/jquery-ui",
        bootstrap: "lib/bootstrap/bootstrap",
        datetimePicker: "lib/datetime_picker/bootstrap-datetimepicker.zh-CN",
        validator: "lib/validator/validator",


        // ------ 下面写的都不要直接用，而是使用上面的封装版本 ------
        //富文本编辑器simditor -> editor
        simditor: "lib/simditor/simditor",
        "simple-module": "lib/simditor/module",
        "simple-hotkeys": "lib/simditor/hotkeys",
        "simple-uploader": "lib/simditor/uploader",

        //code mirror 代码编辑器 ->codeMirror
        _codeMirror: "lib/codeMirror/codemirror",
        codeMirrorClang: "lib/codeMirror/language/clike",

        //百度webuploader -> uploader
        webUploader: "lib/webuploader/webuploader",

        "_datetimePicker": "lib/datetime_picker/bootstrap-datetimepicker"

    },
    shim: {
        "bootstrap": {"deps": ['jquery']},
        "_datetimepicker": {"deps": ["jquery"]},
        "datetimepicker": {"deps": ["_datetimepicker"]}
    },
    findNestedDependencies: true,
    appDir: "../",
    dir: "../../release/",
    modules: [
        {
            name: "submit_code"
        },
        {
            name: "validation"
        },
        {
            name: "editor"
        },
        {
            name: "code_mirror"
        },
        {
            name: "datetimepicker"
        }
    ]
})