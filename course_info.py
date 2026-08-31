def course_info(course):
    info_text = f"课程名称：{course['kcmc']} | 本科生容量：{course['bksrl']} | 已选人数：{course['bksyxrs']} | 当前选课系数：{course['xkxs']}"

    with open('course_info.txt', 'a', encoding='utf-8') as f:
        f.write(info_text + '\n')

    return info_text