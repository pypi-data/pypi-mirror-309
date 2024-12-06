from llamarch.common.llm import LLM
from llamarch.patterns.student_teacher import StudentTeacher

llm = LLM(model_category="huggingface",
          model_name="distilbert/distilgpt2")

student_teacher = StudentTeacher(llm, llm)

query = "What are the implications of AI on the job market?"

student_response, teacher_response = student_teacher.generate_response(query)
print(f"Student response: {student_response}")
print(f"Teacher response: {teacher_response}")
student_teacher.train_student([teacher_response])
print("Fine tuning completed!")
fine_tuned_response = student_teacher.student.generate_response(query)
print(f"Fine tuned response: {fine_tuned_response}")
