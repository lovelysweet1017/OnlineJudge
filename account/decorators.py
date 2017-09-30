import functools

from utils.api import JSONResponse

from .models import ProblemPermission

from contest.models import Contest, ContestType, ContestStatus


class BasePermissionDecorator(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type):
        return functools.partial(self.__call__, obj)

    def error(self, data):
        return JSONResponse.response({"error": "permission-denied", "data": data})

    def __call__(self, *args, **kwargs):
        self.request = args[1]

        if self.check_permission():
            if self.request.user.is_disabled:
                return self.error("Your account is disabled")
            return self.func(*args, **kwargs)
        else:
            return self.error("Please login in first")

    def check_permission(self):
        raise NotImplementedError()


class login_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated()


class super_admin_required(BasePermissionDecorator):
    def check_permission(self):
        user = self.request.user
        return user.is_authenticated() and user.is_super_admin()


class admin_role_required(BasePermissionDecorator):
    def check_permission(self):
        user = self.request.user
        return user.is_authenticated() and user.is_admin_role()


class problem_permission_required(admin_role_required):
    def check_permission(self):
        if not super(problem_permission_required, self).check_permission():
            return False
        if self.request.user.problem_permission == ProblemPermission.NONE:
            return False
        return True


def check_contest_permission(func):
    """
    只供Class based view 使用，检查用户是否有权进入该contest，
    若通过验证，在view中可通过self.contest获得该contest
    """
    @functools.wraps(func)
    def _check_permission(*args, **kwargs):
        self = args[0]
        request = args[1]
        user = request.user
        if kwargs.get("contest_id"):
            contest_id = kwargs.pop("contest_id")
        else:
            contest_id = request.GET.get("contest_id")
        if not contest_id:
            return self.error("Parameter contest_id not exist.")

        try:
            # use self.contest to avoid query contest again in view.
            self.contest = Contest.objects.select_related("created_by").get(id=contest_id, visible=True)
        except Contest.DoesNotExist:
            return self.error("Contest %s doesn't exist" % contest_id)

        # creator or owner
        if self.contest.is_contest_admin(user):
            return func(*args, **kwargs)

        if self.contest.status == ContestStatus.CONTEST_NOT_START:
            return self.error("Contest has not started yet.")

        if self.contest.contest_type == ContestType.PASSWORD_PROTECTED_CONTEST:
            # Anonymous
            if not user.is_authenticated():
                return self.error("Please login in first.")
            # password error
            if ("contests" not in request.session) or (self.contest.id not in request.session["contests"]):
                return self.error("Password is required.")

        return func(*args, **kwargs)

    return _check_permission
