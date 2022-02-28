from django.shortcuts import render
import difflib

# Create your views here.

# 专项测试视图

# 回放流量，生成difflib
def re_rate(request):
    base_url = "127.0.0.1:8000"
    response = request()


def special_test(request):
    # 获取指定的API
    request.POST.get()
