from http.client import CONFLICT
import logging
import sys
from config import Config
from CAS_Login import cas_login
from course_query import query_selected_course
from course_info import course_info

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
    )
logger = logging.getLogger(__name__)

def main():
    # 登录
    try:
        session = cas_login(Config.USERNAME, Config.PASSWORD)
    except Exception as e:
        logger.error("登陆失败，程序退出")
        sys.exit(1)
    
    # 查询选课
    try:
        courses = query_selected_course(session)
    except Exception as e:
        logger.error("查询选课错误，程序退出")
        sys.exit(1)

    for course in courses:
        logger.info(course_info(course))

if __name__ == '__main__':
    main()