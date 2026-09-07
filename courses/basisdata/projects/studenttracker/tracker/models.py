from django.db import models


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    nrp = models.CharField(max_length=50, unique=True)  # Student ID Number
    name = models.CharField(max_length=100)
    email = models.EmailField()
    photo_file = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Path ke file foto atau avatar"
    )

    def __str__(self):
        return f"{self.name} ({self.nrp})"


class Lecturer(models.Model):
    lecturer_id = models.AutoField(primary_key=True)
    lecturer_name = models.CharField(max_length=100)
    lecturer_email = models.EmailField()

    def __str__(self):
        return self.lecturer_name


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    semester = models.IntegerField()
    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.title} ({self.course.course_code})"


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to="submissions/")
    score = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"

    @property
    def status(self):
        """
        Status khusus untuk submission ini:
        - On Time: submitted_at <= due_date
        - Late: submitted_at > due_date
        Status 'Missing' di-hitung di level assignment + student
        (kalau submissio
