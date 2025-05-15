# Fancy University Management System using OOP and Streamlit

import streamlit as st
import streamlit.components.v1 as components

# ========== Page Configuration ==========
st.set_page_config(page_title="Noor University System", page_icon="🎓", layout="centered")
st.markdown("""
    <style>
        .main {
            background-color: #f5f3ff;
        }
        .css-18e3th9 {
            background-color: #ede9fe;
        }
        .stButton>button {
            color: white;
            background-color: #6b21a8;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .footer {
            text-align: center;
            color: gray;
            margin-top: 2rem;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#4b0082;'>🌟 Welcome to Noor University Management Portal 🌟</h2>", unsafe_allow_html=True)

# ========== Base Class ==========
class Person:
    def __init__(self, my_name, my_age):
        self.name = my_name
        self.age = my_age

    def get_details(self):
        return f"Name: {self.name}, Age: {self.age}"


# ========== Student Class ==========
class Student(Person):
    def __init__(self, my_name, age, roll_number):
        super().__init__(my_name, age)
        self.roll_number = roll_number
        self.courses = []

    def register_for_course(self, course):
        if course not in self.courses:
            self.courses.append(course)


# ========== Instructor Class ==========
class Instructor(Person):
    def __init__(self, my_name, age, employee_id):
        super().__init__(my_name, age)
        self.employee_id = employee_id
        self.department = None

    def assign_department(self, department):
        self.department = department


# ========== Course Class ==========
class Course:
    def __init__(self, course_id, name, department):
        self.course_id = course_id
        self.name = name
        self.department = department


# ========== Department Class ==========
class Department:
    def __init__(self, dept_name):
        self.dept_name = dept_name


# ========== Session State Initialization ==========
if "students" not in st.session_state:
    st.session_state.students = []
if "instructors" not in st.session_state:
    st.session_state.instructors = []
if "courses" not in st.session_state:
    st.session_state.courses = []
if "departments" not in st.session_state:
    st.session_state.departments = []

# ========== Streamlit Menu ==========
menu = st.sidebar.selectbox("📋 Menu", [
    "Add Department", "Add Course", "Add Student", "Add Instructor",
    "Assign Instructor", "Register Student", "View All"
])

# ========== Add Department ==========
if menu == "Add Department":
    dept_name = st.text_input("Enter Department Name")
    if st.button("Add Department"):
        if dept_name:
            st.session_state.departments.append(Department(dept_name))
            st.success(f"Department '{dept_name}' added successfully.")
        else:
            st.warning("Please enter department name.")

# ========== Add Course ==========
elif menu == "Add Course":
    course_id = st.text_input("Course ID")
    course_name = st.text_input("Course Name")
    if st.session_state.departments:
        department = st.selectbox("Select Department", [d.dept_name for d in st.session_state.departments])
        if st.button("Add Course"):
            if course_id and course_name and department:
                st.session_state.courses.append(Course(course_id, course_name, department))
                st.success(f"Course '{course_name}' added successfully.")
            else:
                st.warning("Please fill in all fields.")
    else:
        st.warning("Please add a department first.")

# ========== Add Student ==========
elif menu == "Add Student":
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=16, max_value=100, step=1)
    roll_no = st.text_input("Roll Number")
    if st.button("Add Student"):
        if name and roll_no:
            st.session_state.students.append(Student(name, age, roll_no))
            st.success(f"Student '{name}' added successfully.")
        else:
            st.warning("Please fill in all fields.")

# ========== Add Instructor ==========
elif menu == "Add Instructor":
    name = st.text_input("Instructor Name")
    age = st.number_input("Age", min_value=20, max_value=100, step=1)
    emp_id = st.text_input("Employee ID")
    if st.button("Add Instructor"):
        if name and emp_id:
            st.session_state.instructors.append(Instructor(name, age, emp_id))
            st.success(f"Instructor '{name}' added successfully.")
        else:
            st.warning("Please fill in all fields.")

# ========== Assign Instructor ==========
elif menu == "Assign Instructor":
    if st.session_state.instructors and st.session_state.departments:
        instructor_name = st.selectbox("Select Instructor", [i.name for i in st.session_state.instructors])
        department = st.selectbox("Select Department", [d.dept_name for d in st.session_state.departments])
        if st.button("Assign"):
            instructor = next((i for i in st.session_state.instructors if i.name == instructor_name), None)
            if instructor:
                instructor.assign_department(department)
                st.success(f"{instructor_name} assigned to {department} department")
            else:
                st.warning("Instructor not found.")
    else:
        st.warning("Please ensure both instructors and departments are added first.")

# ========== Register Student ==========
elif menu == "Register Student":
    if st.session_state.students and st.session_state.courses:
        student_name = st.selectbox("Select Student", [s.name for s in st.session_state.students])
        course_name = st.selectbox("Select Course", [c.name for c in st.session_state.courses])
        if st.button("Register"):
            student = next((s for s in st.session_state.students if s.name == student_name), None)
            course = next((c for c in st.session_state.courses if c.name == course_name), None)
            if student and course:
                student.register_for_course(course)
                st.success(f"{student_name} registered for {course_name}")
            else:
                st.warning("Student or course not found.")
    else:
        st.warning("Please ensure students and courses are added first.")

# ========== View All ==========
elif menu == "View All":
    st.subheader("📚 Students")
    for s in st.session_state.students:
        st.markdown(f"**{s.get_details()}**, Roll No: `{s.roll_number}`")
        if s.courses:
            st.markdown(f"Registered Courses: `{', '.join([c.name for c in s.courses])}`")
        else:
            st.markdown("Registered Courses: `None`")

    st.subheader("🧑‍🏫 Instructors")
    for i in st.session_state.instructors:
        st.markdown(f"**{i.get_details()}**, Employee ID: `{i.employee_id}`")
        st.markdown(f"Department: `{i.department if i.department else 'Not Assigned'}`")

    st.subheader("📘 Courses")
    for c in st.session_state.courses:
        st.markdown(f"`{c.course_id}` - **{c.name}** ({c.department})")

    st.subheader("🏢 Departments")
    for d in st.session_state.departments:
        st.markdown(f"**{d.dept_name}**")

# ========== Footer ==========
st.markdown("""
<hr>
<p class='footer'>Designed & Developed by Ismat Fatima - 2025</p>
""", unsafe_allow_html=True)