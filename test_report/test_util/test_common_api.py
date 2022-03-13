import pytest
import requests
import allure


class TestCommon:
    # 全局变量env，用于读取当前的测试用例的请求参数
    env = {}
    # request_param是一个字典类型的变量
    # 参数包括method,url,headers,bodys,params,except(dict类型)
    def test_common_request(self):
        assert 1 == 2
        # if(reqeust_param["method"] == "GET"):
        #     timeout = 10
        #     if(reqeust_param.get("timeout")):
        #         timeout = reqeust_param.get("timeout")
        #     re = requests.request(reqeust_param["method"],
        #                           url=reqeust_param["method"],
        #                           headers=reqeust_param["headers"],
        #                           params=reqeust_param["params"],
        #                           )
        #     for flag in reqeust_param.get("except"):
        #         assert flag == re.get(flag)


if __name__ == "__main__":
    pytest.main([])