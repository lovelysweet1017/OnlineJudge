import hashlib
import json
import os
import zipfile

from django.conf import settings

from account.decorators import admin_required
from utils.api import APIView, CSRFExemptAPIView, validate_serializer
from utils.shortcuts import rand_str

from ..models import Problem, ProblemRuleType, ProblemTag
from ..serializers import (CreateProblemSerializer, ProblemSerializer,
                           TestCaseUploadForm, EditProblemSerializer)


class TestCaseUploadAPI(CSRFExemptAPIView):
    request_parsers = ()

    def filter_name_list(self, name_list, spj):
        ret = []
        prefix = 1
        if spj:
            while True:
                in_name = str(prefix) + ".in"
                if in_name in name_list:
                    ret.append(in_name)
                    prefix += 1
                    continue
                else:
                    return sorted(ret)
        else:
            while True:
                in_name = str(prefix) + ".in"
                out_name = str(prefix) + ".out"
                if in_name in name_list and out_name in name_list:
                    ret.append(in_name)
                    ret.append(out_name)
                    prefix += 1
                    continue
                else:
                    return sorted(ret)

    @admin_required
    def post(self, request):
        form = TestCaseUploadForm(request.POST, request.FILES)
        if form.is_valid():
            spj = form.cleaned_data["spj"] == "true"
            file = form.cleaned_data["file"]
        else:
            return self.error("Upload failed")
        tmp_file = os.path.join("/tmp", rand_str() + ".zip")
        with open(tmp_file, "wb") as f:
            for chunk in file:
                f.write(chunk)
        try:
            zip_file = zipfile.ZipFile(tmp_file)
        except zipfile.BadZipFile:
            return self.error("Bad zip file")
        name_list = zip_file.namelist()
        test_case_list = self.filter_name_list(name_list, spj=spj)
        if not test_case_list:
            return self.error("Empty file")

        test_case_id = rand_str()
        test_case_dir = os.path.join(settings.TEST_CASE_DIR, test_case_id)
        os.mkdir(test_case_dir)

        size_cache = {}
        md5_cache = {}

        for item in test_case_list:
            with open(os.path.join(test_case_dir, item), "wb") as f:
                content = zip_file.read(item).replace(b"\r\n", b"\n")
                size_cache[item] = len(content)
                if item.endswith(".out"):
                    md5_cache[item] = hashlib.md5(content).hexdigest()
                f.write(content)
        test_case_info = {"spj": spj, "test_cases": {}}

        hint = None
        diff = set(name_list).difference(set(test_case_list))
        if diff:
            hint = ", ".join(diff) + " are ignored"

        ret = []

        if spj:
            for index, item in enumerate(test_case_list):
                data = {"input_name": item, "input_size": size_cache[item]}
                ret.append(data)
                test_case_info["test_cases"][str(index + 1)] = data
        else:
            # ["1.in", "1.out", "2.in", "2.out"] => [("1.in", "1.out"), ("2.in", "2.out")]
            test_case_list = zip(*[test_case_list[i::2] for i in range(2)])
            for index, item in enumerate(test_case_list):
                data = {"stripped_output_md5": md5_cache[item[1]],
                        "input_size": size_cache[item[0]],
                        "output_size": size_cache[item[1]],
                        "input_name": item[0],
                        "output_name": item[1]}
                ret.append(data)
                test_case_info["test_cases"][str(index + 1)] = data

        with open(os.path.join(test_case_dir, "info"), "w", encoding="utf-8") as f:
            f.write(json.dumps(test_case_info, indent=4))
        return self.success({"id": test_case_id, "info": ret, "hint": hint, "spj": spj})


class ProblemAPI(APIView):
    @validate_serializer(CreateProblemSerializer)
    def post(self, request):
        data = request.data
        if data["spj"]:
            if not data["spj_language"] or not data["spj_code"]:
                return self.error("Invalid spj")
            data["spj_version"] = hashlib.md5((data["spj_language"] + ":" + data["spj_code"]).encode("utf-8")).hexdigest()
        else:
            data["spj_language"] = None
            data["spj_code"] = None
        if data["rule_type"] == ProblemRuleType.OI:
            for item in data["test_case_score"]:
                if item["score"] <= 0:
                    return self.error("Invalid score")
        # todo check filename and score info
        data["created_by"] = request.user
        tags = data.pop("tags")

        problem = Problem.objects.create(**data)
        for item in tags:
            try:
                tag = ProblemTag.objects.get(name=item)
            except ProblemTag.DoesNotExist:
                tag = ProblemTag.objects.create(name=item)
            problem.tags.add(tag)
        return self.success()

    def get(self, request):
        problem_id = request.GET.get("id")
        if problem_id:
            try:
                problem = Problem.objects.get(id=problem_id)
                if request.user.is_admin_role():
                    problem = problem.get(created_by=request.user)
                return self.success(ProblemSerializer(problem).data)
            except Problem.DoesNotExist:
                return self.error("Problem does not exist")

        problems = Problem.objects.all().order_by("-create_time")
        if request.user.is_admin_role():
            problems = problems.filter(created_by=request.user)
        return self.success(self.paginate_data(request, problems, ProblemSerializer))

    @validate_serializer(EditProblemSerializer)
    def put(self, request):
        data = request.data
        try:
            problem = Problem.objects.get(id=data.pop("id"))
            if request.user.is_admin_role():
                problem = problem.get(created_by=request.user)
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")
        if data["spj"]:
            if not data["spj_language"] or not data["spj_code"]:
                return self.error("Invalid spj")
            data["spj_version"] = hashlib.md5((data["spj_language"] + ":" + data["spj_code"]).encode("utf-8")).hexdigest()
        else:
            data["spj_language"] = None
            data["spj_code"] = None
        if data["rule_type"] == ProblemRuleType.OI:
            for item in data["test_case_score"]:
                if item["score"] <= 0:
                    return self.error("Invalid score")
        # todo check filename and score info
        tags = data.pop("tags")

        for k, v in data.items():
            setattr(problem, k, v)
        problem.save()

        problem.tags.remove(*problem.tags.all())
        for tag in tags:
            try:
                tag = ProblemTag.objects.get(name=tag)
            except ProblemTag.DoesNotExist:
                tag = ProblemTag.objects.create(name=tag)
            problem.tags.add(tag)

        return self.success()
