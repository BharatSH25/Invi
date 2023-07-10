from django.shortcuts import render,redirect
from django.contrib import messages
from schedule.forms import tt1

from exam_invigilator import settings
from django.core.mail import send_mail,EmailMessage

from django.http import HttpResponse 
from schedule.models import faculty,room,exam,student,tt,adminlogin,conduct,constraints,feed,head

def home(request):
	
	return render(request,'schedule/home.html')
#home page-college image
def first(request):
	return render(request,'schedule/first.html')
#feedback page
def feedback(request):
	if request.method=="POST":
		name=request.POST['name']
		email=request.POST['email']
		cc=request.POST['cc']
		feed.objects.create(name=name,email=email,feedback=cc)
		return render(request,'schedule/home.html')

	return render(request,'schedule/feedback.html')
#adminLogin page--uses username,password
def admin1(request):
	if request.method=="POST":
		uname=request.POST['uname']
		passwd=request.POST['password']
		data=adminlogin.objects.get(username=uname,password=passwd)
		try:
			if data:
				d=exam.objects.all()
				return render(request,'schedule/adminpage.html',{'data':d})
		
		except Exception:
			#return HttpResponse("please enter correct details...!!!")

			messages.warning(request,'Please enter valid details!!!.......')
			return render(request,'schedule/admin.html')
			

	return render(request,'schedule/admin.html')

#facultylogin--user id,email,department
def fac(request):
	if request.method=="POST":
		id1=request.POST['id']
		email=request.POST['email']
		dept=request.POST['uname']
		try:
			data=faculty.objects.get(faculty_id=id1,email=email,dept=dept)
			if data:
				return render(request,'schedule/facstart.html',{'data':data})
		except Exception:
			messages.warning(request,'Please enter valid details!!!.......')
			return render(request,'schedule/faculty.html')


	return render(request,'schedule/faculty.html')
#studentLogin--uses username,rollno
def stud(request):
	if request.method=="POST":
		uname=request.POST['uname']
		rno=request.POST['rno']
		
		try:
			data=student.objects.get(student_name=uname,rollno=rno)
			if data:
				
				return render(request,'schedule/studstart1.html',{'data':data})
		except Exception:
			#return HttpResponse("please enter correct details...!!!")

			messages.warning(request,'Please enter valid details!!!.......')
			return render(request,'schedule/student.html')
			

	return render(request,'schedule/student.html')
#deleting one exam which is already in timetable,cid---exam id in tt
def delete(request,cid):
	d=conduct.objects.get(id=cid)
	d.delete()
	data=conduct.objects.select_related('ex','fna1','room').all()
	return render(request,'schedule/timetable.html',{'data':data})

#displaying timetable

def timetable(request):
	
	data=conduct.objects.select_related('ex','fna1','room').all()
	return render(request,'schedule/timetable.html',{'data':data})

def adminpage(request):
	#d=exam.objects.all()
	dy=faculty.objects.filter(faculty_status='y',designation__in=['ASSISTANT PROFESSOR']).all()
	
	exam_ids_in_conduct = conduct.objects.values_list('ex_id', flat=True)
	d = exam.objects.exclude(id__in=exam_ids_in_conduct).all()
	#d = exam.objects.exclude(conduct__ex__isnull=False).values_list('id', flat=True).all()
	print(d)
	if request.method=='POST':
		exid=request.POST['id']
		try:
			d1=exam.objects.get(id=exid)
			print(d1)
			
			if d1:
				#redirecting to assignfac page by sending all details of faculty,roomno
				d1=exam.objects.get(id=exid)
				
				
				s1=conduct.objects.filter(ex=d1).values('fna1')
				s2=conduct.objects.filter(ex=d1).values('room')

				#excluding faculty who are already assigned to that exam id--fac1,fac2
				dy=faculty.objects.filter(faculty_status='y',designation__in=['ASSISTANT PROFESSOR']).exclude(fname__in=s1)
				
				data3=room.objects.filter(room_status='y').exclude(roomno__in=s2)
				s3=conduct.objects.filter(ex=d1).values('fna2')
				dx=faculty.objects.filter(faculty_status='y',designation__in=['HOD','PROFESSOR'])
				dc=faculty.objects.filter(faculty_status='y',designation__in=['PRINCIPAL','VICE PRINCIPAL','DEAN','ASSOCIATE DEAN'])
				dz=dy.exclude(fname__in=s3)
				return render(request,'schedule/assignfac.html',{'x':d1,'y':dz,'z':data3,'s':dx,'dc':dc})
		except Exception as e:
			print(str(e))
			messages.warning(request,'Please provide valid exam ID..or go to create exam for new exam..!')
			
			return render(request,'schedule/adminpage.html',{'data':d})
	
	return render(request,'schedule/adminpage.html',{'data':d})
	

