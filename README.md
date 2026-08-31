# 南科大课程容量监控工具

自动登录南科大 CAS 系统，查询当前学期已选课程的容量与选课人数。

## 功能
- CAS 统一认证登录
- 获取已选课程列表
- 显示课程容量、已选人数

## 安装与使用
1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 复制 `.env.example` 为 `.env`，填写学号与密码
4. 运行：`python main.py`

## 注意事项
- 仅供个人学习使用，请遵守学校相关规定。
- 请勿频繁请求，避免账号被锁定。

## 依赖
- Python 3.8+
- requests
- beautifulsoup4
- python-dotenv
- tabulate
