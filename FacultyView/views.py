from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Student
import qrcode
import socket
import socket
from StudentView.views import present


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print(f"IP Address generated : {ip_address}")


def qrgenerator():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # ip = '192.168.31.35'


    link = f"http://{ip_address}:8000/add_manually"

    # Function to generate and display a QR code
    def generate_qr_code(link):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("FacultyView/static/FacultyView/qrcode.png")

    generate_qr_code(link)


def faculty_view(request):
    if request.method == "POST":
        student_roll = request.POST["student_id"]
        student = Student.objects.get(s_roll=student_roll)
        if student in present:
            present.remove(student)
        return HttpResponseRedirect("/")

    else:
        qrgenerator()
        return render(
            request,
            "FacultyView/FacultyViewIndex.html",
            {
                "students": present,
            },
        )


def add_manually(request):
    students = Student.objects.all().order_by("s_roll")
    return render(
        request,
        "StudentView/StudentViewIndex.html",
        {
            "students": students,
        },
    )