#To add a new exam with exam id,date,time and aslo heading hx
def addexam(request):
	data=exam.objects.all()
	hx=head.objects.first()
	if request.method=='POST':
		i=request.POST['id']
		date=request.POST['date']
		start_time=request.POST['stime']
		end_time=request.POST['etime']
		sem=request.POST['sem']
		sub=request.POST['sub']
		depts=request.POST['dept']
		

		try:
			data=exam.objects.create(id=i,exam_date=date,exam_stime=start_time,exam_etime=end_time,semester=sem,subject=sub,dept=depts)
			data=exam.objects.all()
			hx=head.objects.first()

			return render(request,'schedule/addexam.html',{'data':data,'data1':hx})
	
		except Exception:
			data=exam.objects.all()
			messages.warning(request,'Please enter valid details!!!.......')
			return render(request,'schedule/addexam.html',{'data':data,'data1':hx})
		
	return render(request,'schedule/addexam.html',{'data':data,'data1':hx})

#deleting exam in create exam page which deletes that date,time,id
def dele(request,exid):
	d=exam.objects.get(id=exid)
	d.delete()
	data=exam.objects.all()
	hx=head.objects.first()
	return render(request,'schedule/addexam.html',{'data':data,'data1':hx})
      
#faculty assignment
def assignfac(request,exid):
	if request.method=="POST":
		try:
			i=exid
			fna=request.POST['fna1']
			f=request.POST['fna2']
			fna3=request.POST['fna3']
			ro=request.POST['room']
			
			exobj=exam.objects.get(id=i)
			r=room.objects.get(roomno=ro)
			x=faculty.objects.get(fname=fna)
		
			#if fac1,fac2 are different assign
			if x.fname!=f:
				data=conduct.objects.create(fna1=x,ex=exobj,fna2=f,room=r,fna3=fna3)
			if data:
				#redirecting with fresh data(excluding the above assigned faculty to that exam id) to same page.
				exam_ids_in_conduct = conduct.objects.values_list('ex_id', flat=True)
				d = exam.objects.exclude(id__in=exam_ids_in_conduct).all()
				d1=exam.objects.get(id=exid)
				s1=conduct.objects.filter(ex=d1).values('fna1')
				s2=conduct.objects.filter(ex=d1).values('room')
				dy=faculty.objects.filter(faculty_status='y').exclude(fname__in=s1)
				data3=room.objects.filter(room_status='y').exclude(roomno__in=s2)
				s3=conduct.objects.filter(ex=d1).values('fna2')
				dz=dy.exclude(fname__in=s3)
				return render(request,'schedule/adminpage.html',{'data':d})
		except Exception:
			messages.warning(request,'Please enter  valid details!!!.......')
			exam_ids_in_conduct = conduct.objects.values_list('ex_id', flat=True)
			d=exam.objects.exclude(id__in=exam_ids_in_conduct).all()
			return render(request,'schedule/adminpage.html',{'data':d})
	
	d1=exam.objects.get(id=exid)
	s1=conduct.objects.filter(ex=d1).values('fna1')
	s3=conduct.objects.filter(ex=d1).values('fna2')
	
	dy=faculty.objects.filter(faculty_status='y').exclude(fname__in=s1)
	dz=dy.exclude(fname__in=s3)

	s2=conduct.objects.filter(ex=d1).values('room')
	data3=room.objects.filter(room_status='y').exclude(roomno__in=s2)

	
	
	return render(request,'schedule/assignfac.html',{'x':d1,'y':dz,'z':data3})
#update faculty status
def facstatus(request):
	#data for schedules
	x=tt.objects.filter(Branch='CSE')
	y=tt.objects.filter(Branch='IT')
	z=tt.objects.filter(Branch='ECE')
	w=tt.objects.filter(Branch='EEE')

	if request.method=="POST":
		i=request.POST['id']
		d=faculty.objects.get(faculty_id=i)
		if(d.faculty_status=='y'):
			d.faculty_status='n'
		else:
			d.faculty_status='y'
		d.save()
		data=faculty.objects.all()
		return render(request,'schedule/facultyStatus.html',{'data':data,'x':x,'y':y,'z':z,'w':w})
	data=faculty.objects.all()
	return render(request,'schedule/facultyStatus.html',{'data':data,'x':x,'y':y,'z':z,'w':w})
