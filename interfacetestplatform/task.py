from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import os
import traceback
import json
import logging
from . import models
from .utils.data_process import data_preprocess, assert_result, data_postprocess
from .utils.request_process import request_process


# 测试用例执行
@shared_task
def case_task(test_case_id_list, server_address):
    print("开始执行")
    global_key = 'case' + str(int(time.time() * 100000))
    os.environ[global_key] = '{}'
    # print()
    print("得到global_key")
    logging.info("全局变量标识符【global_key】: {}".format(global_key))
    logging.info("全局变量内容【os.environ[global_key]】: {}".format(os.environ[global_key]))
    # 前端传入需要执行的测试用例列表
    for test_case_id in test_case_id_list:
        print("读取上次数据")
        # 从数据库读取测试用例
        test_case = models.TestCase.objects.filter(id=int(test_case_id))[0]
        # 获取上次传入的response
        last_execute_record_data = models.TestCaseExecuteResult.objects.filter(
            belong_test_case_id=test_case_id).order_by('-id')
        if last_execute_record_data:
            last_time_execute_response_data = last_execute_record_data[0].response_data
        else:
            last_time_execute_response_data = ''
        print("上一次响应结果: {}".format(last_execute_record_data))
        print("上一次响应时间: {}".format(last_time_execute_response_data))
        # 创建此次的数据库记录
        execute_record = models.TestCaseExecuteResult.objects.create(belong_test_case=test_case)
        execute_record.last_time_response_data = last_time_execute_response_data
        # 赋值上次记录
        execute_record.save()

        test_case = models.TestCase.objects.filter(id=int(test_case_id))[0]
        print("\n######### 开始执行用例【{}】 #########".format(test_case))
        execute_start_time = time.time()  # 记录时间戳，便于计算总耗时（毫秒）
        execute_record.execute_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(execute_start_time))
        request_data = test_case.request_data
        # extract_var = test_case.extract_var
        # assert_key = test_case.assert_key
        # interface_name = test_case.uri
        # belong_project = test_case.belong_project
        # # belong_module = test_case.belong_module
        # maintainer = test_case.maintainer
        # request_method = test_case.request_method
        # print("初始请求数据: {}".format(request_data))
        # print("关联参数: {}".format(extract_var))
        # print("断言关键字: {}".format(assert_key))
        # print("接口名称: {}".format(interface_name))
        # print("所属项目: {}".format(belong_project))
        # # print("所属模块: {}".format(belong_module))
        # print("用例维护人: {}".format(maintainer))
        # print("请求方法: {}".format(request_method))
        # url = "{}{}".format(server_address, interface_name)
        # print("接口地址: {}".format(url))
        print(type(test_case))
        code, request_data, error_msg = data_preprocess(global_key, str(request_data))
        # 请求数据预处理异常，结束用例执行
        if code != 0:
            print("数据处理异常，error: {}".format(error_msg))
            execute_record.execute_result = "失败"
            execute_record.status = 1
            execute_record.exception_info = error_msg
            execute_end_time = time.time()
            execute_record.execute_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(execute_end_time))
            execute_record.execute_total_time = int(execute_end_time - execute_start_time) * 1000
            execute_record.save()
            return
        # 记录请求预处理结果
        else:
            execute_record.request_data = request_data
        # 调用pytest
        try:

            res_data = request_process(url, request_method, json.loads(request_data))
            print("响应数据: {}".format(json.dumps(res_data.json(), ensure_ascii=False)))  # ensure_ascii：兼容中文
            result_flag, exception_info = assert_result(res_data, assert_key)
            # 结果记录保存
            if result_flag:
                print("用例【%s】执行成功！" % test_case)
                execute_record.execute_result = "成功"
                if extract_var.strip() != "None":
                    var_value = data_postprocess(global_key, json.dumps(res_data.json(), ensure_ascii=False), extract_var)
                    execute_record.extract_var = var_value
            else:
                print("用例【%s】执行失败！" % test_case)
                execute_record.execute_result = "失败"
                execute_record.exception_info = exception_info
            execute_record.response_data = json.dumps(res_data.json(), ensure_ascii=False)
            execute_record.status = 1
            execute_end_time = time.time()
            execute_record.execute_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(execute_end_time))
            print("执行结果结束时间: {}".format(execute_record.execute_end_time))
            execute_record.execute_total_time = int((execute_end_time - execute_start_time) * 1000)
            print("用例执行耗时: {}".format(execute_record.execute_total_time))
            execute_record.save()
        except Exception as e:
            print("接口请求异常，error: {}".format(traceback.format_exc()))
            execute_record.execute_result = "失败"
            execute_record.exception_info = traceback.format_exc()
            execute_record.status = 1
            execute_end_time = time.time()
            execute_record.execute_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(execute_end_time))
            print("执行结果结束时间: {}".format(execute_record.execute_end_time))
            execute_record.execute_total_time = int(execute_end_time - execute_start_time) * 1000
            print("用例执行耗时: {} 毫秒".format(execute_record.execute_total_time))
            execute_record.save()
