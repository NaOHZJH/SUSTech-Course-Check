# /config.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    """Configuration class to hold environment variables."""
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    XN = os.getenv("XN")
    XQ = os.getenv("XQ")

    DEBUG = os.getenv("DEBUG", "False").lower() == 'true'

    CAS_LOGIN_URL = "https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas"
    TIS_BASE = "https://tis.sustech.edu.cn"
    QUERY_YXKC_URL = TIS_BASE + "/Xsxk/queryYxkc"

    # ---- 输出文件位置 ----
    # 所有程序生成的输出文件统一放在 OUTPUT_DIR 下
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

    # 课程信息文本输出
    COURSE_INFO_FILE = os.path.join(OUTPUT_DIR, "course_info.txt")

    # 查询异常时的调试响应
    RESP_FILE = os.path.join(OUTPUT_DIR, "resp.txt")

    # 课表导出文件路径（显式配置优先）
    SCHEDULE_FILE = os.getenv("SCHEDULE_FILE") or os.path.join(OUTPUT_DIR, "course_schedule.xlsx")

    # ICS 日历课表导出文件路径（显式配置优先）
    ICS_FILE = os.getenv("ICS_FILE") or os.path.join(OUTPUT_DIR, "course_schedule.ics")

    # 开学第一周周一日期（格式 YYYY-MM-DD），用于 ICS 课表计算具体日期
    SEMESTER_START = os.getenv("SEMESTER_START")