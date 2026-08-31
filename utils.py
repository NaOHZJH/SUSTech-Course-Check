from pathlib import Path
from config import Config

class Utils:
    def course_info(courses):
        info_text_list = []
        for course in courses:
            info_text = f"课程名称：{course['kcmc']} | 本科生容量：{course['bksrl']} | 已选人数：{course['bksyxrs']} | 当前选课系数：{course['xkxs']}"
            Path(Config.COURSE_INFO_FILE).parent.mkdir(parents=True, exist_ok=True)
            with open(Config.COURSE_INFO_FILE, 'a', encoding='utf-8') as f:
                f.write(info_text + '\n')
            info_text_list.append(info_text)
        return info_text_list

    def if_select_course_success(courses):
        active_courses = []
        inactive_courses = []
        danger_courses = []
        for course in courses:
            if course['sxbj'] == '0':
                inactive_courses.append(course['kcmc'])
                rl, yx = int(course['bksrl']), int(course['bksyxrs'])
                if rl <= yx:
                    danger_courses.append([course['kcmc'], course['xkxs']])
            else:
                active_courses.append(course['kcmc'])
        return active_courses, inactive_courses, danger_courses

    def check_danger_courses(self, courses):
        _active, _inactive, _danger = self.if_select_course_success(courses)

        print("以下课程选课人数大于等于课程容量，请注意调整选课积分")
        for i in _danger:
            print(f"课程名称：{i[0]} | 当前选课积分：{i[1]}")

    def export_schedule(courses):
        pass