from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.views import generic,View
from django.views.generic import View
from django import views
from rest_framework import serializers
import MySQLdb,json,operator,random
from collections import OrderedDict
from operator import itemgetter
from random import randint
from peewee import *
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from time_table_models1 import TimetableFinalCourse,TimetableFinalDescipline,TimetableFinalDesciplineCourse,TimetableFinalClassroom,TimetableFinalShift,TimetableFinalTimeslot,TimetableFinalClassroomAvailable,TimetableFinalDay,TimetableFinalFaculty,TimetableFinalSemester,TimetableFinalSubject,TimetableFinalFacultySubject,TimetableFinalLab,TimetableFinalLabAvailable,TimetableFinalSemesterBatch,TimetableFinalSemesterClassroom,TimetableFinalSemesterLab,TimetableFinalSubjectBatch,TimetableFinalSubjectNoStudent,TimetableFinalSubjectScheme,TimetableFinalTimeslotDay,TimetableFinalSubjectDiscipline,TimetableFinalSubjectLab,TimetableFinalTempLab,TimetableFinalFacultyAdd,TimetableFinalFacultySubject1,TimetableFinalFacultyPref1,TimetableFinalFacultyPref,TimetableFinalLabTable,AuthUser
from .models import descipline,course,descipline_course,day,timeslot,lab,classroom,lab_available,classroom_available,semester,subject_no_student,shift,semester_classroom,semester_lab,subject_batch,semester_batch,subject,subject_scheme,faculty,faculty_subject,timeslot_day,subject_discipline,subject_lab,temp_lab
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from . import classroom1


dict_main={}

def db_connect():
	db=MySQLDatabase('time_table_test8',user='root',password='',host='localhost')
	db.connect()
	return db


def db_close(db):
	db.close()


class Faculty(View):
	def get(self,request):
		db=db_connect()
		data2=[]
		for faculty in TimetableFinalFaculty.select().where(TimetableFinalFaculty.descipline_course_table_id==1):
			faculty1=TimetableFinalFacultyAdd.get(TimetableFinalFacultyAdd.faculty_id==faculty.faculty)
			qualification_list = []
			qualification_list=faculty1.qualification.split(",")
			sub_list=[]
			for sub in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.faculty==faculty.faculty):
				sub_list.append({'sub_name':sub.sub_code.sub_name,'sub_code':sub.sub_code.sub_code})
			data2.append({'id':faculty.faculty,'name':faculty.faculty_name,'position':faculty.position,'qualification':qualification_list,'experience':{'academic':faculty1.acedemic,'industrial':faculty1.industrial},'email':faculty.email,'subjects':sub_list,'title':faculty1.title,'workload':faculty.work_load,'profileImg':faculty1.img_url,'discipline':{'id':faculty.descipline_course_table_id.descipline_table_id.id,'name':str(faculty.descipline_course_table_id.descipline_table_id.descipline_name)},'shift':faculty.shift_table_id.shift_name})
		db_close(db)
		return HttpResponse(json.dumps({'data':data2}), content_type="application/json")

	def post(self,request):
		db=db_connect()
		data=json.loads(request.body.decode('utf-8'))
		email=data['faculty']['email']
		subjects=data['faculty']['subjects']
		shift1=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==data['faculty']['shift']).get()
		experience_list=data['faculty']['experience']
		
		a=TimetableFinalFaculty.create(descipline_course_table_id=data['faculty']['discipline']['id'],email=email,faculty_name=data['faculty']['name'],position=data['faculty']['position'],shift_table_id=shift1,work_load=data['faculty']['workload'])
		q=AuthUser.create(username=email,password="123456",is_staff=0,first_name=a.faculty)
		b=TimetableFinalFacultyAdd.create(acedemic=experience_list['academic'],faculty_id=a,industrial=experience_list['industrial'],qualification=','.join(data['faculty']['qualification']),title=data['faculty']['title'],img_url=data['faculty']['profileImg'])
		if len(subjects)>0:
			with db.atomic():
				for sub in subjects:
					TimetableFinalFacultySubject.create(faculty=a,shift_table_id=shift1,sub_code=sub['sub_code'])
		db_close(db)
		if a>0 and b>0 and q>0:
			return HttpResponse(json.dumps({'status':"Success"}), content_type="application/json")
		else:
			return JsonResponse({'status':"Unsuccess"})


@csrf_exempt
def faculty_update(request):
	db=db_connect()
	data=json.loads(request.body.decode('utf-8'))
	a=data['faculty']['id']
	email=data['faculty']['email']
	subjects=data['faculty']['subjects']
	shift1=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==data['faculty']['shift']).get()
	experience_list=data['faculty']['experience']
	TimetableFinalFaculty.update(descipline_course_table_id=data['faculty']['discipline']['id'],email=email,faculty_name=data['faculty']['name'],position=data['faculty']['position'],shift_table_id=shift1,work_load=data['faculty']['workload']).where(TimetableFinalFaculty.faculty==a).execute()
	acedemic_ex=experience_list['academic']
	acedemic_ex1=experience_list['industrial']
	TimetableFinalFacultyAdd.update(acedemic=acedemic_ex,faculty_id=a,industrial=acedemic_ex1,qualification=','.join(data['faculty']['qualification']),title=data['faculty']['title'],img_url=data['faculty']['profileImg']).where(TimetableFinalFacultyAdd.faculty_id==a).execute()	
	AuthUser.update(username=email).where(AuthUser.first_name==a).execute()
	TimetableFinalFacultySubject.delete().where(TimetableFinalFacultySubject.faculty==a).execute()
	for sub in subjects:
		TimetableFinalFacultySubject.create(faculty=a,shift_table_id=shift1,sub_code=sub['sub_code'])
	db_close(db)
	return HttpResponse(json.dumps({'status':"Success"}), content_type="application/json")