#update rooomstatus
def roomstatus(request):
	if request.method=="POST":
		i=request.POST['id']
		d=room.objects.get(roomno=i)
		if(d.room_status=='y'):
			d.room_status='n'
		else:
			d.room_status='y'
		d.save()
		data=room.objects.all()
		return render(request,'schedule/roomstatus.html',{'data':data})
	data=room.objects.all()
	return render(request,'schedule/roomstatus.html',{'data':data})
#add new faculty
def addfac(request):
	if request.method=="POST":
		fname=request.POST['fname']
		fid=request.POST['fid']
		fmail=request.POST['fmail']
		fdept=request.POST['fdept']
		st=request.POST['st']
		desig=request.POST['designation']
		ph=request.POST['phone']

		try:
			data=faculty.objects.create(fname=fname,faculty_id=fid,email=fmail,dept=fdept,faculty_status=st,designation=desig,phone=ph)
			messages.success(request,"Created succesfully")
			return render(request,'schedule/addfac.html')
		except Exception as e:
			error_message = str(e)  # Extract the error message
			print(f'An exception occurred: {str(e)}')
			messages.warning(request,'Please enter all details!!!.......')
			return render(request,'schedule/addfac.html')
	return render(request,'schedule/addfac.html')

#add new room
def addroom(request):
	if request.method=="POST":
		fname=request.POST['rno']
		fid=request.POST['rcd']
		st=request.POST['st']
		dept=request.POST['department']
		try:
			data=room.objects.create(roomno=fname,roomcapacity=fid,room_status=st,d=dept)
			return render(request,'schedule/addroom.html')
		except Exception:
			messages.warning(request,'Please enter valid details!!!.......')
			return render(request,'schedule/addroom.html')
	return render(request,'schedule/addroom.html')
#update in timetable by clicking edit symbol
def update(request,cid):
	data=conduct.objects.get(id=cid)
	
	if request.method=="POST":
		i=data.id
		fe=request.POST['fname']
		f=request.POST['fna2']
		ro=request.POST['room']
		sem=request.POST['sem']
		sub=request.POST['sub']
		dept=request.POST['dept']
		
		edit=exam.objects.update(id=data.ex.id,semester=sem,subject=sub)
		data=conduct.objects.select_related('ex','fna1','room').get(id=i)
		r=room.objects.get(roomno=ro)
		x=faculty.objects.get(fname=fe)
		data.fna2=f
		data.fna1=x
		data.room=r
		data.save()

		data1=conduct.objects.select_related('ex','fna1','room').all()
		return render(request,'schedule/timetable.html',{'data':data1})

	
	d1=exam.objects.get(id=data.ex.id)
	s1=conduct.objects.filter(ex=d1).values('fna1')
	s2=conduct.objects.filter(ex=d1).values('room')
	dy=faculty.objects.filter(faculty_status='y').exclude(fname__in=s1)
	data3=room.objects.filter(room_status='y').exclude(roomno__in=s2)

	s3=conduct.objects.filter(ex=d1).values('fna2')
	dz=dy.exclude(fname__in=s3)
	return render(request,'schedule/edit.html',{'data':data,'x':d1,'y':dz,'z':data3})
#faculty page after login
def facstart(request):
	return render(request,'schedule/facstart.html')
#student page after login
def studstart1(request):
	return render(request,'schedule/studstart1.html')
#timetables without edit,delete symbols

def timetable2(request):
	data=conduct.objects.select_related('ex','fna1','room').all()
	hx=head.objects.first()
	return render(request,'schedule/timetable2.html',{'data':data,'h':hx})
def timetable3(request):
	data=exam.objects.all()
	hx=head.objects.first()
	return render(request,'schedule/timetable3.html',{'data':data,'h':hx})
def timetable4(request):
	data=conduct.objects.select_related('ex','fna1','room').all()
	hx=head.objects.first()
	return render(request,'schedule/timetable4.html',{'data':data,'h':hx})
def timetable5(request,fid):
	print(fid)
	n=faculty.objects.get(faculty_id=fid)
	print(n)
	data1=conduct.objects.select_related('ex','fna1','room').filter(fna1=n)
	data2=conduct.objects.select_related('ex','fna1','room').filter(fna2=n.fname)

	hx=head.objects.first()
	return render(request,'schedule/timetable5.html',{'data1':data1,'data2':data2,'h':hx})

