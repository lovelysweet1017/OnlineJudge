from django.utils.timezone import now
from django.core.cache import cache
from utils.api import APIView, validate_serializer
from utils.constants import CacheKey
from account.decorators import login_required, check_contest_permission

from utils.constants import ContestRuleType, ContestStatus
from ..models import ContestAnnouncement, Contest, OIContestRank, ACMContestRank
from ..serializers import ContestAnnouncementSerializer
from ..serializers import ContestSerializer, ContestPasswordVerifySerializer
from ..serializers import OIContestRankSerializer, ACMContestRankSerializer


class ContestAnnouncementListAPI(APIView):
    def get(self, request):
        contest_id = request.GET.get("contest_id")
        if not contest_id:
            return self.error("Invalid parameter")
        data = ContestAnnouncement.objects.select_related("created_by").filter(contest_id=contest_id)
        max_id = request.GET.get("max_id")
        if max_id:
            data = data.filter(id__gt=max_id)
        return self.success(ContestAnnouncementSerializer(data, many=True).data)


class ContestAPI(APIView):
    def get(self, request):
        contest_id = request.GET.get("id")
        if contest_id:
            try:
                contest = Contest.objects.select_related("created_by").get(id=contest_id, visible=True)
            except Contest.DoesNotExist:
                return self.error("Contest does not exist")
            return self.success(ContestSerializer(contest).data)

        contests = Contest.objects.select_related("created_by").filter(visible=True)
        keyword = request.GET.get("keyword")
        rule_type = request.GET.get("rule_type")
        status = request.GET.get("status")
        if keyword:
            contests = contests.filter(title__contains=keyword)
        if rule_type:
            contests = contests.filter(rule_type=rule_type)
        if status:
            cur = now()
            if status == ContestStatus.CONTEST_NOT_START:
                contests = contests.filter(start_time__gt=cur)
            elif status == ContestStatus.CONTEST_ENDED:
                contests = contests.filter(end_time__lt=cur)
            else:
                contests = contests.filter(start_time__lte=cur, end_time__gte=cur)
        return self.success(self.paginate_data(request, contests, ContestSerializer))


class ContestPasswordVerifyAPI(APIView):
    @validate_serializer(ContestPasswordVerifySerializer)
    @login_required
    def post(self, request):
        data = request.data
        try:
            contest = Contest.objects.get(id=data["contest_id"], visible=True, password__isnull=False)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        if contest.password != data["password"]:
            return self.error("Wrong password")

        # password verify OK.
        if "accessible_contests" not in request.session:
            request.session["accessible_contests"] = []
        request.session["contests"].append(contest.id)
        # https://docs.djangoproject.com/en/dev/topics/http/sessions/#when-sessions-are-saved
        request.session.modified = True
        return self.success(True)


class ContestAccessAPI(APIView):
    @login_required
    def get(self, request):
        contest_id = request.GET.get("contest_id")
        if not contest_id:
            return self.error()
        return self.success({"access": int(contest_id) in request.session.get("accessible_contests", [])})


class ContestRankAPI(APIView):
    def get_rank(self):
        if self.contest.rule_type == ContestRuleType.ACM:
            return ACMContestRank.objects.filter(contest=self.contest). \
                select_related("user").order_by("-accepted_number", "total_time")
        else:
            return OIContestRank.objects.filter(contest=self.contest). \
                select_related("user").order_by("-total_score")

    @check_contest_permission
    def get(self, request):
        if self.contest.rule_type == ContestRuleType.ACM:
            serializer = ACMContestRankSerializer
        else:
            serializer = OIContestRankSerializer

        cache_key = f"{CacheKey.contest_rank_cache}:{self.contest.id}"
        qs = cache.get(cache_key)
        if not qs:
            qs = self.get_rank()
            cache.set(cache_key, qs)

        return self.success(self.paginate_data(request, qs, serializer))