@csrf_exempt
def sub_update(request):
	data=request.body.decode('utf-8')
	data_temp=json.loads(data)
	subject=data_temp['name']
	subject_code=data_temp['subcode']
	elective=data_temp['elective']
	batch_list=data_temp['batches']
	shift=data_temp['shift']
	course=data_temp['course']
	discipline=data_temp['discipline']
	temp_course=TimetableFinalCourse.get(TimetableFinalCourse.course_name==course).course
	temp_discipline1=TimetableFinalDescipline.get(TimetableFinalDescipline.descipline_name==discipline).id
	temp_discipline=TimetableFinalDesciplineCourse.get((TimetableFinalDesciplineCourse.course==temp_course)&(TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline1)).id
	semester=data_temp['semester']
	temp_semester=TimetableFinalSemester.get(TimetableFinalSemester.semester_name==semester).id
	no_batch=data_temp['no_batch']
	sub_load=data_temp['load']
	sub_theory=data_temp['schema']['lectures']
	sub_tutorial=data_temp['schema']['tutorials']
	sub_practical=data_temp['schema']['labs']

	query=TimetableFinalSubject.update(is_elective=elective,sub_code=subject_code,sub_name=subject).where(TimetableFinalSubject.sub_code==subject_code)
	query.execute()
	temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==shift).get()
	shift=temp_shift.id
	query4=TimetableFinalSubjectBatch.delete().where(TimetableFinalSubjectBatch.sub_code==subject_code)
	query4.execute()
	if no_batch>0:
		for x in range(no_batch):
			b=batch_list[x]
			query1=TimetableFinalSubjectBatch.create(batch_name=str(b['name']),sub_code=subject_code,shift_table_id=shift)
	query=TimetableFinalSubjectDiscipline.update(descipline_course_table_id=temp_discipline,shift_table_id=shift,sub_code=subject_code).where(TimetableFinalSubjectDiscipline.sub_code==subject_code)
	num1=query.execute()
	query1=TimetableFinalSubjectNoStudent.update(no_batch=no_batch,sub_code=subject_code,shift_table_id=shift).where(TimetableFinalSubjectNoStudent.sub_code==subject_code)
	num2=query1.execute()
	query2=TimetableFinalSubjectScheme.update(sub_code=subject_code,sub_load=sub_load,sub_practical_class=sub_practical,sub_theory_class=sub_theory,sub_tutorial_class=sub_tutorial).where(TimetableFinalSubjectScheme.sub_code==subject_code)
	num3=query2.execute()
	if num1>=0 and num2>=0 and num3>=0:
		return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
	else:
		return HttpResponse(json.dumps({"status":"UnSuccess"}),content_type="application/json")


@csrf_exempt
def login_view(request):
	login_temp=json.loads(request.body.decode('utf-8'))
	username=str(login_temp['username'])
	password=str(login_temp['password'])
	count=AuthUser.select().where((AuthUser.username==username)&(AuthUser.password==password)).count()
	if count>0:
		user=AuthUser.select().where((AuthUser.username==username)&(AuthUser.password==password)).get()
		return JsonResponse({'status':"authorized",'is_superuser':user.is_staff,'id':int(user.first_name)})
	else:
		return JsonResponse({"status":"unauthorized"})


@csrf_exempt
def register_view(request):
	login_temp=json.loads(request.body.decode('utf-8'))
	username=str(login_temp['username'])
	password=str(login_temp['password'])
	type1=login_temp['type']
	id1=login_temp['id']
	AuthUser.create(username=username,password=password,is_staff=type1,first_name=id1)
	return JsonResponse({"status":"Done"})


@csrf_exempt
def single_faculty(request):
	db=db_connect()
	data=json.loads(request.body.decode('utf-8'))
	faculty=TimetableFinalFaculty.get(TimetableFinalFaculty.faculty==int(str(data['id'])))
	faculty_add=TimetableFinalFacultyAdd.get(TimetableFinalFacultyAdd.faculty_id==faculty.faculty)
	db_close(db)
	return HttpResponse(json.dumps({'name':faculty.faculty_name,'load':faculty.work_load,'position':faculty.position-1,'title':faculty_add.title,'profileImg':faculty_add.img_url}), content_type="application/json")


@csrf_exempt
def faculty_delete(request):
	if request.method=='POST':
		db=db_connect()
		data=json.loads(request.body.decode('utf-8'))
		id1=data['id']
		z=TimetableFinalFacultyAdd.delete().where(TimetableFinalFacultyAdd.faculty_id==id1).execute()
		x=TimetableFinalFacultySubject.delete().where(TimetableFinalFacultySubject.faculty==id1).execute()
		y=TimetableFinalFaculty.delete().where(TimetableFinalFaculty.faculty==id1).execute()
		v=AuthUser.delete().where(AuthUser.first_name==id1).execute()
		db_close(db)
		if x>=0 and y>=0 and z>=0 and v>=0:
			return JsonResponse({"status":"Success"})
	return JsonResponse({"status":"Unsuccess"})

@csrf_exempt
def faculty_view(request):
	db=db_connect()
	data_temp=json.loads(request.body.decode('utf-8'))

	faculty_id=data_temp['faculty_id']
	query1=TimetableFinalTimeslotDay.select().join(TimetableFinalFacultySubject).where((TimetableFinalTimeslotDay.faculty_subject_table_id==TimetableFinalFacultySubject.id)&(TimetableFinalFacultySubject.faculty_id==faculty_id)).order_by(TimetableFinalTimeslotDay.day_id,TimetableFinalTimeslotDay.timeslot_table_id,TimetableFinalTimeslotDay.batch_name)
	data_list=[]
	final_day_list=[]
	lastID={}
	lastID['id']=-1
	for slot in query1:
		if data_list and slot.day_id.id!=lastID.id:
			final_day_list.append({'day':lastID.day_name,'data':data_list})
			data_list=[]
		subject_name=slot.faculty_subject_table_id.sub_code.sub_name
		temp_resource_type=slot.resource_type
		temp_timeslot=slot.timeslot_table_id.timeslot_name
		times=temp_timeslot.split("-")
		start=times[0]
		end=times[1]
		flag=0
		i=-1
		if temp_resource_type==1:
			room=TimetableFinalLab.get(TimetableFinalLab.lab==slot.resource).lab_name
			resource_type="lab"
			batch_name=slot.batch_name
		else:
			room=TimetableFinalClassroom.get(TimetableFinalClassroom.classroom==slot.resource).classroom_name
			resource_type="lecture"
			batch_name=""
		for index,x in enumerate(data_list):
			if x['end']==end and x['start']==start:
				flag=1
				i=index
		d = {'subject':subject_name,'type':resource_type,'batch':batch_name,'room':room,'start':start,'end':end,'sem':slot.semester_table_id.semester_name}
		if flag==0:
			data_list.append(d)
		if flag==1 and i!=-1:
			data_list[index]['extra'] = d
		lastID=slot.day_id
	final_day_list.append({'day':lastID.day_name,'data':data_list})
	db_close(db)
	return HttpResponse(json.dumps(final_day_list), content_type="application/json")


@csrf_exempt
def faculty_preference(request):
	db=MySQLDatabase('time_table_test8',user='root',password='',host='localhost')
	db.connect()

	data=request.body.decode('utf-8')
	data_temp=json.loads(data)

	faculty_name=data_temp['faculty']
	subject_list=data_temp['subjects']
	discipline=data_temp['discipline']
	course=data_temp['course']
	shift=data_temp['shift']
	temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()
	temp_discipline=TimetableFinalDescipline.select().where(TimetableFinalDescipline.descipline_name==discipline).get()
	temp_course_discipline=TimetableFinalDesciplineCourse.select().where((TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline.id)&(TimetableFinalDesciplineCourse.course==temp_course.course)).get()

	count1=TimetableFinalFacultyPref1.select().where(TimetableFinalFacultyPref1.descipline_course_table_id==temp_course_discipline.id).count()
	if count1>0:
		for fac in TimetableFinalFacultyPref1.select():
			fac.delete_instance()

	temp_shift=TimetableFinalShift.get(TimetableFinalShift.shift_name==str(shift))

	temp_faculty=TimetableFinalFaculty.select().where(TimetableFinalFaculty.faculty_name==faculty_name).get()
	for sub in subject_list:
		temp_sub=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==sub).get()
		fp1=TimetableFinalFacultyPref1.create(descipline_course_table_id=temp_course_discipline.id,faculty_id=temp_faculty.faculty,shift_table_id=temp_shift.id,sub_code=temp_sub.sub_code)
	db.close()
	return HttpResponse(json.dumps({"status":"Success"}), content_type="application/json")


