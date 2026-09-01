# /exporter/ICS_exporter.py

import hashlib
import logging
import re
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .base import CourseExporter

logger = logging.getLogger(__name__)

# 节次时间表：{节次: (开始时间, 结束时间)}，按南科大常见作息默认，
# 可通过构造参数 section_times 覆盖
DEFAULT_SECTION_TIMES: Dict[int, Tuple[str, str]] = {
    1: ('08:00', '08:50'),
    2: ('09:00', '09:50'),
    3: ('10:10', '11:00'),
    4: ('11:10', '12:00'),
    5: ('14:00', '14:50'),
    6: ('15:00', '15:50'),
    7: ('16:10', '17:00'),
    8: ('17:10', '18:00'),
    9: ('19:00', '19:50'),
    10: ('20:00', '20:50'),
    11: ('21:00', '21:50'),
    12: ('22:00', '22:50'),
}

# 星期中文
_WEEKDAY_CN = ['一', '二', '三', '四', '五', '六', '日']
_CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7}

_P_HTML_RE = re.compile(r'<p>(.*?)</p>', re.DOTALL)
_WEEKDAY_RE = re.compile(r'(?:星期|周)([一二三四五六日])')
_SECTION_RE = re.compile(r'第(\d+)-(\d+)节')
_WEEKS_RE = re.compile(r'(\d+-\d+)\s*(?:单|双)?周')
_LOCATION_RE = re.compile(r'第\d+-\d+节\s*(.*?)\s*$')


