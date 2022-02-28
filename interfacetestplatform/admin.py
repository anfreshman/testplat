from django.contrib import admin

# Register your models here.
from .import models


class ProjectAdmin(admin.ModelAdmin):
    # 指定显示在修改页面上的字段
    list_display = ("id", "name", "project_participant", "desc", "create_time", "update_time")

admin.site.register(models.Project, ProjectAdmin)

class TestCaseAdmin(admin.ModelAdmin):
    list_display = (
        "id", "case_name", "belong_project", "request_data", "uri", "assert_key", "maintainer",
        "extract_var", "request_method", "status", "created_time", "updated_time", "user")

admin.site.register(models.TestCase, TestCaseAdmin)