@csrf_exempt
def discipline_list(request):
	course="B.E."
	db=db_connect()
	temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()
	discipline_list=[]
	for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course):
		discipline_list.append(disc.descipline_table_id.descipline_name)
	db_close(db)
	return HttpResponse(json.dumps({"data":discipline_list}), content_type="application/json")



@csrf_exempt
def timetable_gen2(request):
	db=db_connect()

	data=request.body.decode('utf-8')
	print(data)
	data_temp=json.loads(data)
	type1=data_temp['type']
	term=data_temp['term']
	course="B.E."
	discipline="Computer Engineering"
	shift="Morning"
	temp_lab_list=[0,1,3,5]
	temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()
	temp_discipline=TimetableFinalDescipline.select().where(TimetableFinalDescipline.descipline_name==discipline).get()
	temp_shift=TimetableFinalShift.get(TimetableFinalShift.shift_name==str(shift))
	temp_course_discipline=TimetableFinalDesciplineCourse.select().where((TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline.id)&(TimetableFinalDesciplineCourse.course==temp_course.course)).get()
	temp_sem=TimetableFinalSemester.select().where((TimetableFinalSemester.term==term)&(TimetableFinalSemester.descipline_course_table_id==temp_course_discipline.id)&(TimetableFinalSemester.shift_table_id==temp_shift.id)&(TimetableFinalSemester.term==str(term)))
	temp_course_discipline1=temp_course_discipline.id
	if type1==1:
		for t in temp_sem:
			TimetableFinalTimeslotDay.delete().where((TimetableFinalTimeslotDay.descipline_course_table_id==temp_course_discipline1)&(TimetableFinalTimeslotDay.semester_table_id==t.id)).execute()

		query1=TimetableFinalTempLab.delete().where(TimetableFinalTempLab.descipline_course_table_id==temp_course_discipline1)
		query1.execute()
		print("Hello")

		timeslot_list=[]
		for t in TimetableFinalTimeslot.select():
			timeslot_list.append(str(t.timeslot_name))

		day_list=[]
		for d in TimetableFinalDay.select():
			day_list.append(str(d.day_name))



		shift_list=[]
		for shift1 in TimetableFinalShift.select():
			shift_list.append(str(shift1.shift_name))
		shift_list=[]
		shift_list.append("Morning")
		count=TimetableFinalTimeslotDay.select().where((TimetableFinalTimeslotDay.descipline_course_table_id==temp_course_discipline1)).count()

		semester_list=[]

		for sem in temp_sem:
			semester_list.append(str(sem.semester_name))

		sem_sub={}
		for cou in TimetableFinalCourse.select():
			disc_dict={}
			for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
				sem_dict={}
				for sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==disc.id):
					sub_list=[]
					for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
						sub_list.append(sub.sub_code.sub_name)
						sem_dict[str(sem.semester_name)]=sub_list
				disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
			sem_sub[str(cou.course_name)]=disc_dict
		sub_fac_detail={}
		for temp_course in TimetableFinalCourse.select():
			temp_discipline_dict={}
			for temp_discipline in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course):
				temp_sem_dict={}
				for temp_sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==temp_discipline.id):
					temp_shift_dict={}
					for shift in shift_list:
						temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
						temp_sub_dict={}
						for temp_sub_discipline in TimetableFinalSubjectDiscipline.select().where(TimetableFinalSubjectDiscipline.semester_table_id==temp_sem.id):
							for temp_sub in TimetableFinalSubject.select().where(TimetableFinalSubject.sub_code==temp_sub_discipline.sub_code):
								temp_fac_list=[]
								for temp_fac in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.sub_code==temp_sub.sub_code):
									if temp_fac.shift_table_id.id==temp_shift.id:
										temp_fac_list.append((temp_fac.faculty.faculty,temp_fac.faculty.position,temp_fac.faculty.faculty_name,temp_fac.faculty.work_load))
								temp_fac_list.sort(key=lambda tup:tup[1],reverse=True)
								temp_i=0
								temp_fac_dict={}
								for temp_fac_2 in temp_fac_list:
									temp_fac_dict[temp_i]={
														'id':temp_fac_2[0],
														'name':temp_fac_2[2],
														'position':temp_fac_2[1],
														'work_load':temp_fac_2[3]
														}
									temp_i+=1
								sub_scheme_detail=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==temp_sub).get()
								no_batch=TimetableFinalSubjectNoStudent.get(TimetableFinalSubjectNoStudent.sub_code==temp_sub.sub_code).no_batch
								temp_sub_dict[str(temp_sub.sub_name)]={
																		'sub_code':temp_sub.sub_code,
																	'sub_name':temp_sub.sub_name,
																	'is_elective':temp_sub.is_elective,
																	'faculty':temp_fac_dict,
																	'sub_load':sub_scheme_detail.sub_load,
																	'sub_practical_class':(sub_scheme_detail.sub_practical_class)*(no_batch),
																	# 'sub_practical_class':(sub_scheme_detail.sub_practical_class)*(no_batch),
																	'sub_theory_class':sub_scheme_detail.sub_theory_class,
																	'sub_tutorial_class':sub_scheme_detail.sub_tutorial_class
																	}
						temp_shift_dict[str(shift)]=temp_sub_dict
					temp_sem_dict[str(temp_sem.semester_name)]=temp_shift_dict
				temp_discipline_dict[str(temp_discipline.descipline_table_id.descipline_name)]=temp_sem_dict
			sub_fac_detail[str(temp_course.course_name)]=temp_discipline_dict
		sem_sub={}
		for cou in TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course):
			disc_dict={}
			for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
				sem_dict={}
				for sem in TimetableFinalSemester.select().where((TimetableFinalSemester.descipline_course_table_id==disc.id)&(TimetableFinalSemester.term==str(term))):
					sub_list=[]
					for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
						temp_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==sub.sub_code).get()
						practical=temp_scheme.sub_practical_class
						if practical>0:
							sub_list.append(str(sub.sub_code.sub_name))
					sem_dict[str(sem.semester_name)]=sub_list
				disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
			sem_sub[str(cou.course_name)]=disc_dict


		sem_batch={}
		for sem in semester_list:
			batch_list=[]
			subject_list1=sem_sub[str(course)][str(discipline)][str(sem)]
			for sub in subject_list1:
				sub_code1=TimetableFinalSubject.get(TimetableFinalSubject.sub_name==sub).sub_code
				for batch in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==sub_code1):
					if str(batch.batch_name) not in batch_list:
						batch_list.append(str(batch.batch_name))
			sem_batch[str(sem)]=batch_list
		sem_timeslot={}
		for sem in semester_list:
			subject_list=sem_sub[str(course)][str(discipline)][str(sem)]
			length_of_subject_list=len(subject_list)
			temp1=(length_of_subject_list*2)+2
			timeslot_list1=[]
			if temp1>len(timeslot_list):
				timeslot_list1=timeslot_list
			else:
				for i in range(0,temp1+1):
					timeslot_list1.append(timeslot_list[i])
			sem_timeslot[str(sem)]=timeslot_list1

		sem_lab={}
		for sem in semester_list:

			lab_list=[]

			temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
			total_batch=TimetableFinalSemesterBatch.get(TimetableFinalSemesterBatch.semester_table_id==temp_sem.id).no_batches
			for l in TimetableFinalSemesterLab.select().where(TimetableFinalSemesterLab.semester_table_id==temp_sem.id):
				lab_list.append(l.lab.lab)

		lab_available={}
		for l in TimetableFinalLabAvailable.select():
			shift_ava={}
			for shift in shift_list:
				day_ava={}
				temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
				for d in day_list:
					temp_day=TimetableFinalDay.select().where(TimetableFinalDay.day_name==str(d)).get()
					timeslot_ava={}
					for t in timeslot_list:
						temp_timeslot=TimetableFinalTimeslot.select().where((TimetableFinalTimeslot.timeslot_name==str(t))&(TimetableFinalTimeslot.shift_table_id==temp_shift.id)).get()
						timeslot_ava[str(temp_timeslot.timeslot_name)]=1
					day_ava[str(temp_day.day_name)]=timeslot_ava
				shift_ava[str(shift)]=day_ava
			lab_available[str(l.lab.lab)]=shift_ava
		temp_data={}
		data_len=TimetableFinalTempLab.select().where(TimetableFinalTempLab.descipline_course_table_id!=temp_course_discipline1).count()
		if data_len>0:
			for data in TimetableFinalTempLab.select():
				course_name=data.descipline_course_table_id.course.course_name
				discipline_name=data.descipline_course_table_id.descipline_table_id.descipline_name
				semester_name=data.semester_table_id.semester_name
				shift_name=data.shift_table_id.shift_name
				day_name=data.day_id.day_name
				timeslot_name=data.timeslot_table_id.timeslot_name
				faculty_subject_table_id=data.faculty_subject_table_id
				faculty_temp6=TimetableFinalFacultySubject.get(TimetableFinalFacultySubject.id==faculty_subject_table_id)
				faculty_name=faculty_temp6.faculty.faculty_name
				subject_name=faculty_temp6.sub_code.sub_name
				timeslot_temp_data={}
				timeslot_temp_data[str(timeslot_name)]={'faculty':faculty_name,'subject':subject_name}
				temp_data[str(day_name)]=timeslot_temp_data
		course_dict={}
		discipline_dict={}
		sem_dict={}
		for sem in semester_list:
			temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
			timeslot_list=sem_timeslot[str(sem)]
			subject_list=sem_sub[str(course)][str(discipline)][str(sem)]
			total_batch=TimetableFinalSemesterBatch.get(TimetableFinalSemesterBatch.semester_table_id==temp_sem.id).no_batches
			shift_dict={}
			for shift in shift_list:

				temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
				days_dict={}

				subject_batch_counter={}
				for sub in subject_list:
					temp_sub=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==sub).get()
					batch_dict={}
					for batch in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==temp_sub.sub_code):
						batch_dict[str(batch.batch_name)]=0
					subject_batch_counter[str(temp_sub.sub_name)]=batch_dict
				for d in day_list:
					subject_list1=sem_sub[str(course)][str(discipline)][str(sem)]
					if len(subject_list1)>0:

						new_temp_dict={}

						subject_counter={}
						for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
							info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
							for k1 in info3.keys():
								subject_counter[str(info3['sub_name'])]=0
						sub_batch={}
						for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
							info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
							for k1 in info3.keys():
								temp_sub_name=info3['sub_name']
								temp_sub_code=info3['sub_code']
								batch_list=[]
								for b in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==temp_sub_code):
									batch_list.append(str(b.batch_name))
								sub_batch[str(temp_sub_name)]=batch_list

						faculty_counter={}
						for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
							info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
							for k1 in info3.keys():
								faculties=info3['faculty']
								for k2 in faculties.keys():
									fac1=faculties[k2]
									faculty_counter[str(fac1['name'])]=0

						done_dict={}
						temp_done_batch_list=[]
						for sub in subject_list:
							done_dict[str(sub)]=temp_done_batch_list

						done_batch_list=[]

						timeslot_dict={}
						flag1=0
						for i in range(0,len(timeslot_list)):
							t=randint(0,6)
							timeslot=timeslot_list[t]
							if t not in temp_lab_list:
								while t not in temp_lab_list:
									t=randint(0,6)
							timeslot=timeslot_list[t]
							flag=0
							for lab in TimetableFinalSemesterLab.select().where(TimetableFinalSemesterLab.semester_table_id==temp_sem.id):
								if lab_available[str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]==1:
									for x in range(total_batch):
										if len(course_dict)>0:
											pass
										elif len(sem_dict)>0:

											if len(subject_list1)>0:
												flag=0
												while flag==0:
													sub=random.choice(subject_list1)

													subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]
													prac=subject_detail['sub_practical_class']
													batch_list1=sub_batch[str(sub)]
													temp_sub_code1=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==str(sub)).get()
													temp_sub_scheme1=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==temp_sub_code1.sub_code).get()
													for b1 in batch_list1:
														if str(b1) not in done_batch_list and subject_batch_counter[str(sub)][str(b1)]<temp_sub_scheme1.sub_practical_class:
															b=b1
															flag=1
															break
											faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['faculty']

											faculty_flag=0
											for k in faculties:
												inner_flag=0
												fac1=faculties[k]
												faculty_old=""
												if len(temp_data)>0:
													if str(d) in temp_data:
														new_temp_data=temp_data[str(d)]
														if timeslot in new_temp_data:
															faculty_old=new_temp_data[timeslot]['faculty']
															print(faculty_old,"Hi")
												print("Hello here we are before checking")
												for k1 in sem_dict.keys():
													temp_shift_dict=sem_dict[str(k1)]
													for k2 in temp_shift_dict.keys():
														temp_days_dict=temp_shift_dict[str(k2)]
														if d in temp_days_dict:
															# print(d)
															temp_timeslot_dict=temp_days_dict[str(d)]
															# print(temp_timeslot_dict)
															print("value of t is",t)
															if timeslot in temp_timeslot_dict:
																print(t)
																temp_info=temp_timeslot_dict[str(timeslot)]
																info=temp_info['value']
																for key2 in info.keys():
																	batch_dict=info[str(key2)]
																	if batch_dict['faculty']==str(fac1['name']):
																		print(batch_dict['faculty'])
																		inner_flag=1

												print("Hello here we are after checking")
												if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=4 or inner_flag==1:
													continue
												else:

													for k1 in sem_dict.keys():
														temp_shift_dict=sem_dict[str(k1)]
														for k2 in temp_shift_dict.keys():
															temp_days_dict=temp_shift_dict[str(k2)]
															if d in temp_days_dict:
																temp_timeslot_dict=temp_days_dict[str(d)]
																if timeslot in temp_timeslot_dict:
																	print(t)
																	temp_info=temp_timeslot_dict[str(timeslot)]
																	info=temp_info['value']
																	for key2 in info.keys():
																		batch_dict=info[str(key2)]
																		if batch_dict['faculty']==str(fac1['name']):
																			print(batch_dict['faculty'])
																			inner_flag=1
													if inner_flag==1:
														continue
													else:
														new_temp_dict[str(b)]={'faculty':str(fac1['name']),'subject':str(sub),'batch':str(b),'lab':str(lab.lab.lab_name)}
														v=t
														for t1 in range(0,2):
															timeslot=timeslot_list[v]
															timeslot_dict[str(timeslot)]={'lab':1,'classroom':0,'value':new_temp_dict}
															if str(fac1['name']) in faculty_counter:
																faculty_counter[str(fac1['name'])]+=1
															else:
																faculty_counter[str(fac1['name'])]=1
															fac1['work_load']-=1
															if str(sub) in subject_counter:
																subject_counter[str(sub)]+=1
															else:
																subject_counter[str(sub)]=1
															sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_practical_class']-=1
															subject_batch_counter[str(sub)][str(b)]+=1
															v+=1
															lab_available[str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]=0

														done_batch_list.append(b)
														if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_practical_class']==0:
															subject_list1.remove(sub)
														flag=1
														break
										else:
											if len(subject_list1)>0:
												flag=0
												while flag==0:
													sub=random.choice(subject_list1)
													subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]
													prac=subject_detail['sub_practical_class']
													batch_list1=sub_batch[str(sub)]
													temp_sub_code1=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==str(sub)).get()
													temp_sub_scheme1=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==temp_sub_code1.sub_code).get()
													for b1 in batch_list1:
														if str(b1) not in done_batch_list and subject_batch_counter[str(sub)][str(b1)]<temp_sub_scheme1.sub_practical_class:
															b=b1
															flag=1
															break
											faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['faculty']
											faculty_flag=0
											for k in faculties:
												inner_flag=0
												fac1=faculties[k]
												faculty_old=""
												if len(temp_data)>0:
													if str(d) in temp_data:
														new_temp_data=temp_data[str(d)]
														if timeslot in new_temp_dict:
															faculty_old=new_temp_dict[timeslot]['faculty']
															if faculty_old==str(fac1['name']):
																inner_flag=1
												if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=4 or str(fac1['name'])==faculty_old:
													continue
												else:
													new_temp_dict[str(b)]={'faculty':str(fac1['name']),'subject':str(sub),'batch':str(b),'lab':str(lab.lab.lab_name)}
													v=t
													for t1 in range(0,2):
														timeslot=timeslot_list[v]
														timeslot_dict[str(timeslot)]={'lab':1,'classroom':0,'value':new_temp_dict}
														if str(fac1['name']) in faculty_counter:
															faculty_counter[str(fac1['name'])]+=1
														else:
															faculty_counter[str(fac1['name'])]=1
														fac1['work_load']-=1
														if str(sub) in subject_counter:
															subject_counter[str(sub)]+=1
														else:
															subject_counter[str(sub)]=1
														sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_practical_class']-=1
														subject_batch_counter[str(sub)][str(b)]+=1
														v+=1
														lab_available[str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]=0

													done_batch_list.append(str(b))
													if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_practical_class']==0:
														subject_list1.remove(sub)
													flag=1
													break

									if flag==1:
										flag1=1
										break
							if flag1==1:
								break
							# if flag1==1:
							# 	break
						days_dict[str(d)]=timeslot_dict
						# print(days_dict)
				# return HttpResponse(json.dumps(days_dict), content_type="application/json")
				shift_dict[str(shift)]=days_dict
				# print(shift_dict)
			sem_dict[str(sem)]=shift_dict
			# print("helomcsdnnc")
			# print(sem_dict)
		discipline_dict[str(discipline)]=sem_dict
		# print(discipline_dict)
		# print("Hello World")
		# print("helomcsdnnc5565")
		course_dict[str(course)]=discipline_dict



		# print("Hello5")


		# print("OK")
		# temp_course_dict=course_dict[str(course)][str(discipline)]
		sem_dict5={}
		for sem in semester_list:
			temp_sem_dict={}
			for shift in shift_list:
				temp_day_dict={}
				for d in day_list:
					temp_timeslot_dict={}
					for t in timeslot_list:
						if d in course_dict[str(course)][str(discipline)][str(sem)][str(shift)]:
							if t in course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(d)]:
								temp_timeslot_dict[str(t)]=course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(d)][str(t)]
							else:
								temp_timeslot_dict[str(t)]={}
						else:
							temp_timeslot_dict[str(t)]={}
					temp_day_dict[str(d)]=temp_timeslot_dict
				temp_sem_dict[str(shift)]=temp_day_dict
			sem_dict5[str(sem)]=temp_sem_dict

		class_course_dict=classroom1.classroom1(course,discipline,shift,term,day_list,timeslot_list,shift_list,semester_list,sub_fac_detail,course_dict)
		# print("Yo")
		final_course_dict={}
		final_discipline_dict={}
		temp1_sem_dict=class_course_dict[str(course)][str(discipline)]
		sem_dict1={}
		for sem in temp1_sem_dict.keys():
			temp1_shift_dict=temp1_sem_dict[str(sem)]
			shift_dict1={}
			for shift in temp1_shift_dict.keys():
				temp1_days_dict=temp1_shift_dict[str(shift)]
				days_dict1={}
				for days in temp1_days_dict.keys():
					# print(days)
					temp1_timeslot_dict=temp1_days_dict[days]
					timeslot_dict1={}
					for t in temp1_timeslot_dict.keys():
						temp_info=temp1_timeslot_dict[str(t)]
						timeslot_dict1[str(t)]=temp_info
					if days in course_dict[str(course)][str(discipline)][str(sem)][str(shift)]:
						temp2_timeslot_dict=course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(days)]
						for t1 in temp2_timeslot_dict.keys():
							temp_info1=temp2_timeslot_dict[str(t1)]
							timeslot_dict1[str(t1)]=temp_info1

					days_dict1[str(days)]=timeslot_dict1
				shift_dict1[str(shift)]=days_dict1
			sem_dict1[str(sem)]=shift_dict1
		final_discipline_dict[str(discipline)]=sem_dict1
		final_course_dict[str(course)]=final_discipline_dict

		data_list=[]
		for sem in semester_list:
			sem_id=TimetableFinalSemester.get(TimetableFinalSemester.semester_name==sem).id
			classroom=TimetableFinalSemesterClassroom.get(TimetableFinalSemesterClassroom.semester_table_id==sem_id).classroom.classroom_name
			for shift in shift_list:
				days_list1=[]
				for d in day_list:
					slot_list=[]
					for t in timeslot_list:

						if d in final_course_dict[str(course)][str(discipline)][str(sem)][str(shift)]:

							if t in final_course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(d)]:
								if final_course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(d)][str(t)]['lab']==1:
									b=final_course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(d)][str(t)]['value']
									value_list1=[]
									for key1 in b.keys():
										# print(key1)
										temp_info_data=b[key1]
										subject=temp_info_data["subject"]
										batch=temp_info_data["batch"]
										room=temp_info_data["lab"]
										faculty=temp_info_data["faculty"]
										value_list1.append({"subject":subject,"batch":batch,"room":room,"faculty":faculty})
									slot_list.append({"type":"lab","values":value_list1})
								else:
									b=final_course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(d)][str(t)]['value']
									value_list1=[]
									for key1 in b.keys():
										temp_info_data=b[key1]
										subject=temp_info_data["subject"]
										# batch=temp_info_data["batch"]
										room=temp_info_data["classroom"]
										faculty=temp_info_data["faculty"]
										value_list1.append({"subject":subject,"batch":"","room":room,"faculty":faculty})
									slot_list.append({"type":"classroom","values":value_list1})
							# else:
							# 	slot_list.append({"values":[]})
					days_list1.append({"name":d,"slots":slot_list})
				data_list.append({"name":sem,"shift":shift,"days":days_list1,"classroom":classroom})

		# print(final_course_dict)
		# print("Hello")
		temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()
		temp_discipline=TimetableFinalDescipline.select().where(TimetableFinalDescipline.descipline_name==discipline).get()
		temp_course_discipline=TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course).get()
		temp_data=final_course_dict[str(course)][str(discipline)]
		# print(temp_data)
		for k1 in temp_data.keys():
			# TimetableFinalTimeslotDay
			#k1=sem
			temp_sem=TimetableFinalSemester.get(TimetableFinalSemester.semester_name==k1).id
			temp1_sem_dict=temp_data[k1]
			for k2 in temp1_sem_dict.keys():
				#k2=Morning
				temp_shift=TimetableFinalShift.get(TimetableFinalShift.shift_name==k2).id
				temp1_shift_dict=temp1_sem_dict[k2]
				for k3 in temp1_shift_dict.keys():
					#k3=Day
					temp_day=TimetableFinalDay.get(TimetableFinalDay.day_name==k3).id
					temp1_days_dict=temp1_shift_dict[k3]
					for k4 in temp1_days_dict.keys():
						temp_timeslot=TimetableFinalTimeslot.get(TimetableFinalTimeslot.timeslot_name==k4).id
						#k4=timeslot
						temp1_timeslot_dict=temp1_days_dict[k4]
						temp_course=TimetableFinalCourse.get(TimetableFinalCourse.course_name==course).course
						temp_discipline=TimetableFinalDescipline.get(TimetableFinalDescipline.descipline_name==discipline).id
						course_discipline_id=TimetableFinalDesciplineCourse.get((TimetableFinalDesciplineCourse.course==temp_course)&(TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline)).id
						if temp1_timeslot_dict['classroom']==1:
							info=temp1_timeslot_dict['value']
							for key1 in info.keys():
								temp_info=info[key1]
								classroom_name=temp_info['classroom']
								subject_name=temp_info['subject']
								# type_name=temp_info['type']
								faculty_name=temp_info['faculty']
								batch_name=""
								day_name=k3

								temp_faculty=TimetableFinalFaculty.get(TimetableFinalFaculty.faculty_name==faculty_name).faculty
								temp_sub=TimetableFinalSubject.get(TimetableFinalSubject.sub_name==subject_name).sub_code
								fac_sub_id=TimetableFinalFacultySubject.get((TimetableFinalFacultySubject.faculty==temp_faculty)&(TimetableFinalFacultySubject.sub_code==temp_sub)).id
								resource_id=TimetableFinalClassroom.get(TimetableFinalClassroom.classroom==classroom_name).classroom
								resource_type=0
								# print(batch_name,temp_day,course_discipline_id,fac_sub_id,resource_id,resource_type,temp_sem,temp_shift,temp_timeslot)
								TimetableFinalTimeslotDay.create(batch_name=batch_name,day_id=temp_day,descipline_course_table_id=course_discipline_id,faculty_subject_table_id=fac_sub_id,resource=resource_id,resource_type=0,semester_table_id=temp_sem,shift_table_id=temp_shift,timeslot_table_id=temp_timeslot)
						else:
							info=temp1_timeslot_dict['value']
							for key1 in info.keys():
								#key1=batch_name
								batch_name=key1
								temp_info=info[key1]
								subject_name=temp_info['subject']
								batch=temp_info['batch']
								lab1=temp_info['lab']
								faculty_name=temp_info['faculty']
								# type_name=temp_info['type']
								temp_faculty=TimetableFinalFaculty.get(TimetableFinalFaculty.faculty_name==faculty_name).faculty
								temp_sub=TimetableFinalSubject.get(TimetableFinalSubject.sub_name==subject_name).sub_code
								fac_sub_id=TimetableFinalFacultySubject.get((TimetableFinalFacultySubject.faculty==temp_faculty)&(TimetableFinalFacultySubject.sub_code==temp_sub)).id
								resource_id=TimetableFinalLab.get(TimetableFinalLab.lab_name==lab1).lab
								resource_type=1
								# print(batch_name,temp_day,course_discipline_id,fac_sub_id,resource_id,resource_type,temp_sem,temp_shift,temp_timeslot)
								TimetableFinalTimeslotDay.create(batch_name=batch_name,day_id=temp_day,descipline_course_table_id=course_discipline_id,faculty_subject_table_id=fac_sub_id,resource=resource_id,resource_type=1,semester_table_id=temp_sem,shift_table_id=temp_shift,timeslot_table_id=temp_timeslot)
								TimetableFinalLabTable.create(batch_name=batch_name,day_id=temp_day,descipline_course_table_id=course_discipline_id,lab=resource_id,semester_table_id=temp_sem,shift_table_id=temp_shift,timeslot_table_id=temp_timeslot)

		temp_shift1=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==shift).get()
		x=TimetableFinalTimeslotDay.select().join(TimetableFinalSemester).where((TimetableFinalTimeslotDay.descipline_course_table_id==temp_course_discipline1)&(TimetableFinalTimeslotDay.shift_table_id==temp_shift1.id)&(TimetableFinalSemester.descipline_course_table_id==temp_course_discipline1)&(TimetableFinalSemester.term==term)&(TimetableFinalTimeslotDay.semester_table_id==TimetableFinalSemester.id)).order_by(TimetableFinalTimeslotDay.semester_table_id,TimetableFinalTimeslotDay.day_id,TimetableFinalTimeslotDay.timeslot_table_id,TimetableFinalTimeslotDay.batch_name)
		
		final_sem_list=[]
		if x:
			days_list=[]
			slots_list=[]
			values_list=[]
			last=x[0]
			for sem in x:
				if sem.semester_table_id!=last.semester_table_id:
					slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
					days_list.append({'name':last.day_id.day_name,'slots':slots_list})
					resource=TimetableFinalSemesterClassroom.get(TimetableFinalSemesterClassroom.semester_table_id==last.semester_table_id).classroom.classroom_name
					final_sem_list.append({'classroom':resource,'name':last.semester_table_id.semester_name,'days':days_list})
					days_list=[]
					slots_list=[]
					values_list=[]
				elif sem.day_id!=last.day_id:
					slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
					days_list.append({'name':last.day_id.day_name,'slots':slots_list})
					slots_list=[]
					values_list=[]
				elif sem.timeslot_table_id!=last.timeslot_table_id:
					slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
					values_list=[]
				if sem.resource_type==0:
					resource=TimetableFinalClassroom.select().where(TimetableFinalClassroom.classroom==sem.resource).get().classroom_name
				else:
					resource=TimetableFinalLab.get(TimetableFinalLab.lab==sem.resource).lab_name
				values_list.append({'faculty':sem.faculty_subject_table_id.faculty.faculty_name,'subject':sem.faculty_subject_table_id.sub_code.sub_name,'room':resource,'batch':sem.batch_name})
				last=sem
			slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
			days_list.append({'name':last.day_id.day_name,'slots':slots_list})
			resource=TimetableFinalSemesterClassroom.get(TimetableFinalSemesterClassroom.semester_table_id==last.semester_table_id).classroom.classroom_name
			final_sem_list.append({'classroom':resource,'name':last.semester_table_id.semester_name,'days':days_list})
		db_close(db)
		return HttpResponse(json.dumps(final_sem_list), content_type="application/json")
	elif type1==0:
		temp_shift1=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==shift).get()
		x=TimetableFinalTimeslotDay.select().join(TimetableFinalSemester).where((TimetableFinalTimeslotDay.descipline_course_table_id==temp_course_discipline1)&(TimetableFinalTimeslotDay.shift_table_id==temp_shift1.id)&(TimetableFinalSemester.descipline_course_table_id==temp_course_discipline1)&(TimetableFinalSemester.term==term)&(TimetableFinalTimeslotDay.semester_table_id==TimetableFinalSemester.id)).order_by(TimetableFinalTimeslotDay.semester_table_id,TimetableFinalTimeslotDay.day_id,TimetableFinalTimeslotDay.timeslot_table_id,TimetableFinalTimeslotDay.batch_name)
		
		final_sem_list=[]
		if x:
			days_list=[]
			slots_list=[]
			values_list=[]
			last=x[0]
			for sem in x:
				if sem.semester_table_id!=last.semester_table_id:
					slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
					days_list.append({'name':last.day_id.day_name,'slots':slots_list})
					resource=TimetableFinalSemesterClassroom.get(TimetableFinalSemesterClassroom.semester_table_id==last.semester_table_id).classroom.classroom_name
					final_sem_list.append({'classroom':resource,'name':last.semester_table_id.semester_name,'days':days_list})
					days_list=[]
					slots_list=[]
					values_list=[]
				elif sem.day_id!=last.day_id:
					slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
					days_list.append({'name':last.day_id.day_name,'slots':slots_list})
					slots_list=[]
					values_list=[]
				elif sem.timeslot_table_id!=last.timeslot_table_id:
					slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
					values_list=[]
				if sem.resource_type==0:
					resource=TimetableFinalClassroom.select().where(TimetableFinalClassroom.classroom==sem.resource).get().classroom_name
				else:
					resource=TimetableFinalLab.get(TimetableFinalLab.lab==sem.resource).lab_name
				values_list.append({'faculty':sem.faculty_subject_table_id.faculty.faculty_name,'subject':sem.faculty_subject_table_id.sub_code.sub_name,'room':resource,'batch':sem.batch_name})
				last=sem
			slots_list.append({'type':'lab' if last.resource_type==1 else 'classroom','values':values_list})
			days_list.append({'name':last.day_id.day_name,'slots':slots_list})
			resource=TimetableFinalSemesterClassroom.get(TimetableFinalSemesterClassroom.semester_table_id==last.semester_table_id).classroom.classroom_name
			final_sem_list.append({'classroom':resource,'name':last.semester_table_id.semester_name,'days':days_list})
		db_close(db)
		return HttpResponse(json.dumps(final_sem_list), content_type="application/json")

