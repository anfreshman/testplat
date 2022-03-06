from django.test import TestCase
from .views import project
from django.http import HttpRequest
from .models import Project
# Create your tests here.

def test_project(TestCase):
    def setUp(self):
        print("running {}",{self.__class__.__name__})

    # 从数据库获取项目 - 获取返回值 - 比较
    def test_get_project(self):
        # 获取项目
        projects = Project.objects.filter().order_by('-id')
        flagProject = projects[0]
        # 获取返回值
        request = HttpRequest()
        response = project(request)
        html = response.content.decode('utf8')
        self.assertIn(str(flagProject), html)



