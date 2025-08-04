# 创建一个三层嵌套的Python字典
student = {
    'personal_info': {
        'name': '张三',
        'age': 20,
        'contact': {
            'email': 'zhangsan@example.com',
            'phone': '123-456-7890',
            'address': {
                'city': '北京',
                'district': '海淀区',
                'street': '中关村大街1号'
            }
        }
    },
    'academic': {
        'major': '计算机科学',
        'courses': {
            'CS101': {
                'name': '编程基础',
                'grade': 'A',
                'credits': 3
            },
            'CS102': {
                'name': '数据结构',
                'grade': 'B+',
                'credits': 4
            }
        }
    }
}

print('\n三层嵌套的Python字典示例：')
print('\n1. 访问第一层：')
print(f"学生专业: {student['academic']['major']}")

print('\n2. 访问第二层：')
print(f"联系电话: {student['personal_info']['contact']['phone']}")

print('\n3. 访问第三层：')
print(f"住址-城市: {student['personal_info']['contact']['address']['city']}")
print(f"课程CS101成绩: {student['academic']['courses']['CS101']['grade']}")

print('\n4. 遍历嵌套字典：')
print('\n所有课程信息：')
for course_code, course_info in student['academic']['courses'].items():
    print(f"  课程代码: {course_code}")
    print(f"  课程名称: {course_info['name']}")
    print(f"  课程成绩: {course_info['grade']}")
    print(f"  学分: {course_info['credits']}")
    print()