@csrf_exempt
def subjects(request):
	db=db_connect()
	data=request.body.decode('utf-8')
	data_temp=json.loads(data)
	course="B.E."
	discipline=str(data_temp['discipline'])
	print(discipline,"sndabsdb")
	discipline_data=TimetableFinalDescipline.get(TimetableFinalDescipline.descipline_name==discipline).id
	discipline_course=TimetableFinalDesciplineCourse.get(TimetableFinalDesciplineCourse.descipline_table_id==discipline_data).id
	sub_list=[]
	for sub in TimetableFinalSubjectDiscipline.select().distinct().where((TimetableFinalSubjectDiscipline.descipline_course_table_id==discipline_course)):
		sub_list.append({"sub_code":sub.sub_code.sub_code,"sub_name":sub.sub_code.sub_name})
	return HttpResponse(json.dumps(sub_list), content_type="application/json")


@csrf_exempt
def fetch(request):
	discipline = "Computer Engineering"
	term = "odd"
	disc_temp={}
	str1=""
	print(dict_main)
	if discipline in dict_main:
		disc_temp==dict_main[discipline]
	if term in disc_temp:
		str1==disc_temp[term]
	return HttpResponse(str1, content_type="application/json")


@csrf_exempt
def delete_subject(request):
	db=db_connect()
	data=request.body.decode('utf-8')
	print(data)
	data_temp=json.loads(data)
	print(data_temp)
	sub_code=data_temp['subcode']
	print(str(sub_code)+"--------------------------->")
	t=TimetableFinalSubjectLab.get(TimetableFinalSubjectLab.sub_code==sub_code)
	t1=t.delete_instance()
	count1=TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==sub_code).count()
	if count1>0:
		sub=TimetableFinalSubjectBatch.get(TimetableFinalSubjectBatch.sub_code==sub_code)
		e=sub.delete_instance()
	count=TimetableFinalSubjectNoStudent.select().where(TimetableFinalSubjectNoStudent.sub_code==sub_code).count()
	if count>0:
		sub=TimetableFinalSubjectNoStudent.get(TimetableFinalSubjectNoStudent.sub_code==sub_code)
		a=sub.delete_instance()
	sub=TimetableFinalSubjectScheme.get(TimetableFinalSubjectScheme.sub_code==sub_code)
	b=sub.delete_instance()
	sub=TimetableFinalSubjectDiscipline.get(TimetableFinalSubjectDiscipline.sub_code==sub_code)
	c=sub.delete_instance()
	sub=TimetableFinalSubject.get(TimetableFinalSubject.sub_code==sub_code)
	d=sub.delete_instance()
	if a>0:
		db_close(db)
		return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
	else:
		return HttpResponse(json.dumps({"status":"UnSuccess"}),content_type="application/json")


