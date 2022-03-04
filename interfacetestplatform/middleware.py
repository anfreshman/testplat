# 定义采集装饰器
import django
from . import models

# 如果
class reteReplay(django.utils.deprecation.MiddlewareMixin):
    def process_request(self, request):
        if request.method == "GET":
            if request.GET.get("") == True:
                return None
            else:
                models.ApiData.api_request_data = request
