# /main.py

import logging
import sys
from pathlib import Path
from config import Config
from CAS_Login import cas_login
from course_query import query_selected_course
from course_info import course_info
from exporter.EXCEL_exporter import ExcelExporter
from exporter.ICS_exporter import ICSExporter

# 配置日志
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
    )
logger = logging.getLogger(__name__)

def export_schedule(courses):
    """将课程列表导出为 Excel 课表，失败不影响主流程"""
    if not courses:
        logger.warning("没有课程数据，跳过课表导出")
        return
    try:
        ExcelExporter(courses, Config.SCHEDULE_FILE).export()
        logger.info(f"课表已导出：{Config.SCHEDULE_FILE}")
    except Exception as e:
        logger.error(f"课表导出失败：{e}")

def export_ics(courses):
    """将课程列表导出为 .ics 日历课表，失败不影响主流程"""
    if not courses:
        logger.warning("没有课程数据，跳过 ICS 课表导出")
        return
    if not Config.SEMESTER_START:
        logger.warning("未配置 SEMESTER_START（开学第一周周一日期），跳过 ICS 课表导出")
        return
    try:
        ICSExporter(courses, Config.ICS_FILE, Config.SEMESTER_START).export()
        logger.info(f"ICS 课表已导出：{Config.ICS_FILE}")
    except Exception as e:
        logger.error(f"ICS 课表导出失败：{e}")

def main():
    # 登录
    try:
        session = cas_login(Config.USERNAME, Config.PASSWORD)
    except Exception as e:
        logger.error(f"登陆失败，程序退出：{e}")
        sys.exit(1)
    
    # 查询选课
    try:
        courses = query_selected_course(session)
    except Exception as e:
        logger.error(f"查询选课错误，程序退出：{e}")
        sys.exit(1)

    # 清空历史输出文件，避免多次运行累积重复数据
    Path(Config.COURSE_INFO_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(Config.COURSE_INFO_FILE, 'w', encoding='utf-8') as f:
        f.write('')

    for course in courses:
        logger.info(course_info(course))

    # 导出课表
    export_schedule(courses)
    export_ics(courses)

if __name__ == '__main__':
    main()