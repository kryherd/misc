#!/usr/bin/env python
import pandas as pd
import numpy as np
import bisect

data = "./gradesanon.csv"

def dataclean(data):
	df=pd.read_csv(data) # read in dataa
	df.columns = df.columns.str.replace("[()]", ".") #replace parentheses in column names; avoids errors
	# remove previewusers -- not real students
	remove=df.index[df['Username'].str.contains("previewuser")].tolist()
	df=df.drop(df.index[remove])
	# remove any column where 80% of students have not completed the assignment
	# effectively removes things that haven't been assigned yet
	emptlist = []
	for column in df:
		empty=float(df[column].isnull().sum())/float(len(df))
		if empty > .8:
			test = df.columns.get_loc(column)
			emptlist.append(test)
	df=df.drop(df.columns[emptlist], axis=1)
	id_info=df.filter(items=['Username'])
	quiz=df.filter(regex='Chapter\s\d{2}\sQuiz')
	quiz.name="quiz"
	video=df.filter(regex='Video\sActivities')
	video.name="video"
	lc=df.filter(regex='LearningCurve')
	lc.name="lc"
	exam=df.filter(regex='Exam\s\d\sPercent')
	exam.name="exam"
	clicker=df.filter(regex='Session')
	clicker.name="clicker"
	# calculate stuff
	totals={"quiz": 5, "video": 5, "lc": 5, "exam": 100, "clicker": 1}
	def avg_pct(sec):
		sec.fillna(0, inplace=True)
		avg_name = str(sec.name) + " Average"
		pct_name = str(sec.name) + " Percent"
		for row in sec.iterrows():
			row[1].replace(row[1].sort_values()[0:2],np.nan, inplace=True)
		sec[avg_name] = sec.mean(axis=1)
		sec[pct_name] = sec[avg_name]/totals[str(sec.name)]*100
		sec = pd.concat([id_info, sec], axis=1)
	def avg_pct_exam(sec):
		sec.fillna(0, inplace=True)
		avg_name = str(sec.name) + " Average"
		pct_name = str(sec.name) + " Percent"
		sec[avg_name] = sec.mean(axis=1)
		sec[pct_name] = sec[avg_name]/totals[str(sec.name)]*100
		sec = pd.concat([id_info, sec], axis=1)
	dflist = [quiz, video, lc, clicker]
	for i in dflist:
		avg_pct(i)
	avg_pct_exam(exam)
	dflist2 = [quiz, video, lc, exam, clicker]
	all = pd.concat([quiz["quiz Percent"], video["video Percent"], lc["lc Percent"], exam["exam Percent"], clicker["clicker Percent"]], axis=1)
	all["Total Grade"] = .60*all.ix[:,3] + .15*all.ix[:,2] + .15*((all.ix[:,1] + all.ix[:,0])/2) + .1*all.ix[:,4]
	all = pd.concat([id_info, all], axis = 1)	
	grades = [
    (59.5, 'F'),
    (63.49, 'D-'),
    (66.49, 'D'),
    (69.49, 'D+'),
    (73.49, 'C-'),
    (76.49, 'C'),
    (79.49, 'C+'),
    (83.49, 'B-'),
    (86.49, 'B'),
    (89.49, 'B+'),
    (93.49, 'A-'),
    (96.49, 'A'),
    (99.49, 'A+'),
	]
	grades.sort() # list must be sorted
	def letgrade(to_find):
		pos = bisect.bisect_right(grades, (to_find,))
		return grades[pos][1]
	all["Letter Grade"] = all["Total Grade"].apply(lambda x: letgrade(x))
	print all;
	
dataclean(data)
