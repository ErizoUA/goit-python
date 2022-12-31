
# 5 студентів із найбільшим середнім балом з усіх предметів.
q1 = '''
SELECT st.name, round(avg(g.grade), 2) AS avg_grade
FROM grades g
JOIN students st ON st.id = g.student_id
GROUP BY st.name
ORDER BY avg_grade DESC
LIMIT 5
;
'''

# 1 студент із найвищим середнім балом з одного предмета.
q2 = '''
SELECT sub.name, st.name, round(avg(g.grade), 2) AS avg_grade
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
WHERE sub.id = 1
GROUP BY st.name, sub.name
ORDER BY avg_grade DESC
LIMIT 1
;
'''

# Середній бал в групі по одному предмету.
q3 = '''
SELECT sub.name, gr.name, round(avg(g.grade), 2) AS avg_grade
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
JOIN groups gr ON gr.id = st.group_id
WHERE sub.id = 1
GROUP BY gr.name, sub.name
;
'''

# Середній бал у потоці.
q4 = '''
SELECT round(avg(g.grade), 2) AS avg_grade
FROM grades g
;
'''

# Які курси читає викладач.
q5 = '''
SELECT t.name, sub.name
FROM teachers t
JOIN subjects sub ON t.id = sub.teacher_id
WHERE t.id = 1
;
'''

# Список студентів у групі.
q6 = '''
SELECT st.id, st.name, gr.name
FROM students st
JOIN groups gr ON gr.id = st.group_id
WHERE gr.id = 1
;
'''

# Оцінки студентів у групі з предмета.
q7 = '''
SELECT st.id, st.name, sub.name, gr.name, g.grade, g.date_of
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
JOIN groups gr ON gr.id = st.group_id
WHERE sub.id = 1 AND gr.id = 1
;
'''

# Оцінки студентів у групі з предмета на останньому занятті.
q8 = '''
SELECT st.name, sub.name, gr.name, g.grade, g.date_of
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
JOIN groups gr ON gr.id = st.group_id
WHERE sub.id = 1 AND gr.id = 1 AND g.date_of = (SELECT g.date_of
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN groups gr ON gr.id = st.group_id
WHERE g.subject_id = 1 AND gr.id = 1
ORDER BY g.date_of DESC
LIMIT 1)
;
'''

# Список курсів, які відвідує студент.
q9 = '''
SELECT sub.name, st.name
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
WHERE g.student_id = 1
GROUP BY sub.name
;
'''

# Список курсів, які студенту читає викладач.
q10 = '''
SELECT st.name, t.name, sub.name
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
JOIN teachers t ON t.id = sub.teacher_id
WHERE t.id = 1 AND g.student_id = 1
GROUP BY sub.name
;
'''

# Середній бал, який викладач ставить студенту.
q11 = '''
SELECT DISTINCT st.name, t.name, round(avg(g.grade), 2) AS avg_grade
FROM grades g
JOIN students st ON st.id = g.student_id
JOIN subjects sub ON sub.id = g.subject_id
JOIN teachers t ON t.id = sub.teacher_id
WHERE t.id = 1 AND st.id = 1
GROUP BY st.name
;
'''

# Середній бал, який ставить викладач.
q12 = '''
SELECT t.name, round(avg(g.grade), 2) AS avg_grade
FROM grades g
JOIN subjects sub ON sub.id = g.subject_id
JOIN teachers t ON t.id = sub.teacher_id
WHERE t.id = 1
GROUP BY t.name
;
'''
