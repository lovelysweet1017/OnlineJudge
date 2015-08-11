define("admin", ["jquery", "avalon"], function ($, avalon) {

    avalon.ready(function () {

        function li_active(selector) {
            $(selector).attr("class", "list-group-item active");
        }

        function li_inactive(selector) {
            $(".list-group-item").attr("class", "list-group-item");
        }

        function show_template(url) {
            $("#loading-gif").show();
            vm.template_url = url;
        }

        var hash = window.location.hash.substring(1);

        if (!hash) {
            hash = "index/index";
        }

        var vm = avalon.define({
            $id: "admin",
            template_url: "template/" + hash + ".html",
            group_id: -1,
            hide_loading: function () {
                $("#loading-gif").hide();
            }
        });

        vm.$watch("showGroupDetailPage", function(group_id){
            vm.group_id = group_id;
            vm.template_url = "template/group/group_detail.html";
        });

        avalon.scan();

        li_active("#li-" + hash.replace("/", "-"));

        window.onhashchange = function () {
            var hash = window.location.hash.substring(1);
            if (hash) {
                li_inactive(".list-group-item");
                li_active("#li-" + hash.replace("/", "-"));
                show_template("template/" + hash + ".html");
            }
        };
    });


});