from django.shortcuts import render, redirect
from projects.models import *
from django.http import StreamingHttpResponse, HttpResponse
import cv2
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .forms import RegisterForm, UploadCvForm
from .pdf_handler import extract_pdf
# Create your views here.

def interview_index(request):
  interviews = Interview.objects.all()
  context = {
    'interviews': interviews
  }
  return render(request, 'interview_index.html', context)

def interview_speech_to_text(request):
  context = {
  }
  return render(request, 'interview_speech_to_text.html', context)

@csrf_exempt
def interview_detail(request, pk):
  interview = Interview.objects.get(pk=pk)

  if request.method == 'POST':
    interview.interview_conversation_text = request.POST['send']
    interview.save()

  test = interview.interview_test
  question_tests = QuestionTest.objects.order_by('question_index').filter(test=test)
  questions = []
  for qt in question_tests:
    questions.append(qt.question)
  context = {
    'interview': interview,
    'questions': questions,
  }
  return render(request, 'interview_detail.html', context)


def stream():
  cap = cv2.VideoCapture(0)
  while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
      print("Error: failed to capture image")
      break

    cv2.imwrite('projects/static/stream_frame/demo.jpg', frame)
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + open('projects/static/stream_frame/demo.jpg', 'rb').read() + b'\r\n')


def video_feed(request):
  return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def home(response):
	return render(response, "base.html")

def upload(response):
	
	if response.method == 'POST' and response.FILES['document']:
		upload_file = response.FILES['document']

		file_save = FileSystemStorage()
		filename = file_save.save(upload_file.name, upload_file)
		file_url = file_save.url(filename)
		data = extract_pdf(file_url[1:])
		user = response.user

		resume = Resume(
			resume_created_by = user,
			resume_name = data['name']['value'],
			resume_dob = data['dob']['value'],
			resume_mobile = data['phone']['value'],
			resume_email = data['email']['value'],
			resume_link = data['link']
		)
		resume.save()

		return render(response, "home/upload.html", {"data":data}, {"user":user})
	return render(response, "home/upload.html")

def register(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			un = form.cleaned_data.get('username')
			pss = form.cleaned_data.get('password1')
			print(un, pss)
			form.save()
			return redirect("/login")
		else:
			print("invalid form")
			form = RegisterForm()
	else:
		form = RegisterForm()
	
	return render(response, "register/register.html", {"form":form})
