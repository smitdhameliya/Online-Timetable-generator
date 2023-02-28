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
from time_table_models1 import TimetableFinalCourse,TimetableFinalDescipline,TimetableFinalDesciplineCourse,TimetableFinalClassroom,TimetableFinalShift,TimetableFinalTimeslot,TimetableFinalClassroomAvailable,TimetableFinalDay,TimetableFinalFaculty,TimetableFinalSemester,TimetableFinalSubject,TimetableFinalFacultySubject,TimetableFinalLab,TimetableFinalLabAvailable,TimetableFinalSemesterBatch,TimetableFinalSemesterClassroom,TimetableFinalSemesterLab,TimetableFinalSubjectBatch,TimetableFinalSubjectNoStudent,TimetableFinalSubjectScheme,TimetableFinalTimeslotDay,TimetableFinalSubjectDiscipline,TimetableFinalSubjectLab,TimetableFinalTempLab,TimetableFinalFacultyAdd
from .models import descipline,course,descipline_course,day,timeslot,lab,classroom,lab_available,classroom_available,semester,subject_no_student,shift,semester_classroom,semester_lab,subject_batch,semester_batch,subject,subject_scheme,faculty,faculty_subject,timeslot_day,subject_discipline,subject_lab,temp_lab
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def classroom1(course,discipline,shift,term,day_list,timeslot_list,shift_list,semester_list,sub_fac_detail,course_dict):
	course_dict1=course_dict
	db=MySQLDatabase('time_table_test6',user='root',password='',host='localhost')
	db.connect()
	# print(course)
	# print(course_dict[str(course)])
	temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()

	# # print("Hello")
	# day_list=[]
	# for d in TimetableFinalDay.select():
	# 	day_list.append(str(d.day_name))

	# timeslot_list=[]
	# for t in TimetableFinalTimeslot.select():
	# 	timeslot_list.append(str(t.timeslot_name))

	# shift_list=[]
	# for shift1 in TimetableFinalShift.select():
	# 	shift_list.append(str(shift1.shift_name))

	# semester_list=[]
	temp_discipline=TimetableFinalDescipline.select().where(TimetableFinalDescipline.descipline_name==discipline).get()
	temp_shift=TimetableFinalShift.get(TimetableFinalShift.shift_name==str(shift))
	temp_course_discipline=TimetableFinalDesciplineCourse.select().where((TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline.id)&(TimetableFinalDesciplineCourse.course==temp_course.course)).get()
	temp_sem=TimetableFinalSemester.select().where((TimetableFinalSemester.term==term)&(TimetableFinalSemester.descipline_course_table_id==temp_course_discipline.id)&(TimetableFinalSemester.shift_table_id==temp_shift.id)&(TimetableFinalSemester.term==str(term)))
	# for sem in temp_sem:
		# semester_list.append(str(sem.semester_name))

	# sem_sub={}
	# for cou in TimetableFinalCourse.select():
	# 	disc_dict={}
	# 	for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
	# 		sem_dict={}
	# 		for sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==disc.id):
	# 			sub_list=[]
	# 			for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
	# 				# print(sub.sub_code.sub_name)
	# 				# sub_list.append(str(sub.sub_code.sub_name))
	# 				sub_list.append(sub.sub_code.sub_name)
 #                    # print(sem.semester_name,sub.sub_name)
	# 				sem_dict[str(sem.semester_name)]=sub_list
	# 		disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
	# 	sem_sub[str(cou.course_name)]=disc_dict

	# sub_fac_detail={}
	# for temp_course in TimetableFinalCourse.select():
	# 	temp_discipline_dict={}
	# 	for temp_discipline in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course):
	# 		temp_sem_dict={}
	# 		for temp_sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==temp_discipline.id):
	# 			temp_shift_dict={}
	# 			for shift in shift_list:
	# 				temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
	# 				temp_sub_dict={}
	# 				for temp_sub_discipline in TimetableFinalSubjectDiscipline.select().where(TimetableFinalSubjectDiscipline.semester_table_id==temp_sem.id):
	# 					for temp_sub in TimetableFinalSubject.select().where(TimetableFinalSubject.sub_code==temp_sub_discipline.sub_code):
	# 						temp_fac_list=[]
	# 						for temp_fac in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.sub_code==temp_sub.sub_code):
	# 							# print(temp_fac.faculty.faculty)
	# 							# print(str(temp_fac.shift_table_id.id),str(temp_shift.id))
	# 							if temp_fac.shift_table_id.id==temp_shift.id:
	# 								temp_fac_list.append((temp_fac.faculty.faculty,temp_fac.faculty.position,temp_fac.faculty.faculty_name,temp_fac.faculty.work_load))
	# 						temp_fac_list.sort(key=lambda tup:tup[1],reverse=True)
	# 						# print(temp_fac_list)
	# 						temp_i=0
	# 						temp_fac_dict={}
	# 						for temp_fac_2 in temp_fac_list:
	# 							temp_fac_dict[temp_i]={
	# 												'id':temp_fac_2[0],
	# 												'name':temp_fac_2[2],
	# 												'position':temp_fac_2[1],
	# 												'work_load':temp_fac_2[3]
	# 												}
	# 							temp_i+=1
	# 						# print(temp_fac_dict)
	# 						sub_scheme_detail=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==temp_sub).get()
	# 						no_batch=TimetableFinalSubjectNoStudent.get(TimetableFinalSubjectNoStudent.sub_code==temp_sub.sub_code).no_batch
	# 						# print(type(sub_scheme_detail.sub_theory_class))
	# 						# print(type(sub_scheme_detail.sub_tutorial_class))
	# 						# print(type(sub_scheme_detail))
	# 						temp_sub_dict[str(temp_sub.sub_name)]={
	# 																'sub_code':temp_sub.sub_code,
	# 															'sub_name':temp_sub.sub_name,
	# 															'is_elective':temp_sub.is_elective,
	# 															'faculty':temp_fac_dict,
	# 															'sub_load':sub_scheme_detail.sub_load,
	# 															'sub_practical_class':(sub_scheme_detail.sub_practical_class)*(no_batch),
	# 															# 'sub_practical_class':(sub_scheme_detail.sub_practical_class)*(no_batch),
	# 															'sub_theory_class':sub_scheme_detail.sub_theory_class,
	# 															'sub_tutorial_class':sub_scheme_detail.sub_tutorial_class
	# 															}
	# 				temp_shift_dict[str(shift)]=temp_sub_dict
	# 			temp_sem_dict[str(temp_sem.semester_name)]=temp_shift_dict
	# 		temp_discipline_dict[str(temp_discipline.descipline_table_id.descipline_name)]=temp_sem_dict
	# 	sub_fac_detail[str(temp_course.course_name)]=temp_discipline_dict

	# print(sub_fac_detail)

	sem_sub={}		
	for cou in TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course):
		disc_dict={}
		for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
			sem_dict={}
			for sem in TimetableFinalSemester.select().where((TimetableFinalSemester.descipline_course_table_id==disc.id)&(TimetableFinalSemester.term==str(term))):
				sub_list=[]
				for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
					temp_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==sub.sub_code).get()
					theory=temp_scheme.sub_theory_class
					tutorial=temp_scheme.sub_tutorial_class
					if theory>0 or tutorial>0:
						sub_list.append(str(sub.sub_code.sub_name))
                    # print(sem.semester_name,sub.sub_name)
				sem_dict[str(sem.semester_name)]=sub_list
			disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
		sem_sub[str(cou.course_name)]=disc_dict
	# print(sem_sub)


	sub_sem={}
	for cou in TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course):
		disc_dict={}
		for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
			sem_dict={}
			for sem in TimetableFinalSemester.select().where((TimetableFinalSemester.descipline_course_table_id==disc.id)&(TimetableFinalSemester.term==str(term))):
				sub_list=[]
				flag_elective=0
				for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
					temp_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==sub.sub_code).get()
					elective=temp_scheme.sub_code.is_elective
					if elective==1:
						if flag_elective==0:
							theory=temp_scheme.sub_theory_class
							tutorial=temp_scheme.sub_tutorial_class
							if theory>0 or tutorial>0:
								sub_list.append(str(sub.sub_code.sub_name))
								flag_elective=1
					else:
						theory=temp_scheme.sub_theory_class
						tutorial=temp_scheme.sub_tutorial_class	
						if theory>0 or tutorial>0:
							sub_list.append(str(sub.sub_code.sub_name))
				sem_dict[str(sem.semester_name)]=sub_list
			disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
		sub_sem[str(cou.course_name)]=disc_dict


	sub_elective_sem={}
	for cou in TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course):
		disc_dict={}
		for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
			sem_dict={}
			for sem in TimetableFinalSemester.select().where((TimetableFinalSemester.descipline_course_table_id==disc.id)&(TimetableFinalSemester.term==str(term))):
				sub_list=[]
				flag_elective=0
				for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
					temp_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==sub.sub_code).get()
					elective=temp_scheme.sub_code.is_elective
					if elective==1:
						sub_list.append(str(sub.sub_code.sub_name))
						# if flag_elective==0:
						# 	theory=temp_scheme.sub_theory_class
						# 	tutorial=temp_scheme.sub_tutorial_class
						# 	if theory>0 or tutorial>0:
						# 		sub_list.append(str(sub.sub_code.sub_name))
						# 		flag_elective=1
					# else:
					# 	theory=temp_scheme.sub_theory_class
					# 	tutorial=temp_scheme.sub_tutorial_class	
					# 	if theory>0 or tutorial>0:
					# 		sub_list.append(str(sub.sub_code.sub_name))
				# print(sem.semester_name)
				sem_dict[str(sem.semester_name)]=sub_list
				# print(sem_dict)
			disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
			# print(disc_dict)
		sub_elective_sem[str(cou.course_name)]=disc_dict			
	# print(sub_elective_sem)



	sem_timeslot={}
	for sem in semester_list:
		# print(sem_sub[str(course)][str(discipline)][str(sem)],sem)
		subject_list=sub_sem[str(course)][str(discipline)][str(sem)]
		length_of_subject_list=len(subject_list)
		temp1=(length_of_subject_list*2)+2
		timeslot_list1=[]
		# print(len(timeslot_list))
		# print(temp1)
		if temp1>len(timeslot_list):
			timeslot_list1=timeslot_list
		else:
			# print(temp1)
			for i in range(0,temp1+1):
				# print(timeslot_list[i])
				# print(i)
				timeslot_list1.append(timeslot_list[i])
		sem_timeslot[str(sem)]=timeslot_list1

	#course_dict1
	# elective_subjects=[]
	# subject_list2=

	sem_classroom={}
	for sem in semester_list:
		classroom_list=[]
		temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
		for classroom1 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
			classroom_list.append(classroom1.classroom.classroom)
	

	classroom_available={}
	for classroom2 in TimetableFinalClassroomAvailable.select():
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
		classroom_available[str(classroom2.classroom.classroom)]=shift_ava

	temp_data={}
	# print(temp_shift.shift_name)       &(TimetableFinalTempLab.shift_table_id!=temp_shift.id)
	# print(temp_course_discipline.id)
	data_len=TimetableFinalTempLab.select().where((TimetableFinalTempLab.descipline_course_table_id!=temp_course_discipline.id)).count()
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

	sem_timeslot1={}
	sem_dict1=course_dict1[str(course)][str(discipline)]
	# for k1,v1 in sem_dict1.iteritems():
	# 	temp_shift_dict1=sem_dict1[str(v1)]
	# 	shift_dict1={}
	# 	for k2,v2 in temp_shift_dict1.iteritems():
	# 		temp_days_dict1=temp_shift_dict1[str(v2)]
	# 		days_dict1={}
	# 		for k3,v3 in temp_days_dict1.iteritems():
	# 			temp_timeslot_dict=temp_days_dict1[str(v3)]
	# 			timeslot_list1=temp_timeslot_dict.keys()
	# 			timeslot_list2=[]
	# 			for t in timeslot_list:
	# 				if t not in timeslot_list1:
	# 					timeslot_list2.append(t)
	# 			days_dict1[str(v3)]=timeslot_list2
	# 		shift_dict1[str(v2)]=days_dict1
	# 	sem_timeslot1[str(v1)]=shift_dict1

	for k1 in sem_dict1.keys():
		temp_shift_dict1=sem_dict1[k1]
		shift_dict1={}
		for k2 in temp_shift_dict1.keys():
			temp_days_dict1=temp_shift_dict1[k2]
			days_dict1={}
			for d in day_list:
				timeslot_list2=[]
			# for k3 in temp_days_dict1.keys():
				if d in temp_days_dict1:
					temp_timeslot_dict=temp_days_dict1[str(d)]
					timeslot_list1=temp_timeslot_dict.keys()
					for t in timeslot_list:
						if t not in timeslot_list1:
							timeslot_list2.append(str(t))
				else:
					timeslot_list2=timeslot_list
				days_dict1[str(d)]=timeslot_list2
			shift_dict1[str(k2)]=days_dict1
		sem_timeslot1[str(k1)]=shift_dict1
	# print(sem_timeslot1)
	# print(sem_timeslot1[str(7)]["Morning"]["Monday"])


	course_dict={}
	discipline_dict={}	
	sem_dict={}
	for sem in semester_list:
		# print("Hello")
		# print(sem,course)

		elective_subjects=sub_elective_sem[str(course)][str(discipline)][str(sem)]
		temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
		subject_list=sem_sub[str(course)][str(discipline)][str(sem)]

		total_batch=TimetableFinalSemesterBatch.get(TimetableFinalSemesterBatch.semester_table_id==temp_sem.id).no_batches	

		shift_dict={}
		for shift in shift_list:
			temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
			days_dict={}

			for d in day_list:
				subject_list1=sem_sub[str(course)][str(discipline)][str(sem)]
				print(subject_list1)
				if len(subject_list1)>0:
					

					subject_counter={}
					for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
						info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
						for k1 in info3.keys():
							# sub1=info3[k1]
							subject_counter[str(info3['sub_name'])]=0
					faculty_counter={}
					for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
						info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
		            	# print(sub_fac_detail[str(course)][str(discipline)][str(sem)][info4])
		            	# print(info3)
						for k1 in info3.keys():
		               	# sub1=info3[k1]
		               	# print(info3[k1],"Hello")
							faculties=info3['faculty']
							for k2 in faculties.keys():
								fac1=faculties[k2]
								faculty_counter[str(fac1['name'])]=0
					done_timeslot_list=[]
					# print(course_dict)
					# print(str(course))
					temp_dict1=course_dict1[str(course)][str(discipline)][str(sem)][str(shift)]
					if str(d) in temp_dict1:
						temp_dict=temp_dict1[str(d)]
						for t in temp_dict:
							done_timeslot_list.append(str(t))
					flag1=0
					timeslot_dict={}
					# print(len(timeslot_list))
					timeslot_list1=sem_timeslot1[str(sem)][str(shift)][str(d)]
					# for i in range(0,len(timeslot_list)):
					for timeslot in timeslot_list1:
						new_temp_dict={}	
						# t=randint(0,6)
						# timeslot=timeslot_list[t]
						# if timeslot in done_timeslot_list:
							# while timeslot in done_timeslot_list:
								# t=randint(0,6)
								# timeslot=timeslot_list[t]
								# print(sem,timeslot,d)
						# timeslot=timeslot_list[t]


						flag=0

						# for classroom3 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
							# if classroom_available[str(classroom3.classroom.classroom)][str(shift)][str(d)][str(timeslot)]==1:

						if len(course_dict)>0:
							pass
						elif len(sem_dict)>0:
							if len(subject_list1)>1:
								sub=random.choice(subject_list1)
								theory_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
								tutorial_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
								if (theory_class<=0 and tutorial_class<=0) or subject_counter[str(sub)]>=2:
									# print(sub,theory_class,tutorial_class,subject_counter[str(sub)])
									while (theory_class<=0 and tutorial_class<=0) or subject_counter[str(sub)]>=2:
										sub=random.choice(subject_list1)
										# print(sub)
										theory_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
										tutorial_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
								if sub in elective_subjects:
									#subject is elective
									for s in elective_subjects:
										faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(s)]['faculty']
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
											if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=2 or str(fac1['name'])==faculty_old:
												continue
											else:
												for k1 in sem_dict.keys():
													# temp_shift_dict3=sem_dict1[k1]
													temp_shift_dict=sem_dict[str(k1)]
													for k2 in temp_shift_dict.keys():
														# temp_days_dict3=temp_shift_dict3[k2]
														temp_days_dict=temp_shift_dict[str(k2)]
														if str(d) in temp_days_dict:
															temp_timeslot_dict=temp_days_dict[str(d)]
															if str(timeslot) in temp_timeslot_dict:
																temp_info=temp_timeslot_dict[str(timeslot)]
																info1=temp_info['value']
																for key1 in info1.keys():
																	info=info1[key1]
																	if info['faculty']==str(fac1['name']):
																		inner_flag=1
													for k1 in sem_dict1.keys():
														temp_shift_dict3=sem_dict1[k1]
														for k2 in temp_shift_dict3.keys():
															temp_day_dict3=temp_shift_dict3[k2]
															if d in temp_day_dict3:
																temp_timeslot_dict3=temp_day_dict3[d]
																if timeslot in temp_timeslot_dict3: 
																	temp_info3=temp_timeslot_dict3[timeslot]
																	temp_info4=temp_info3['value']
																	for key1 in temp_info4.keys():
																		info=temp_info4[key1]
																		if info['faculty']==str(fac1['name']):
																			inner_flag=1
												if inner_flag==1:
													continue
												else:
													classroom1=""
													for classroom3 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
														if classroom_available[str(classroom3.classroom.classroom)][str(shift)][str(d)][str(timeslot)]==1:
															classroom1=str(classroom3.classroom.classroom)
															break
													theory_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
													tutorial_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
													if theory_class>tutorial_class:
														print(str(sub))
														new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'theory'}
														timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
														sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']-=1

													else:
														new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'tutorial'}
														timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
														sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']-=1
													if str(fac1['name']) in faculty_counter:
														faculty_counter[str(fac1['name'])]+=1
													else:
														faculty_counter[str(fac1['name'])]=1
													if s in subject_counter:
														subject_counter[str(s)]+=1
													else:
														subject_counter[str(s)]=1
													done_timeslot_list.append(timeslot)
													if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']==0 and sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']==0:
														subject_list1.remove(s)
														elective_subjects.remove(s)
													flag=1
													break#faculty['k']	


								else:
									#subject is selective
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
										if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=2 or str(fac1['name'])==faculty_old:
											continue
										else:
											for k1 in sem_dict.keys():
												temp_shift_dict=sem_dict[str(k1)]
												for k2 in temp_shift_dict.keys():
													temp_days_dict=temp_shift_dict[str(k2)]
													if str(d) in temp_days_dict:
														temp_timeslot_dict=temp_days_dict[str(d)]
														if str(timeslot) in temp_timeslot_dict:
															temp_info=temp_timeslot_dict[str(timeslot)]
															info1=temp_info['value']
															for key1 in info1.keys():
																info=info1[key1]
																if info['faculty']==str(fac1['name']):
																	inner_flag=1
											for k1 in sem_dict1.keys():
												temp_shift_dict3=sem_dict1[k1]
												for k2 in temp_shift_dict3.keys():
													temp_day_dict3=temp_shift_dict3[k2]
													if d in temp_day_dict3:
														temp_timeslot_dict3=temp_day_dict3[d]
														if timeslot in temp_timeslot_dict3: 
															temp_info3=temp_timeslot_dict3[timeslot]
															temp_info4=temp_info3['value']
															for key1 in temp_info4.keys():
																info=temp_info4[key1]
																if info['faculty']==str(fac1['name']):
																	inner_flag=1
											if inner_flag==1:
												continue
											else:
												classroom1=""
												for classroom3 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
													if classroom_available[str(classroom3.classroom.classroom)][str(shift)][str(d)][str(timeslot)]==1:
														classroom1=str(classroom3.classroom.classroom)
														break
												theory_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
												tutorial_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
												if theory_class>tutorial_class:
													new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'theory'}
													timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
													sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']-=1

												else:
													new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'tutorial'}
													timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
													sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']-=1
												if str(fac1['name']) in faculty_counter:
													faculty_counter[str(fac1['name'])]+=1
												else:
													faculty_counter[str(fac1['name'])]=1
												if str(sub) in subject_counter:
													subject_counter[str(sub)]+=1
												else:
													subject_counter[str(sub)]=1
												done_timeslot_list.append(timeslot)
												if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']==0 and sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']==0:
													subject_list1.remove(sub)
												flag=1
												break#faculty['k']
							elif len(subject_list1)==1:
								sub=subject_list1[0]
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
									if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=2 or str(fac1['name'])==faculty_old:
										continue
									else:
										for k1 in sem_dict.keys():
											temp_shift_dict=sem_dict[str(k1)]
											for k2 in temp_shift_dict.keys():
												temp_days_dict=temp_shift_dict[str(k2)]
												if str(d) in temp_days_dict:
													temp_timeslot_dict=temp_days_dict[str(d)]
													if str(timeslot) in temp_timeslot_dict:
														temp_info=temp_timeslot_dict[str(timeslot)]
														info1=temp_info['value']
														for key1 in info1.keys():
															info=info1[key1]
															if info['faculty']==str(fac1['name']):
																inner_flag=1
										for k1 in sem_dict1.keys():
											temp_shift_dict3=sem_dict1[k1]
											for k2 in temp_shift_dict3.keys():
												temp_day_dict3=temp_shift_dict3[k2]
												if d in temp_day_dict3:
													temp_timeslot_dict3=temp_day_dict3[d]
													if timeslot in temp_timeslot_dict3: 
														temp_info3=temp_timeslot_dict3[timeslot]
														temp_info4=temp_info3['value']
														for key1 in temp_info4.keys():
															info=temp_info4[key1]
															if info['faculty']==str(fac1['name']):
																inner_flag=1
										if inner_flag==1:
											continue
										else:
											classroom1=""
											for classroom3 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
												if classroom_available[str(classroom3.classroom.classroom)][str(shift)][str(d)][str(timeslot)]==1:
													classroom1=str(classroom3.classroom.classroom)
													break
											theory_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
											tutorial_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
											if theory_class>tutorial_class:
												new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'theory'}
												timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
												sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']-=1

											else:
												new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'tutorial'}
												timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
												sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']-=1
											if str(fac1['name']) in faculty_counter:
												faculty_counter[str(fac1['name'])]+=1
											else:
												faculty_counter[str(fac1['name'])]=1
											if str(sub) in subject_counter:
												subject_counter[str(sub)]+=1
											else:
												subject_counter[str(sub)]=1
											done_timeslot_list.append(timeslot)
											if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']==0 and sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']==0:
												subject_list1.remove(sub)
											flag=1
											break#faculty['k']

						else:
							if len(subject_list1)>1:
								# print("Hello")
								# print(sem)
								sub=random.choice(subject_list1)
								theory_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
								tutorial_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
								if (theory_class<=0 and tutorial_class<=0) or subject_counter[str(sub)]>=2:
									while (theory_class<=0 and tutorial_class<=0) or subject_counter[str(sub)]>=2:
										sub=random.choice(subject_list1)
										theory_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
										tutorial_class=subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
								if sub in elective_subjects:
									#subject is elective
									for s in elective_subjects:
										faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(s)]['faculty']
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
											if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=2 or str(fac1['name'])==faculty_old:
												continue
											else:
												for k1 in sem_dict.keys():
													temp_shift_dict=sem_dict[str(k1)]
													for k2 in temp_shift_dict.keys():
														temp_days_dict=temp_shift_dict[str(k2)]
														if str(d) in temp_days_dict:
															temp_timeslot_dict=temp_days_dict[str(d)]
															if str(timeslot) in temp_timeslot_dict:
																temp_info=temp_timeslot_dict[str(timeslot)]
																info1=temp_info['value']
																for key1 in info1.keys():
																	info=info1[key1]
																	if info['faculty']==str(fac1['name']):
																		inner_flag=1
												for k1 in sem_dict1.keys():
													temp_shift_dict3=sem_dict1[k1]
													for k2 in temp_shift_dict3.keys():
														temp_day_dict3=temp_shift_dict3[k2]
														if d in temp_day_dict3:
															temp_timeslot_dict3=temp_day_dict3[d]
															if timeslot in temp_timeslot_dict3: 
																temp_info3=temp_timeslot_dict3[timeslot]
																temp_info4=temp_info3['value']
																for key1 in temp_info4.keys():
																	info=temp_info4[key1]
																	if info['faculty']==str(fac1['name']):
																		inner_flag=1
												if inner_flag==1:
													continue
												else:
													classroom1=""
													for classroom3 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
														if classroom_available[str(classroom3.classroom.classroom)][str(shift)][str(d)][str(timeslot)]==1:
															classroom1=str(classroom3.classroom.classroom)
															break
													theory_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
													tutorial_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
													if theory_class>tutorial_class:
														new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'theory'}
														timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
														sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']-=1

													else:
														new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'tutorial'}
														timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
														sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']-=1
													if str(fac1['name']) in faculty_counter:
														faculty_counter[str(fac1['name'])]+=1
													else:
														faculty_counter[str(fac1['name'])]=1
													if s in subject_counter:
														subject_counter[str(s)]+=1
													else:
														subject_counter[str(s)]=1
													done_timeslot_list.append(timeslot)
													if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']==0 and sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']==0:
														subject_list1.remove(s)
														elective_subjects.remove(s)
													flag=1
													break#faculty['k']
								else:
									faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['faculty']
									faculty_flag=0
									for k in faculties:
										inner_flag=0
										fac1=faculties[k]
										faculty_old=""
										if len(temp_data)>0:
											# print("HEllo")
											if str(d) in temp_data:
												new_temp_data=temp_data[str(d)]
												if timeslot in new_temp_data:
													faculty_old=new_temp_data[timeslot]['faculty']
										for k1 in sem_dict1.keys():
											temp_shift_dict3=sem_dict1[k1]
											for k2 in temp_shift_dict3.keys():
												temp_day_dict3=temp_shift_dict3[k2]
												if d in temp_day_dict3:
													temp_timeslot_dict3=temp_day_dict3[d]
													if timeslot in temp_timeslot_dict3: 
														temp_info3=temp_timeslot_dict3[timeslot]
														temp_info4=temp_info3['value']
														for key1 in temp_info4.keys():
															info=temp_info4[key1]
															# print(info)
															if info['faculty']==str(fac1['name']):
																inner_flag=1
																old_faculty=str(fac1['name'])
										if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=2 or str(fac1['name'])==faculty_old or inner_flag==1:
											# print("HEllo")
											continue
										else:
											# print("HEllo")
											classroom1=""
											for classroom3 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
												if classroom_available[str(classroom3.classroom.classroom)][str(shift)][str(d)][str(timeslot)]==1:
													classroom1=str(classroom3.classroom.classroom)
													break
											theory_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
											tutorial_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
											if theory_class>tutorial_class:
												new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'theory'}
												timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
												sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']-=1

											else:
												new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'tutorial'}
												timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
												sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']-=1
											if str(fac1['name']) in faculty_counter:
												faculty_counter[str(fac1['name'])]+=1
											else:
												faculty_counter[str(fac1['name'])]=1
											if str(sub) in subject_counter:
												subject_counter[str(sub)]+=1
											else:
												subject_counter[str(sub)]=1
											done_timeslot_list.append(timeslot)
											if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']==0 and sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']==0:
												subject_list1.remove(sub)
											flag=1
											break#faculty['k']



							elif len(subject_list1)==1:
								# flag=0
								# print(subject_list1)
								sub=subject_list1[0]
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

									for k1 in sem_dict1.keys():
										temp_shift_dict3=sem_dict1[k1]
										for k2 in temp_shift_dict3.keys():
											temp_day_dict3=temp_shift_dict3[k2]
											if d in temp_day_dict3:
												temp_timeslot_dict3=temp_day_dict3[d]
												if timeslot in temp_timeslot_dict3: 
													temp_info3=temp_timeslot_dict3[timeslot]
													temp_info4=temp_info3['value']
													for key1 in temp_info4.keys():
														info=temp_info4[key1]
														if info['faculty']==str(fac1['name']):
															inner_flag=1
															old_faculty=str(fac1['name'])
									if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=2 or str(fac1['name'])==faculty_old or inner_flag==1:
										continue
									else:
										classroom1=""
										for classroom3 in TimetableFinalSemesterClassroom.select().where(TimetableFinalSemesterClassroom.semester_table_id==temp_sem.id):
											if classroom_available[str(classroom3.classroom.classroom)][str(shift)][str(d)][str(timeslot)]==1:
												classroom1=str(classroom3.classroom.classroom)
												# print("Hello")
												break
										theory_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']
										tutorial_class=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']
										if theory_class>tutorial_class:
											new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'theory'}
											timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
											sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']-=1

										else:
											new_temp_dict[str(sub)]={'faculty':str(fac1['name']),'subject':str(sub),'classroom':classroom1,'type':'tutorial'}
											timeslot_dict[str(timeslot)]={'lab':0,'classroom':1,'value':new_temp_dict}
											sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']-=1
										if str(fac1['name']) in faculty_counter:
											faculty_counter[str(fac1['name'])]+=1
										else:
											faculty_counter[str(fac1['name'])]=1
										done_timeslot_list.append(timeslot)
										if sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_theory_class']==0 and sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_tutorial_class']==0:
											subject_list1.remove(sub)
										flag=1
										break#faculty['k']
							# if flag==1:
							# 	flag1=1
							# 	break#classroom
						# if flag1==1:
						# 	break
					days_dict[str(d)]=timeslot_dict
			shift_dict[str(shift)]=days_dict
		sem_dict[str(sem)]=shift_dict
	discipline_dict[str(discipline)]=sem_dict
	course_dict[str(course)]=discipline_dict
	db.close()
	return course_dict
	# print(course_dict)


					# old_timeslot_dict=course_dict[str(course)][str(discipline)][str(sem)][str(shift)][str(d)]
					# for key,value in old_timeslot_dict.iteritems():
					# 	old_timeslot_dict[key]=timeslot_dict[key]

