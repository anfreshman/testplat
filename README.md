# testplat自动化测试平台

## 项目管理（已完成）
Django + mysql + BootStrap，实现了基础的项目相关增删改查

## 测试用例管理（已完成）
Django + mysql + BootStrap，实现了接口测试用例与项目的关联

## 测试用例执行（已完成）
Django

## 测试报告消费（50%）
集成allure生成可观测的测试用例文件，结合飞书机器人做到有失败执行群里通知（飞书机器人部分待开发）

## 专项测试 - 压力测试（初版）
调用tcpcopy功能，实现了在前端页面进行简易压测

## 专项测试 - 流量回放（初版）
捕获每次调用流量，回放时用difflib观察差异
目前方式开放性不足，且对代码有入侵，难以mock数据，考虑参考jvm-sandbox实现简易的AOP中间件

## 专项测试 - 覆盖率统计（初版）
集成coverage.py，生成单元测试覆盖率统计报告

## 流水线发布()
调用Jenkins功能，每次发布触发接口自动化与流量回放

