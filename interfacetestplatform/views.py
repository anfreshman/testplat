
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import auth  # Django用户认证（Auth）组件一般用在用户的登录注册上，用于判断当前的用户是否合法
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from django.http import HttpResponse
from .form import UserForm
import traceback
import logging
from . import models
from .models import Project, TestCase
from .task import case_task
from specialtest.models import *

# 封装分页处理
def get_paginator(request, data):
    paginator = Paginator(data, 1)  # 默认每页展示10条数据
    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('page')
    try:
        paginator_pages = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        paginator_pages = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    # print("page_num:" + paginator_pages)
    return paginator_pages


# 项目管理页的视图函数
@login_required
def project(request):
    print(request)
    logging.info("request.user.is_authenticated: ", request.user.is_authenticated)  # 打印用户是否已登录
    projects = Project.objects.filter().order_by('-id')  # 使用负id是为了倒序取出项目数据
    # logging.info("projects:{}", projects.number)  # 打印项目名称
    # 构造流量回放的数据
    ApiData.objects.create(target_api="project/", api_request_data=request, api_response_data=render(request, 'project.html', {'projects': get_paginator(request, projects)}))
    return render(request, 'project.html', {'projects': get_paginator(request, projects)})


def index(request):
    return render(request, 'index.html')


def login(request):
    # 打印session
    logging.info("request.session.items(): {}".format(request.session.items()))
    # 如果已经登录
    if request.session.get('is_login', None):
        return redirect('/')
    # 如果是表单提交操作，校验是否合法，内容是否正确
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                # 使用django提供的身份验证功能
                user = auth.authenticate(username=username, password=password)  # 从auth_user表中匹配信息，匹配成功则返回用户对象；反之返回None
                if user is not None:
                    print("用户[%s]登录成功" % username)
                    auth.login(request, user)
                    request.session['is_login'] = True
                    # 登录成功，跳转主页
                    return redirect('/')
                else:
                    message = "用户名不存在或者密码不正确！"
            except:
                traceback.print_exc()
                message = "登录程序出现异常"
            # 用户名或密码为空，返回登录页和错误提示信息
        else:
            return render(request, 'login.html', locals())
        # 不是表单提交，代表只是访问登录页
    else:
        login_form = UserForm()
        return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("/login/")


"""
    项目负责人：0
    研发leader：10
    研发：11
    测试leader：20
    测试：21
    产品leader：30
    产品：31
    运营leader: 40
    运营：41
"""
def getMember():
    pass

# 获取接口路径
def get_server_address(env):
    if env:  # 环境处理
        env_data = models.InterfaceServer.objects.filter(env=env[0])
        print("env_data: {}".format(env_data))
        if env_data:
            ip = env_data[0].ip
            port = env_data[0].port
            print("ip: {}, port: {}".format(ip, port))
            server_address = "http://{}:{}".format(ip, port)
            print("server_address: {}".format(server_address))
            return server_address
        else:
            return ""
    else:
        return ""

# 测试用例菜单项
@login_required
def test_case(request):
    print("request.session['is_login']: {}".format(request.session['is_login']))
    test_cases = ""
    # 页面获取
    if request.method == "GET":
        test_cases = models.TestCase.objects.filter().order_by('id')
        print("testcases: {}".format(test_cases))
    #     表单提交
    elif request.method == "POST":
        print("request.POST: {}".format(request.POST))
        test_case_id_list = request.POST.getlist('test_cases_list')
        env = request.POST.getlist('env')
        print("env: {}".format(env))
        server_address = get_server_address(env)
        if not server_address:
            return HttpResponse("提交的运行环境为空，请选择环境后再提交！")
        if test_case_id_list:
            test_case_id_list.sort()
            print("test_case_id_list: {}".format(test_case_id_list))
            print("获取到用例，开始用例执行")
            # 普通执行
            # case_task(test_case_id_list, server_address)
            # celery 执行
            case_task.apply_async((test_case_id_list, server_address))
        else:
            print("运行测试用例失败")
            return HttpResponse("提交的运行测试用例为空，请选择用例后在提交！")
        test_cases = models.TestCase.objects.filter().order_by('id')
    return render(request, 'test_case.html', {'test_cases': get_paginator(request, test_cases)})
