from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentCountSeralizers
from rest_framework import status
from .models import Students
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing,String
from django.http import HttpResponse
from reportlab.lib.colors import  HexColor

from reportlab.lib.units import inch
import time
# Create your views here.

@api_view(['GET'])
def api_overview(req):
    overview ={
        'List_all':"all"
    }
    return Response({"Message":"Api Works"})

@api_view(["POST"])
def create_data(req):
    student = StudentCountSeralizers(data=req.data)
    if student.is_valid():
        student.save()
        return Response({'Message':"Student Count Create Successfully"},status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_all_count(req):
    student_counts_all = Students.objects.all()
    student = StudentCountSeralizers(student_counts_all,many=True)
    if not student:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(student.data,status=status.HTTP_200_OK) 

@api_view(["POST"])
def Update_Student_count(req,pk):
    student = Students.objects.get(pk=pk)
    data = StudentCountSeralizers(instance=student,data=req.data)
    if data.is_valid():
        data.save()
        return Response({"Message":"User update Successfully"},status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET",])
def pdf_gen(req):
    items = Students.objects.all()
    items_today = Students.objects.get(date="2023-12-12")
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    logo_path = "https://www.mathworks.com/academia/tah-portal/kpr-institute-of-engineering-and-technology-31501138/_jcr_content/schoolLogo.adapt.full.high.jpg/1594770319547.jpg"  # Replace with the path to your logo image
    logo = Image(logo_path, width=1 * inch, height=1 * inch)  # Adjust the width and height as needed
    elements.append(logo)
    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        name='Products',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=12,
        alignment=1,
    )

    heading_text = 'Students Attendance Report'
    heading_paragraph = Paragraph(heading_text, heading_style)
    elements.append(heading_paragraph)
    print(items_today.total)
    drawing = Drawing(600, 300)
    pc = Pie()
    pc.x = 150
    pc.y = 50
    pc.width = 150
    pc.height = 150
    pc.data = [items_today.on_duty,items_today.total_precent,items_today.total_absent,]
    pc.slices.strokeWidth = 1
    pc.slices[0].popout = 25
    pc.slices[1].popout = 20
    pc.slices[2].popout = 20
    pc.sideLabels = False
    pc.sideLabelsOffset = 1
    title = String(0, 250, "Today Report", fontName='Helvetica-Bold', fontSize=12, fillColor=HexColor('#000000'))

    drawing.add(pc)
    drawing.add(title)

    elements.append(drawing)
    table_data = [['Total', 'Precent', 'Absent', 'Onduty', 'Date']]
    for item in items:
        row = [str(item.total), str(item.total_precent),str(item.total_absent),str(item.on_duty),str(item.date)]
        table_data.append(row)

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.aliceblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table = Table(table_data, repeatRows=1, colWidths=[80, 80])
    table.setStyle(table_style)
    heading_text = 'This Week Report'
    heading_style = ParagraphStyle(
        name='count',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        fontName='Helvetica-Bold',
        spaceAfter=12,
        alignment=0,
    )
    heading_paragraph = Paragraph(heading_text, heading_style)
    elements.append(heading_paragraph)
    elements.append(table)

    doc.build(elements)
    return response


@api_view(["POST"])
def create_Loop(request):
    start_time = time.time()
    my_model = [Students(total=request.data.get("total"), total_precent=request.data.get("total_precent"), total_absent=request.data.get("total_absent"), on_duty=request.data.get("on_duty")) for i in range(3000) ]
    Students.objects.bulk_create(my_model)
    end_time = time.time()
    return Response({"message": "Loop Completed", "execution_time": end_time - start_time}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def update_loop(request,total):
    datas = Students.objects.filter(total=total)
    print(datas)
    print(request.data.get("total"))
    for data in datas:
        data.total = request.data.get("total")
        data.total_precent = request.data.get("total_precent")
        data.total_absent = request.data.get("total_absent")
        data.on_duty = request.data.get("on_duty")
    Students.objects.bulk_update(datas,['total','total_precent','total_absent','on_duty'])
    return Response({"msg":"hi"})