class Subject(View):
	def get(self,request):
		db=db_connect()
		course="B.E."
		shift="Morning"
		temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()
		temp_discipline=TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course).get()
		discipline=temp_discipline.descipline_table_id.descipline_name
		temp_discipline=TimetableFinalDescipline.select().where(TimetableFinalDescipline.descipline_name==discipline).get()
		temp_cousre=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()
		temp_discipline_course=TimetableFinalDesciplineCourse.select().where((TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline.id)&(TimetableFinalDesciplineCourse.course==temp_cousre.course)).get()
		semester_list=[]
		for sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==temp_discipline_course.id):
			subjects=[]
			for sub in TimetableFinalSubjectDiscipline.select().distinct().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==temp_discipline_course.id)):
				sub_name=sub.sub_code.sub_name
				sub_code=sub.sub_code.sub_code
				elective=sub.sub_code.is_elective
				temp_shift3=sub.shift_table_id.shift_name
				sub_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==sub_code).get()
				lectures=sub_scheme.sub_theory_class
				tutorials=sub_scheme.sub_tutorial_class
				labs=sub_scheme.sub_practical_class
				schema={'lectures':lectures,'labs':labs,'tutorials':tutorials}
				batches=[]
				for batch in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==sub_code):
					batches.append({'name':batch.batch_name})
				faculties=[]
				for fac in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.sub_code==sub_code):
					faculties.append({'name':fac.faculty.faculty_name})
				subjects.append({'shift':temp_shift3,'course':course,'discipline':discipline,'name':sub_name,'subcode':sub_code,'schema':schema,'batches':batches,'faculties':faculties,'elective':elective,'no_batch':len(batches)})
			semester_list.append({'name':str(sem.semester_name),'subjects':subjects})
		final_dict={'name':discipline,'semesters':semester_list}
		db_close(db)
		return HttpResponse(json.dumps(final_dict), content_type="application/json")
	
	def post(self,request):
		data=request.body.decode('utf-8')
		data_temp=json.loads(data)
		subject=data_temp['name']
		subject_code=data_temp['subcode']
		elective=data_temp['elective']
		batch_list=data_temp['batches']
		shift=data_temp['shift']
		lab_list=[]
		shift1 = []
		shift1.append(shift)
		course=data_temp['course']
		discipline=data_temp['discipline']
		temp_course=TimetableFinalCourse.get(TimetableFinalCourse.course_name==course).course
		temp_discipline1=TimetableFinalDescipline.get(TimetableFinalDescipline.descipline_name==discipline).id
		temp_discipline=TimetableFinalDesciplineCourse.get((TimetableFinalDesciplineCourse.course==temp_course)&(TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline1)).id
		semester=data_temp['semester']
		temp_semester=TimetableFinalSemester.get(TimetableFinalSemester.semester_name==semester).id
		no_batch=data_temp['no_batch']
		semester_id=TimetableFinalSemester.get(TimetableFinalSemester.semester_name==semester).id
		for lab in TimetableFinalSemesterLab.select().where(TimetableFinalSemesterLab.semester_table_id==semester_id):
			lab_list.append(lab.lab)
		sub_load=data_temp['load']
		sub_theory=data_temp['schema']['lectures']
		sub_tutorial=data_temp['schema']['tutorials']
		sub_practical=data_temp['schema']['labs']
		if shift=="Both":
			shift1=[]
			shift1.append("Morning")
			shift1.append("Afternoon")
		for shift in shift1:
			TimetableFinalSubject.create(is_elective=elective,sub_code=subject_code,sub_name=subject)
			temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==shift).get()
			shift=temp_shift.id
			if no_batch>0:
				for b in batch_list:
					TimetableFinalSubjectBatch.create(batch_name=str(b['name']),sub_code=subject_code,shift_table_id_id=shift)
			TimetableFinalSubjectDiscipline.create(descipline_course_table_id_id=temp_discipline,semester_table_id_id=temp_semester,shift_table_id_id=shift,sub_code_id=subject_code)
			for l in lab_list:
				TimetableFinalSubjectLab.create(lab=l,sub_code=subject_code)
			TimetableFinalSubjectNoStudent.create(no_batch=no_batch,sub_code=subject_code,shift_table_id_id=shift)
			TimetableFinalSubjectScheme.create(sub_code=subject_code,sub_load=sub_load,sub_practical_class=sub_practical,sub_theory_class=sub_theory,sub_tutorial_class=sub_tutorial)

		return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")


