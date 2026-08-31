# /course_info.py

import os
from pathlib import Path
from config import Config

def course_info(course):
    info_text = f"课程名称：{course.get('kcmc', '')} | 本科生容量：{course.get('bksrl', '')} | 已选人数：{course.get('bksyxrs', '')} | 当前选课系数：{course.get('xkxs', '')}"

    # 确保输出目录存在
    Path(Config.COURSE_INFO_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(Config.COURSE_INFO_FILE, 'a', encoding='utf-8') as f:
        f.write(info_text + '\n')

    return info_text