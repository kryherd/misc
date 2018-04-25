#!/usr/bin/env python

# This script takes the gradebook downloaded from HuskyCT and outputs section totals
# as well as final percent and letter grades.

# import packages
import pandas as pd
import numpy as np
import bisect
import datetime
import sys
import argparse
import subprocess
import re

# set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--data', action='store', type=str, help="Path to data")
args=parser.parse_args()

# load in data
data = "%s" % (args.data)

# create function that does everything!
def dataclean(data):
	df=pd.read_csv(data) # read in data
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
	# separate the grades by section: student info, quizzes, video activities, LC, exams, clickers
	# also gives dataframes names
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
	#Remove weeks 1 and 2 of clicker points
	clicker.drop(list(clicker.filter(regex = 'Session 2')), axis = 1, inplace = True)
	clicker.drop(list(clicker.filter(regex = 'Session 1')), axis = 1, inplace = True)
	# indicate how many points are in each type of assignment
	totals={"quiz": 5, "video": 5, "lc": 5, "exam": 100, "clicker": 1}
	# function for calculating section averages for assignments that have 2 dropped
	def avg_pct(sec):
		sec.fillna(0, inplace=True) # replaces NaNs with zeroes, for assignments not completed
		avg_name = str(sec.name) + " Average"
		pct_name = str(sec.name) + " Percent"
		# replace exactly two lowest values with NaN; drops two lowest assignments
		for row in sec.iterrows():
			row[1].replace(row[1].sort_values()[0:2],np.nan, inplace=True)
		# create average; NaNs are ignored	
		sec[avg_name] = sec.mean(axis=1)
		# create percentage
		sec[pct_name] = sec[avg_name]/totals[str(sec.name)]*100
	# function for calculating section averages for assignments that have 3 dropped
	def avg_pct_three(sec):
		sec.fillna(0, inplace=True) # replaces NaNs with zeroes, for assignments not completed
		avg_name = str(sec.name) + " Average"
		pct_name = str(sec.name) + " Percent"
		# replace exactly two lowest values with NaN; drops two lowest assignments
		for row in sec.iterrows():
			row[1].replace(row[1].sort_values()[0:3],np.nan, inplace=True)
		# create average; NaNs are ignored	
		sec[avg_name] = sec.mean(axis=1)
		# create percentage
		sec[pct_name] = sec[avg_name]/totals[str(sec.name)]*100
	# calculate section averages with no dropped assignments (i.e., exams)
	def avg_pct_exam(sec):
		avg_name = str(sec.name) + " Average"
		pct_name = str(sec.name) + " Percent"
		sec[avg_name] = sec.mean(axis=1)
		sec[pct_name] = sec[avg_name]/totals[str(sec.name)]*100
	# run function on 4 sections
	dflist = [quiz, video, lc]
	for i in dflist:
		avg_pct(i)
	#run function for clickers
	avg_pct_three(clicker)
	# run function for exams
	avg_pct_exam(exam)
	 # add username info
	quiz= pd.concat([id_info, quiz], axis=1)
	lc= pd.concat([id_info, lc], axis=1)
	video= pd.concat([id_info, video], axis=1)
	clicker= pd.concat([id_info, clicker], axis=1)
	exam= pd.concat([id_info, exam], axis=1)
	# create a totals page
	all = pd.concat([quiz["quiz Percent"], video["video Percent"], lc["lc Percent"], exam["exam Percent"], clicker["clicker Percent"]], axis=1)
	# calculate final grade - exams, LC, friday activities, clicker
	all["Total Grade"] = .60*all.ix[:,3] + .15*all.ix[:,2] + .15*((all.ix[:,1] + all.ix[:,0])/2) + .1*all.ix[:,4]
	# add username info
	all = pd.concat([id_info, all], axis = 1)
	all["Total Grade"].fillna(0, inplace=True)
	# list indicating upper bound for all grades
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
    (110, 'A'),
	]
	grades.sort() # list must be sorted
	# create function to assign letter grades
	def letgrade(to_find):
		pos = bisect.bisect_right(grades, (to_find,))
		return grades[pos][1]
	# assign letter grades
	all["Letter Grade"] = all["Total Grade"].apply(lambda x: letgrade(x))
	# get the current date/time
	now = datetime.datetime.now()
	# formate date/time
	when=now.strftime("%Y-%m-%d-%H%M")
	# create Excel document with multiple sheets
	writer = pd.ExcelWriter('GradeOutput_' + when + '.xlsx')
	all.to_excel(writer, 'Totals', index= False)
	quiz.to_excel(writer, 'Quiz Grades', index= False)
	video.to_excel(writer, 'Video Activity Grades', index= False)
	lc.to_excel(writer, 'LC Grades', index= False)
	clicker.to_excel(writer, 'Clicker Grades', index= False)
	exam.to_excel(writer, 'Exam Grades', index= False)
	writer.save;

# run function
dataclean(data)
