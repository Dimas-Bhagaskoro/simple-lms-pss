from celery import shared_task
import csv
import os

@shared_task
def test_task():
    print("CELERY WORKS 🎉")
    return "ok"

@shared_task
def send_enrollment_email(email, course_id):
    print(
        f"EMAIL SENT TO {email} FOR COURSE {course_id}"
    )
    return "email sent"

@shared_task
def generate_certificate(user_id, course_id):

    certificate_name = (
        f"certificate_user_{user_id}_course_{course_id}.pdf"
    )

    print(
        f"CERTIFICATE GENERATED: {certificate_name}"
    )

    return certificate_name
@shared_task
def export_course_report(course_id):

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/course_report_{course_id}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "course_id",
            "status"
        ])

        writer.writerow([
            course_id,
            "exported"
        ])

    print(
        f"REPORT EXPORTED: {filename}"
    )

    return filename

@shared_task
def update_course_statistics():

    from courses.models import Enrollment

    total_enrollments = Enrollment.objects.count()

    print(
        f"TOTAL ENROLLMENTS: {total_enrollments}"
    )

    return total_enrollments