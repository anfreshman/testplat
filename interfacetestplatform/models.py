from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import GroupedForeignKey  # 后台级联选择
# Create your models here.

# 项目模块，需要有项目相关人，角色，项目描述，项目创建时间，项目更新时间，测试情况
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('项目名称', max_length=50, unique=True, null=False)
    # 项目相关人，json格式的字符串，由成员和身份组成。
    project_participant = models.TextField("项目成员", null=False)
    desc = models.CharField('项目描述', max_length=100, null=True)
    create_time = models.DateTimeField('项目创建时间', auto_now_add=True)
    update_time = models.DateTimeField('项目更新时间', auto_now=True, null=True)

    # 打印对象时返回项目名称
    def __str__(self):
        return self.name

    # Meta类用于定义Model的元数据，即不属于Model的字段，但是可以用来标识它的一些属性
    class Meta:
        verbose_name = '项目信息表'
        verbose_name_plural = '项目信息表'


class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    case_name = models.CharField('用例名称', max_length=50, null=False)  # 如 register
    belong_project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    request_data = models.CharField('请求数据', max_length=1024, null=False, default='')
    uri = models.CharField('接口地址', max_length=1024, null=False, default='')
    assert_key = models.CharField('断言内容', max_length=1024, null=True)
    maintainer = models.CharField('编写人员', max_length=1024, null=False, default='')
    extract_var = models.CharField('提取变量表达式', max_length=1024, null=True)  # 示例：userid||userid": (\d+)
    request_method = models.CharField('请求方式', max_length=1024, null=True)
    status = models.IntegerField(null=True, help_text="0：表示有效，1：表示无效，用于软删除")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='责任人', null=True)

    def __str__(self):
        return self.case_name

    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = '测试用例表'


# 线上接口的数据，每次发布自动获取最新的接口请求内容，用于流量回放，目前是每次都捕获，集成上流水线之后变为发布后第一次捕获。
class ApiData(models.Model):
    id = models.AutoField(primary_key=True)
    target_api = models.URLField('目标http接口')
    api_request_data = models.TextField('请求内容')
    api_response_data = models.TextField('响应内容')

    def __str__(self):
        return self.target_api

    class Meta:
        verbose_name = '流量离线数据'
        verbose_name_plural = '流量离线数据'


class InterfaceServer(models.Model):
    id = models.AutoField(primary_key=True)
    env = models.CharField('环境', max_length=50, null=False, default='')
    ip = models.CharField('ip', max_length=50, null=False, default='')
    port = models.CharField('端口', max_length=100, null=False, default='')
    remark = models.CharField('备注', max_length=100, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return self.env

    class Meta:
        verbose_name = '接口地址配置表'
        verbose_name_plural = '接口地址配置表'


# 测试用例执行记录
class TestCaseExecuteResult(models.Model):
    id = models.AutoField(primary_key=True)
    belong_test_case = GroupedForeignKey(TestCase, "belong_test_case", on_delete=models.CASCADE, verbose_name='所属用例')
    status = models.IntegerField(null=True, help_text="0：表示未执行，1：表示已执行")
    exception_info = models.CharField(max_length=2048, blank=True, null=True)
    request_data = models.CharField('请求体', max_length=1024, null=True)  # {"code": "00", "userid": 22889}
    response_data = models.CharField('响应字符串', max_length=1024, null=True)  # {"code": "00", "userid": 22889}
    execute_result = models.CharField('执行结果', max_length=1024, null=True)  # 成功/失败
    extract_var = models.CharField('关联参数', max_length=1024, null=True)  # 响应成功后提取变量
    last_time_response_data = models.CharField('上一次响应字符串', max_length=1024, null=True)  # {"code": "00", "userid": 22889}
    execute_total_time = models.CharField('执行耗时', max_length=1024, null=True)
    execute_start_time = models.CharField('执行开始时间', max_length=300, blank=True, null=True)
    execute_end_time = models.CharField('执行结束时间', max_length=300, blank=True, null=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '用例执行结果记录表'
        verbose_name_plural = '用例执行结果记录表'