#faculty request for admin 
from datetime import date

today = date.today()
def request(request):

	if request.method=="POST":
		try:
			d=request.POST['date']
			i=request.POST['id']
			s1=conduct.objects.filter(ex__exam_date=d).values('fna1')
			s2=conduct.objects.filter(ex__exam_date=d).values('fna2')
			print(s1,s2)
			f1=faculty.objects.filter(fname__in=s1)
			f2=faculty.objects.filter(fname__in=s2)
			print(f1,f2)
			data=faculty.objects.get(faculty_id=i)
			print(data)
			k=0
			
			for i in f1:
				
				if data.fname==i.fname:
					k=1
					d1=conduct.objects.get(fna1=data.fname,ex__exam_date=d)
			
			
			for i in f2:
				if data.fname==i.fname:
					k=2
					d2=conduct.objects.get(fna2=data.fname,ex__exam_date=d)
			
			
			
			if (k==1 and d1.ex.exam_date>today) or (k==2 and d2.ex.exam_date>today):
				constraints.objects.create(cname=data.fname,cdate=d)
				messages.success(request,"REQUEST SENT SUCCESSFULLY..")	
				return render(request,'schedule/request.html')
			else:
				
				
				
				messages.warning(request,"CANNOT PROCEED THE REQUEST!!...PLEASE CHECK THE DATE")
				data=conduct.objects.select_related('ex','fna1','room').all()
				return render(request,'schedule/timetable2.html',{'data':data})
			
		except Exception as e:
			print(f'An exception occurred: {str(e)}')
			messages.warning(request,"please enter your details correctly")
			return render(request,'schedule/request.html')
	return render(request,'schedule/request.html')
#faculty constraints
def facconstraints(request):
	data=constraints.objects.all()
	return render(request,'schedule/facconstraints.html',{'data':data})
#deleting faculty constarints
def delet(request,id):
	data=constraints.objects.get(id=id)
	data.delete()
	data=constraints.objects.all()
	return render(request,'schedule/facconstraints.html',{'data':data})
#add some schedules
def addtt(req):
	form=tt1()
	if  req.POST:
		data=tt1(req.POST,req.FILES)
		if data.is_valid():
			data.save()
			messages.success(req,"ADDED SUCCESSFULLY..")	
			return render(req,'schedule/addtt.html',{'form':form})
	
	return render(req,'schedule/addtt.html',{'form':form})
#show schedules
def showtt(req,name):
	try:
		d=tt.objects.get(Section=name)
		return render(req,'schedule/showtt.html',{'info':d})
	except Exception:
		messages.warning(req,'Looks like there is no timetable with this name.')
		return render(req,'schedule/addtt.html')
#delete schedules
def deltt(req,name):
	d=tt.objects.get(Section=name)
	d.delete()
	form=tt1()
	return render(req,'schedule/addtt.html',{'form':form})
#sending email to faculty

def send_email(request):
	data1=conduct.objects.select_related('ex','fna1','room').values('fna1')
	data2=conduct.objects.select_related('ex','fna1','room').values('fna2')
	f1=faculty.objects.filter(fname__in=data1)
	f2=faculty.objects.filter(fname__in=data2)
	l=[]
	for i in f1:
		l.append(i.email)
	for i in f2:
		l.append(i.email)
	if request.method=="POST":
		
		sub=request.POST['sub']
		body=request.POST['message']
		file=request.FILES['file']

		sender=settings.EMAIL_HOST_USER
		

		email=EmailMessage(sub,body,sender,l)
		email.content_subtype='html'
		email.attach(file.name,file.read(),file.content_type)
		email.send()

		messages.success(request,"MAIL SENT SUCCESSFULLY")
		return render(request,'schedule/email.html',{'data':l})

	return render(request,'schedule/email.html',{'data':l})
#heading
def head1(request):
	data1=head.objects.first()
	data=exam.objects.all()
	if request.method=="POST":
		heading=request.POST['heading']
		data1.heading=heading
		data1.save()
		return render(request,'schedule/addexam.html',{'data':data,'data1':data1})
	return render(request,'schedule/addexam.html',{'data':data,'data1':data1})
	
def facrequests(request):
	data=constraints.objects.all()
	return render(request,'schedule/facrequests.html',{'data':data})