class ICSExporter(CourseExporter):

    def __init__(
        self,
        courses,
        file_path,
        semester_start: Any,
        section_times: Optional[Dict[int, Tuple[str, str]]] = None,
    ):
        """
        :param courses: 课程列表（来自 course_query）
        :param file_path: 输出 .ics 文件路径
        :param semester_start: 开学第一周周一日期，接受 datetime.date 或 'YYYY-MM-DD' 字符串
        :param section_times: 节次时间表覆盖（可选）
        """
        super().__init__(courses, file_path)
        if isinstance(semester_start, str):
            semester_start = date.fromisoformat(semester_start)
        self.semester_start: date = semester_start
        self.section_times = {**DEFAULT_SECTION_TIMES, **(section_times or {})}

    # ------------------------------------------------------------------
    # 解析（与 EXCEL 导出器保持一致的解析结果）
    # ------------------------------------------------------------------

    def _parse_time(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        解析课程时间，返回 {课程名: [时间条目]}。

        时间条目字段：
            weeks     周次字符串，如 '1-16'
            week_type 'all' | 'odd' | 'even'（每周 / 单周 / 双周）
            weekday   1-7（星期一 = 1）
            start     起始节次（从 1 开始）
            end       结束节次
            location  上课地点，如 '一教107'
        """
        result: Dict[str, List[Dict[str, Any]]] = {}

        for course in self.courses:
            name = course.get('kcmc', '')
            if not name:
                continue

            entries = []
            for content in _P_HTML_RE.findall(course.get('pkjgmx', '')):
                content = content.strip()
                if not content:
                    continue

                weekday_m = _WEEKDAY_RE.search(content)
                section_m = _SECTION_RE.search(content)
                weeks_m = _WEEKS_RE.search(content)
                if not (weekday_m and section_m and weeks_m):
                    continue

                if '单周' in content:
                    week_type = 'odd'
                elif '双周' in content:
                    week_type = 'even'
                else:
                    week_type = 'all'

                location_m = _LOCATION_RE.search(content)
                location = location_m.group(1).strip() if location_m else ''

                entries.append({
                    'weeks': weeks_m.group(1),
                    'week_type': week_type,
                    'weekday': _CN_NUM[weekday_m.group(1)],
                    'start': int(section_m.group(1)),
                    'end': int(section_m.group(2)),
                    'location': location,
                })

            if entries:
                result[name] = entries

        self.date_data = result
        return result

    # ------------------------------------------------------------------
    # 导出
    # ------------------------------------------------------------------

    def export(self) -> None:
        """导出课表为 .ics 日历文件（每周展开为独立事件）。"""
        date_data = self._parse_time()

        lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//SUSTech CAS Auto Login//Course Schedule//CN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH',
            'X-WR-CALNAME:课程表',
            'X-WR-TIMEZONE:Asia/Shanghai',
        ]

        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%S')

        for name, entries in date_data.items():
            for e in entries:
                for week_no in self._expand_weeks(e['weeks'], e['week_type']):
                    day = self._date_of_week(week_no, e['weekday'])
                    start_dt, end_dt = self._class_period(day, e['start'], e['end'])
                    if start_dt is None or end_dt is None:
                        continue

                    uid = self._make_uid(name, day, e['start'])
                    desc = (
                        f"第{e['weeks']}周"
                        + self._week_type_label(e['week_type'])
                        + f" 星期{_WEEKDAY_CN[e['weekday'] - 1]} 第{e['start']}-{e['end']}节"
                    )

                    lines.append('BEGIN:VEVENT')
                    lines.append(f'UID:{uid}')
                    lines.append(f'DTSTAMP:{dtstamp}')
                    lines.append(f'DTSTART:{start_dt:%Y%m%dT%H%M%S}')
                    lines.append(f'DTEND:{end_dt:%Y%m%dT%H%M%S}')
                    lines.append(f'SUMMARY:{self._escape(name)}')
                    if e.get('location'):
                        lines.append(f'LOCATION:{self._escape(e["location"])}')
                    lines.append(f'DESCRIPTION:{self._escape(desc)}')
                    lines.append('END:VEVENT')

        lines.append('END:VCALENDAR')

        # RFC 5545：行以 CRLF 结束，长行按 75 字符折叠
        content = '\r\n'.join(self._fold(line) for line in lines) + '\r\n'

        file_path = self.file_path
        if not str(file_path).lower().endswith('.ics'):
            file_path = str(file_path) + '.ics'
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        # newline='' 禁止换行转换，确保 CRLF 原样写入（Windows 下默认会转成 \r\r\n）
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        logger.info(f'课程表已导出：{file_path}')

    # ------------------------------------------------------------------
    # 工具
    # ------------------------------------------------------------------

    def _expand_weeks(self, weeks: str, week_type: str) -> List[int]:
        """把 '1-16' 展开为周次列表，并按单/双周过滤。"""
        m = re.match(r'(\d+)-(\d+)', weeks.strip())
        if not m:
            return []
        start, end = int(m.group(1)), int(m.group(2))
        result = []
        for w in range(start, end + 1):
            if week_type == 'odd' and w % 2 == 0:
                continue
            if week_type == 'even' and w % 2 == 1:
                continue
            result.append(w)
        return result

    def _date_of_week(self, week_no: int, weekday: int) -> date:
        """第 week_no 周星期 weekday（1=周一）的日期。"""
        return self.semester_start + timedelta(weeks=week_no - 1, days=weekday - 1)

    def _class_period(self, day: date, start_section: int, end_section: int):
        """根据节次时间表返回 (开始datetime, 结束datetime)，缺少节次时间时返回 (None, None)。"""
        start_hm = self.section_times.get(start_section)
        end_hm = self.section_times.get(end_section)
        if not start_hm or not end_hm:
            logger.warning(f'缺少第{start_section}-{end_section}节的作息时间，跳过该课程时段')
            return None, None
        sh, sm = map(int, start_hm[0].split(':'))
        eh, em = map(int, end_hm[1].split(':'))
        return (
            datetime.combine(day, time(sh, sm)),
            datetime.combine(day, time(eh, em)),
        )

    @staticmethod
    def _week_type_label(week_type: str) -> str:
        if week_type == 'odd':
            return '（单周）'
        if week_type == 'even':
            return '（双周）'
        return ''

    @staticmethod
    def _make_uid(name: str, day: date, start_section: int) -> str:
        raw = f'{name}|{day.isoformat()}|{start_section}'
        digest = hashlib.md5(raw.encode('utf-8')).hexdigest()
        return f'{digest}@cas-auto-login'

    @staticmethod
    def _escape(text: str) -> str:
        """转义 ICS 保留字符：反斜杠、分号、逗号。"""
        return (
            text.replace('\\', '\\\\')
            .replace(';', '\\;')
            .replace(',', '\\,')
        )

    @staticmethod
    def _fold(line: str, limit: int = 75) -> str:
        """RFC 5545 行折叠：超过 limit 字符的行走行，续行以空格开头。"""
        if len(line) <= limit:
            return line
        parts = [line[i:i + limit] for i in range(0, len(line), limit)]
        return '\r\n '.join(parts)
