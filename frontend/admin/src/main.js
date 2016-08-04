import Vue from 'vue'
import App from './App'
import VueRouter from "vue-router"
import VueI18n from "vue-i18n"

import "expose?$!expose?jQuery!jquery"
import "bootstrap"
import bootbox from "bootbox"

import locale from "./locales"

import userList from "./components/account/userList.vue"
import editUser from "./components/account/editUser.vue"
import problem from "./components/problem/problem.vue"
import announcementList from "./components/announcement/announcementList.vue"
import editAnnouncement from "./components/announcement/editAnnouncement.vue"


// i18n settings
Vue.use(VueI18n);

// todo: strore lang config in localstorage
var lang = "zh-cn";
Vue.config.lang = lang;

Object.keys(locale).forEach(function (lang) {
    Vue.locale(lang, locale[lang])
});

/////////

// custom ajax
Vue.use({
    install: function (Vue, options) {
        function getCookie(name) {
            var value = "; " + document.cookie;
            var parts = value.split("; " + name + "=");
            if (parts.length == 2) {
                return parts.pop().split(";").shift();
            }
        }

        Vue.prototype.request = function (option) {
            var request = new XMLHttpRequest();
            request.open(option.method, option.url, true);
            request.onerror = function () {
                if (option.error) {
                    option.error(request)
                }
                else {
                    alert(locale[lang].request.error);
                }
            };
            request.onload = function () {
                if (request.status >= 200 && request.status < 400) {
                    try {
                        var data = JSON.parse(request.responseText);
                        if (data.code == 1 && data.data) {
                            alert(data.data);
                            return;
                        }
                    }
                    catch (err) {
                        request.onerror();
                    }
                    if(option.success) {
                        option.success(data);
                    }
                    else {
                        alert(locale[lang].request.succeeded);
                    }
                }
                else {
                    request.onerror();
                }
            };
            request.setRequestHeader('x-requested-with', 'XMLHttpRequest');
            if (option.method.toLowerCase() == 'post' || option.method.toLowerCase() == 'put') {
                request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
                request.setRequestHeader('x-csrftoken', getCookie('csrftoken'));
                request.send(JSON.stringify(option.data));
            }
            else {
                request.send();
            }
        }
    }
});
///////


Vue.use(VueRouter);
var router = new VueRouter({linkActiveClass: "active"});

router.map({
    "/user/:page": {
        name: "userList",
        component: userList
    },
    "/user/edit/:userId": {
        name: "editUser",
        component: editUser
    },
    "/problem/create": {
        name: "createProblem",
        component: problem
    },
    "/announcement/:page": {
        name: "announcementList",
        component: announcementList
    },
    "/announcement/edit/:announcementId": {
        name: "editAnnouncement",
        component: editAnnouncement
    },
    "/problem": {
        component: problem
    }
});

// hide loading
document.getElementById("loading").style.display = "none";

// override window.alert
window.alert = function bootboxAlert(content) {
    bootbox.dialog({
        message: content,
        title: locale[lang].alert.alert,
        buttons: {
            main: {
                label: locale[lang].alert.OK,
                className: "btn-primary"
            }
        }
    })
};

// override window.confirm
window.confirm = function bootboxConfirm(content, okCallback, cancelCallback) {
    bootbox.dialog ({
        message: content,
        title: locale[lang].alert.confirm,
        buttons: {
            cancel: {
                label: locale[lang].alert.cancel,
                className: "btn-success",
                callback: function() {
                    if(cancelCallback) {
                        return cancelCallback;
                    }
                    else {
                        return function(){};
                    }
                }
            },
            main: {
                label: locale[lang].alert.OK,
                className: "btn-danger",
                callback: okCallback
            }
        }
    })
};

router.redirect({"/user": "/user/1"});
router.redirect({"/announcement": "/announcement/1"});

router.start(App, '#app');