def automatic(request):
	#exam_data = exam.objects.all()
	exam_ids_in_conduct = conduct.objects.values_list('ex_id', flat=True)
	exam_data = exam.objects.exclude(id__in=exam_ids_in_conduct).all()
	faculty_data=faculty.objects.filter(faculty_status='y',designation__in=['ASSISTANT PROFESSOR']).all()
	room_data=room.objects.all()
	import pandas as pd
	exam_df = pd.DataFrame(list(exam_data.values('id', 'exam_date', 'exam_stime', 'exam_etime', 'semester', 'dept', 'subject')))
	room_df=pd.DataFrame(list(room_data.values('roomno','roomcapacity','room_status','d')))
	faculty_df=pd.DataFrame(list(faculty_data.values('fname','faculty_id','faculty_status','email','dept','designation','phone')))
	new_df = pd.DataFrame(columns=[ 'id','exam_date','exam_stime','Room', 'Department', 'Invigilator'])
	for index, row in exam_df.iterrows():
		id=row['id']
		exam_date = row['exam_date']
		exam_time = row['exam_stime']
		room_number = room_df.loc[index % len(room_df), 'roomno']
		department = room_df.loc[index % len(room_df), 'd']
		invigilator_name = faculty_df.loc[index % len(faculty_df), 'fname']
		new_df.loc[index] = [id,exam_date, exam_time, room_number, department, invigilator_name]
	superintendent_data=faculty.objects.filter(faculty_status='y',designation__in=['PROFESSOR','HOD']).all()
	superintendent_df = pd.DataFrame(list(superintendent_data.values('fname')))
	#for deputy chiefs
	dc_data=faculty.objects.filter(faculty_status='y',designation__in=['PRINCIPAL','VICE PRINCIPAL','DEAN','ASSOCIATE DEAN']).all()
	dc_df=pd.DataFrame(list(dc_data.values('fname')))

	departments = new_df['Department'].tolist()
	date_based=new_df['exam_date'].tolist()
	s_df= pd.DataFrame(columns=['Superintendent'])

	deputy_df=pd.DataFrame(columns=['Deputy'])
	groups = []
	current_group = []
	for i in range(len(departments)):
		if i == 0 or departments[i] == departments[i-1]:
			current_group.append(departments[i])
		else:
			groups.append(current_group)
			current_group = [departments[i]]
	groups.append(current_group)
	superintendent_count = superintendent_df.shape[0]
	deputy_count=dc_df.shape[0]

	superintendent_index=0
	deputy_index=0
	for group in groups:
		d = group[0]
		superintendent_name = superintendent_df.loc[superintendent_index % superintendent_count, 'fname']
		dc_name= dc_df.loc[deputy_index % deputy_count, 'fname']

		superintendent_index += 1
		deputy_index += 1
		for room_number in range(1, len(group) + 1):
			exam_date = exam_df.iloc[room_number - 1]['exam_date']
			exam_time = exam_df.iloc[room_number - 1]['exam_stime']
			s_df.loc[len(s_df)] = [  superintendent_name]
			deputy_df.loc[len(deputy_df)]=[ dc_name]
	combined_df = pd.concat([new_df, s_df,deputy_df], axis=1)
	final_data= combined_df.to_dict('records')


	if request.method=='POST':
		
		try:
			for i in final_data:

				obj=conduct(id=id,fna1=Invigilator,fna2=Superintendent,fna3=Deputy,room=Room)
				obj.save()
			
		except Exception as e:
			print(str(e))

		


	return render(request,'schedule/automatic.html',{'data':final_data})

def save_automatic(request):

	try:
			
			
			for i in final_data:

				obj=conduct(id=id,fna1=Invigilator,fna2=Superintendent,fna3=Deputy,room=Room)
				obj.save()
			print("success")
			return redirect('adminpage')
	except Exception as e:
			print(str(e))
	return redirect('adminpage')



