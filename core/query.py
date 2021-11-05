from api.models import TestCase, Scenario
from utils.pubulic.DictUtil import DictUtils
from utils.pubulic.logger import Logger

logger = Logger("Query case data")
dict_uitls = DictUtils()


def single_query_testcase_data(selected_case_id, selected_scenario_ids):
    data = []
    dict_ = {}
    _dict = TestCase.objects.filter(id=selected_case_id).values(
        "test_suit__module",
        "test_suit__class_title",
        "case",
        "case_title",
        "case_description",
        "templates__name",
        "templates__url",
        "templates__method",
        "templates__header",
        "templates__data"
    ).first()

    _scenarios = Scenario.objects.filter(id__in=selected_scenario_ids).values()
    scenario = []
    for _scenario in _scenarios:
        _scenario_name = _scenario["scenario"]
        _parameter = dict_uitls._multiDictMerge(_scenario["parameter"])
        _validator = dict_uitls._multiDictMerge(_scenario["validator"])
        scenario.append([_parameter, _scenario_name, _validator])

    dict_.update(
        {
            "module": _dict["test_suit__module"],
            "class_title": _dict["test_suit__class_title"],
            "case": _dict["case"],
            "case_title": _dict["case_title"],
            "case_description": _dict["case_description"],
            "templates_name": _dict["templates__name"],
            "url": _dict["templates__url"],
            "method": _dict["templates__method"],
            "header": _dict["templates__header"],
            "data": _dict["templates__data"],
            "scenarios": scenario
        }
    )

    data.append(dict_)
    return data


def single_query_testsuit_data(selected_case_ids):
    data = []
    for id in selected_case_ids:
        dict_ = {}
        _dict = TestCase.objects.filter(id=id).values(
            "test_suit__module",
            "test_suit__class_title",
            "case",
            "case_title",
            "case_description",
            "templates__name",
            "templates__url",
            "templates__method",
            "templates__header",
            "templates__data"
        ).first()

        _scenarios = Scenario.objects.filter(test_case__id=id).values()
        scenario = []
        for _scenario in _scenarios:
            _scenario_name = _scenario["scenario"]
            _parameter = dict_uitls._multiDictMerge(_scenario["parameter"])
            _validator = dict_uitls._multiDictMerge(_scenario["validator"])
            scenario.append([_parameter, _scenario_name, _validator])

        dict_.update(
            {
                "module": _dict["test_suit__module"],
                "class_title": _dict["test_suit__class_title"],
                "case": _dict["case"],
                "case_title": _dict["case_title"],
                "case_description": _dict["case_description"],
                "templates_name": _dict["templates__name"],
                "url": _dict["templates__url"],
                "method": _dict["templates__method"],
                "header": _dict["templates__header"],
                "data": _dict["templates__data"],
                "scenarios": scenario
            }
        )

        data.append(dict_)
    return data


def single_query_project_data(selected_suit_ids):
    suits = []
    for selected_suit_id in selected_suit_ids:
        case_ids = TestCase.objects.filter(test_suit__id=selected_suit_id).values("id")
        case_ids = [case_id["id"] for case_id in case_ids]
        cases = single_query_testsuit_data(case_ids)
        suits.extend(cases)
    return suits
