# /exporter/base.py

from abc import ABC, abstractmethod
import re

class CourseExporter(ABC):

    def __init__(self, courses, file_path):
        self.courses = courses
        self.file_path = file_path

    @abstractmethod
    def export(self) -> None:
        """
        用于导出课程数据
        """
        pass

    def _parse_time(self):
        """
        解析课程时间
        格式示例：1-16周,星期一第9-10节 一教107   {'weeks':'1-16', 'weekday':'1', 'start':'9', 'end':'10', 'if_odd_week':False}
                 2-16双周,星期三第9-10节 一教107 {'weeks':'2-16', 'weekday':'3', 'start':'9', 'end':'10', 'if_odd_week':False}
        """

        weekday_map = {
            '星期一': '1', '星期二': '2', '星期三': '3', '星期四': '4',
            '星期五': '5', '星期六': '6', '星期日': '7',
            '周一': '1', '周二': '2', '周三': '3', '周四': '4',
            '周五': '5', '周六': '6', '周日': '7'
        }
        self.date_data = {}

        for i in self.courses:
            course_name = i.get('kcmc', '')
            p_pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)
            p_content = p_pattern.findall(i.get('pkjgmx', ''))

            _tmp = []
            for content in p_content:
                content = content.strip()
                if not content:
                    continue

                week_day = None
                for cn, num in weekday_map.items():
                    if cn in content:
                        week_day = num
                        break
                if week_day is None:
                    continue

                section_match = re.search(r'第(\d+)-(\d+)节', content)
                weeks_match = re.search(r'(\d+-\d+)\s*(?:单|双)?周', content)
                if not section_match or not weeks_match:
                    continue

                start = section_match.group(1)
                end = section_match.group(2)
                weeks = weeks_match.group(1)

                if '单周' in content:
                    odd = True
                elif '双周' in content:
                    odd = False
                else:
                    odd = False

                _tmp.append({
                    'weeks': weeks,
                    'weekday': week_day,
                    'start': start,
                    'end': end,
                    'if_odd_week': odd
                })

            self.date_data[course_name] = _tmp

        return self.date_data