@csrf_exempt
def sub_update(request):
	data=request.body.decode('utf-8')
	data_temp=json.loads(data)
	subject=data_temp['name']
	subject_code=data_temp['subcode']
	elective=data_temp['elective']
	batch_list=data_temp['batches']
	shift=data_temp['shift']
	course=data_temp['course']
	discipline=data_temp['discipline']
	temp_course=TimetableFinalCourse.get(TimetableFinalCourse.course_name==course).course
	temp_discipline1=TimetableFinalDescipline.get(TimetableFinalDescipline.descipline_name==discipline).id
	temp_discipline=TimetableFinalDesciplineCourse.get((TimetableFinalDesciplineCourse.course==temp_course)&(TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline1)).id
	semester=data_temp['semester']
	temp_semester=TimetableFinalSemester.get(TimetableFinalSemester.semester_name==semester).id
	no_batch=data_temp['no_batch']
	sub_load=data_temp['load']
	sub_theory=data_temp['schema']['lectures']
	sub_tutorial=data_temp['schema']['tutorials']
	sub_practical=data_temp['schema']['labs']

	query=TimetableFinalSubject.update(is_elective=elective,sub_code=subject_code,sub_name=subject).where(TimetableFinalSubject.sub_code==subject_code)
	query.execute()
	temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==shift).get()
	shift=temp_shift.id
	query4=TimetableFinalSubjectBatch.delete().where(TimetableFinalSubjectBatch.sub_code==subject_code)
	query4.execute()
	if no_batch>0:
		for x in range(no_batch):
			b=batch_list[x]
			query1=TimetableFinalSubjectBatch.create(batch_name=str(b['name']),sub_code=subject_code,shift_table_id=shift)
	query=TimetableFinalSubjectDiscipline.update(descipline_course_table_id=temp_discipline,shift_table_id=shift,sub_code=subject_code).where(TimetableFinalSubjectDiscipline.sub_code==subject_code)
	num1=query.execute()
	query1=TimetableFinalSubjectNoStudent.update(no_batch=no_batch,sub_code=subject_code,shift_table_id=shift).where(TimetableFinalSubjectNoStudent.sub_code==subject_code)
	num2=query1.execute()
	query2=TimetableFinalSubjectScheme.update(sub_code=subject_code,sub_load=sub_load,sub_practical_class=sub_practical,sub_theory_class=sub_theory,sub_tutorial_class=sub_tutorial).where(TimetableFinalSubjectScheme.sub_code==subject_code)
	num3=query2.execute()
	if num1>=0 and num2>=0 and num3>=0:
		return HttpResponse(json.dumps({"status":"Success"}),content_type="application/json")
	else:
		return HttpResponse(json.dumps({"status":"UnSuccess"}),content_type="application/json")