def import_exam(request):
    import pandas as pd
    import datetime
    if request.method == 'POST':

        if 'file' not in request.FILES:
            data=exam.objects.all()
            messages.warning(request,'please enter file')
            return render(request,'schedule/addexam.html',{'data':data})	
        # Retrieve the uploaded file from the request
        file = request.FILES['file']
        
        # Read the Excel file into a DataFrame
        try:
            df = pd.read_excel(file)
        except Exception as e:
            print(str(e))
            return render(request, 'schedule/addexam.html', {'error_message': str(e)})
        
        # Iterate over each row in the DataFrame and create exam objects
        for _, row in df.iterrows():
            # Extract the time range string from the "Time" column
            time_range = row['Time']
            
            # Split the time range into start and end times
            start_time, end_time = time_range.split('-')
            
            # Convert the start and end times to datetime objects
            start_time = datetime.datetime.strptime(start_time.strip(), '%I:%M %p').time()
            end_time = datetime.datetime.strptime(end_time.strip(), '%I:%M %p').time()
            
            # Create exam object with separate exam_stime and exam_etime
            exam_obj = exam(
                id=row['Id'],
                exam_date=row['Date'],
                exam_stime=start_time,
                exam_etime=end_time,
                semester=row['Semester'],
                dept=row['Department'],
                subject=row['Subject']
            )
            exam_obj.save()
            
        data=exam.objects.all()
        messages.success(request,"Imported Successfully")        
        return render(request, 'schedule/addexam.html', {'data': data})
    data=exam.objects.all()
    return render(request, 'schedule/addexam.html',{'data':data})


def import_faculty(request):
	import pandas as pd
	import phonenumbers
	if request.method== 'POST':
		if 'file' not in request.FILES:
			data=faculty.objects.all()
			messages.warning(request,"Please select a file")
			return render(request,'schedule/addfac.html',{'data':data})
		file = request.FILES['file']
		try:
			df=pd.read_excel(file)
			for _, row in df.iterrows():
				dept=row['Department'].upper()
				designation= row['Designation'].upper()
				phone_number = "+91" + str(row['Phone'])
				parsed_number = phonenumbers.parse(phone_number, None)
				formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
				faculty_obj= faculty(fname= row['Name'], faculty_id= row['Id'] ,faculty_status="y", email= row['Email'] , dept=dept, designation=designation,phone= formatted_number)
				faculty_obj.save()
			messages.success(request,"Imported Successfully")
			return render(request,'schedule/addfac.html')
		except Exception as e:
			print(str(e))
			messages.warning(request,"An error occurred while importing")
			return render(request,'schedule/addfac.html')
	return render(request,'schedule/addfac.html')
		











"""
exam_data = exam.objects.all()
faculty_data=faculty.objects.all()
room_data=room.objects.all()
import pandas as pd

exam_df = pd.DataFrame(list(exam_data.values('id', 'exam_date', 'exam_stime', 'exam_etime', 'semester', 'dept', 'subject')))
print(exam_df)
room_df=pd.DataFrame(list(room_data.values('roomno','roomcapacity','room_status','d')))
print(room_df)
faculty_df=pd.DataFrame(list(faculty_data.values('fname','faculty_id','faculty_status','email','dept','designation','phone')))
print(faculty_df)

new_df = pd.DataFrame(columns=[ 'exam_date','exam_stime','Room', 'Department', 'Invigilator'])

for index, row in exam_df.iterrows():
    exam_date = row['exam_date']
    exam_time = row['exam_stime']
    room_number = room_df.loc[index % len(room_df), 'roomno']
    department = room_df.loc[index % len(room_df), 'd']
    invigilator_name = faculty_df.loc[index % len(faculty_df), 'fname']
    
    new_df.loc[index] = [exam_date, exam_time, room_number, department, invigilator_name]
print(new_df)

#for superintendents
superintendent_df = pd.DataFrame(list(faculty_data.values('fname')))

# Get the list of unique departments
departments = new_df['Department'].tolist()
date_based=new_df['exam_date'].tolist()

s_df= pd.DataFrame(columns=[  'Superintendent'])
print("DEpartments",departments)
# Group consecutive departments and assign superintendents
groups = []
current_group = []

for i in range(len(departments)):
    if i == 0 or departments[i] == departments[i-1]:
        current_group.append(departments[i])
    else:
        groups.append(current_group)
        current_group = [departments[i]]

groups.append(current_group)
print(groups)

# Fetch all superintendents from the superintendent dataframe
superintendent_count = superintendent_df.shape[0]
superintendent_index = 0

print(superintendent_count)

# Assign superintendents to each group in a round-robin manner
for group in groups:
    d = group[0]
    superintendent_name = superintendent_df.loc[superintendent_index % superintendent_count, 'fname']
    superintendent_index += 1

    for room_number in range(1, len(group) + 1):
        exam_date = exam_df.iloc[room_number - 1]['exam_date']
        exam_time = exam_df.iloc[room_number - 1]['exam_stime']

        s_df.loc[len(s_df)] = [  superintendent_name]
        
combined_df = pd.concat([new_df, s_df], axis=1)

# Print the combined DataFrame
print(combined_df)
"""