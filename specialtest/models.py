from django.db import models

# Create your models here.
"""
    专项计划种类：
        1： 压力测试pl
"""

# 线上接口的数据，每次发布自动获取最新的接口请求内容，用于流量回放，目前是每次都捕获，集成上流水线之后变为发布后第一次捕获。
class ApiData(models.Model):
    id = models.AutoField(primary_key=True)
    target_api = models.URLField('目标http接口')
    api_request_data = models.TextField('请求内容')
    api_response_data = models.TextField('响应内容')


# class perssureTest(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField('名称', max_length=50, unique=True, null=False)
#     target_api = models.URLField('目标http接口')





