import math
import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta,date
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExportList.ExportListCurrent import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.DatePicker import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.PunchCard.CalcTimePad import *

import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *
import requests

class RosterUi:
	def fromEXCEL(self):
		try:
			print("Clearing Current RosterShift's")
			with Session(ENGINE) as session:
				session.query(RosterShift).delete()
				session.commit()
				session.flush()
			print("Loading New RosterShifts From Github Hosted Excel/ODS...")
			src="https://github.com/0rion-HunterShield/Schedule/raw/refs/heads/main/schedule.ods"
			#schedule.ods
			page=requests.get(src)
			if page.status_code == 200:
				print(page)
				lclfile=Path("LOCAL_SCHEDULE")
				if lclfile.exists():
					lclfile.unlink()
				with open(lclfile,"wb") as outf:
					for chunk in page.iter_content():
						if chunk:
							outf.write(chunk)
				df=pd.read_excel(lclfile,engine="odf")
				for row in df.itertuples():
					#print(row)
					fname=row.FirstName
					lname=row.LastName
					flName=f"{fname},{lname}"
					#String needs to be month/day/year@hh:mm(FROM)-hh:mm(TO)
					try:
						shift_string=f"{row.Date.month}/{row.Date.day}/{row.Date.year}@{row.ShiftStart.hour}:{row.ShiftStart.minute}-{row.ShiftEnd.hour}:{row.ShiftEnd.minute}"
						if pd.isna(row.LunchStart) or pd.isna(row.LunchEnd) or pd.isna(row.LunchDate):
							lunch_string="no-lunch"
						else:
							lunch_string=f"{row.LunchDate.month}/{row.LunchDate.day}/{row.LunchDate.year}@{row.LunchStart.hour}:{row.LunchStart.minute}-{row.LunchEnd.hour}:{row.LunchEnd.minute}"
						dpt=row.Department
						print(flName,shift_string,lunch_string,sep="@")
						self.addShift(shift_string=shift_string,lunch_string=lunch_string,flName=flName,dpt=dpt)
					except Exception as e:
						print(e,row,type(row.LunchStart),row.LunchStart)
		except Exception as e:
			print(e)

	def fromBlog(self):
		print("Clearing Current RosterShift's")
		with Session(ENGINE) as session:
			session.query(RosterShift).delete()
			session.commit()
			session.flush()
		print("Loading New RosterShifts From Blog...")
		src="https://kl11-sw156.blogspot.com/2024/10/schedule.html"
		page=requests.get(src)
		if page.status_code == 200:
			soup=BS(page.content,"html.parser")
			#print(soup)
			paragraphs=soup.find_all("div",{"class":"post-body entry-content float-container"})
			broker=''
			for num,i in enumerate(paragraphs):
				#print(i)
				para=num,i.text
				for num2,i2 in enumerate(para[1].split("&")):
					#print(i2)
					try:
						flName,shift_string,lunch_string,dpt=i2.split("#")
						print(flName,shift_string,lunch_string,sep="@")
						self.addShift(shift_string=shift_string,lunch_string=lunch_string,flName=flName,dpt=dpt)
					except Exception as e:
						print(f"Invalid Shift Line {repr(e)},{e},{i2}")
					
	def addShift(self,shift_string=None,lunch_string=None,flName=None,dpt=None):
		with Session(ENGINE) as session:
				while True:
					try:
						if shift_string != None:
							print(shift_string)
							if shift_string in ['vctn','unavailable','vacation','sucking balls','unknown reason','being a $2 fucking whore as an ass bitch to $YOURCHOICE_PERSON']:
								shift_range=[None,None]
							try:
								shift_range=FormBuilderMkText(shift_string,"datetime~")
							except Exception as e:
								return
						else:
							shift_range=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Shift DateString [mm/day/year@hh:mm(start)-hh:mm(end)]",data="datetime~")
						print(shift_range,"Shift Range")
						if shift_range in [None,'d']:
							return
						elif shift_range in ['RETRY',]:
							continue
						break
					except Exception as e:
						print(e)
				while True:
					try:
						if lunch_string != None:
							print(lunch_string)
							try:
								if lunch_string.lower() in ['no-lunch','no_lunch','nl','vctn','unavailable','vacation','sucking balls','unknown reason','being a $2 fucking whore as an ass bitch to $YOURCHOICE_PERSON']:
									lunch_range=[None,None]
								else:
									lunch_range=FormBuilderMkText(lunch_string,"datetime~")
							except Exception as e:
								print(e)
								return e
						else:
							lunch_range=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"Shift Lunch DateString [mm/day/year@hh:mm(start)-hh:mm(end)]",data="datetime~")
						if lunch_range in [None,]:
							return
						elif lunch_range in ['d',]:
							lunch_range=[None,None]
						elif lunch_range in ['RETRY',]:
							continue
						break
					except Exception as e:
						print(e)
				print(lunch_range,"Lunch Range")
				while True:
					whoId=None
					if flName == None:
						whoSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Who are you scheduling?",helpText="firstname/lastname",data="string")
					whoSearch=''
					if whoSearch in [None,]:
						return
					elif whoSearch in ['d',]:
						who=session.query(Roster).order_by(Roster.LastName).all()
					else:
						if flName != None:
							print(flName)
							FirstName,LastName=flName.split(",")
							if FirstName.startswith(" "):
								FirstName=FirstName[1:]
							if FirstName.endswith(" "):
								FirstName=FirstName[:1]
							if LastName.startswith(" "):
								LastName=LastName[1:]
							if LastName.endswith(" "):
								LastName=LastName[:1]
							who=session.query(Roster).filter(or_(Roster.FirstName.icontains(FirstName),Roster.LastName.icontains(LastName))).order_by(Roster.LastName.asc()).all()
						else:
							who=session.query(Roster).filter(or_(Roster.FirstName.icontains(whoSearch),Roster.LastName.icontains(whoSearch))).order_by(Roster.LastName.asc()).all()
						whoCt=len(who)
						if whoCt == 0:
							print(f"There is no one by that name {flName}, please this person")
							return
						if whoCt > 1:
							for num,i in enumerate(who):
								msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {whoCt} -> {Fore.cyan}{i.LastName},{Fore.light_magenta}{i.FirstName}{Style.reset}"""
								print(msg)
							which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left of the screen",data="integer")
							if which in [None,]:
								return
							elif which in ['d']:
								which=0
						else:
							which=0
						selectedPerson=who[which]
						whoId=selectedPerson.RoId
						break
				while True:
					dptId=None
					if dpt == None:
						dptSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What Department?",helpText="name",data="string")
					else:
						dptSearch=dpt
						print(dpt)
					if dptSearch in [None,]:
						return
					elif dptSearch in ['d']:
						dpts=session.query(Department).order_by(Department.Name.asc())
					else:
						dpts=session.query(Department).filter(or_(Department.Position.icontains(dptSearch),Department.Name.icontains(dptSearch)))
					try:
						dptSearchInteger=int(eval(dptSearch))
						dpts=dpts.filter(or_(Department.Number==dptSearchInteger))
					except Exception as e:
						print(e)
						try:
							dptSearchInteger=int(dptSearch)
							dpts=dpts.filter(or_(Department.Number==dptSearchInteger))
						except Exception as ee:
							print(ee)



					dpts=dpts.all()
					dptsCt=len(dpts)
					if dptsCt == 0:
						print(f"There is no one by that name, please add the {dptSearch} department!")
						return
					if dptsCt > 1:
						for num,i in enumerate(dpts):
							msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {dptsCt} -> {Fore.cyan}{i.Name} {i.Position} {Fore.light_magenta}{i.Number}"""
							print(msg)
						which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left of the screen",data="integer")
						if which in [None,]:
							return
						elif which in ['d']:
							which=0
					else:
						which=0
					selectedDpt=dpts[which]
					dptId=selectedDpt.dptId
					break
				RoSh=RosterShift(dptId=dptId,RoId=whoId,ShiftStart=shift_range[0],ShiftEnd=shift_range[1],ShiftLunchStart=lunch_range[0],ShiftLunchEnd=lunch_range[1],DTOE=datetime.now())
				session.add(RoSh)
				session.commit()
				session.refresh(RoSh)
				print(RoSh)

	def legend(self):
		header=f"""\n{Fore.grey_50}DAYNAME of {Fore.grey_70}Week WEEK_NUMBER|{Fore.light_green}Index/{Fore.light_yellow}Count {Fore.orange_red_1}of TOTAL -> {Fore.cyan}LastName,{Fore.light_magenta}FirstName [{Fore.light_yellow}DPT{Fore.light_magenta}] - {Fore.light_green}SS(SHIFT START)/{Fore.light_red}SE(SHIFT END)/{Fore.light_yellow}LS(LunchStart)/{Fore.dark_goldenrod}LE(LunchEnd) {Fore.grey_70}#NOTE {Fore.light_yellow}LS({Fore.orange_red_1}None{Fore.light_yellow})/{Fore.dark_goldenrod}LE({Fore.orange_red_1}None{Fore.dark_goldenrod}) Means {Fore.light_red}No Lunch{Style.reset}
{Style.bold}After 12PM{Style.reset} ... Shifts that occur after 12PM
{Style.dim}Before 12PM{Style.reset} ... Shifts that occur before 12PM
"""
		print(header)

	def caRosterShift(self):
		with Session(ENGINE) as session:
			session.query(RosterShift).delete()
			session.commit()
			session.flush()
			
	def caPeople(self):
		with Session(ENGINE) as session:
			session.query(Roster).delete()
			session.commit()
			session.flush()

	def caDepartments(self):
		with Session(ENGINE) as session:
			session.query(Department).delete()
			session.commit()
			session.flush()
	
	def laRosterShift(self):
		with Session(ENGINE) as session:
			RS=session.query(RosterShift).order_by(RosterShift.ShiftStart.asc()).all()
			rsCt=len(RS)
			if rsCt == 0:
				print("No Shifts scheduled")
				return
			for num,i in enumerate(RS):
				selectedPerson=session.query(Roster).filter(Roster.RoId==i.RoId).first()
				if not selectedPerson:
					continue
				dpt=session.query(Department).filter(Department.dptId==i.dptId).first()
				if dpt:
					dptName=f"{dpt.Name}.{dpt.Position} - {dpt.Number}"
				else:
					dptName=f"N/A - N/A"
				if i.ShiftStart.hour >= 12:
					dayEnd=f"{Style.bold}After 12PM "
				else:
					dayEnd=f'{Style.dim}Before 12PM '
					if i.ShiftStart.hour == 0:
						yesterday=datetime(i.ShiftStart.year,i.ShiftStart.month,i.ShiftStart.day)-timedelta(days=1)
						dayEnd+=f'{Fore.light_cyan}(Might Be {yesterday.strftime("%A")})'
				msg=f"""{dayEnd}{Fore.grey_50}{Fore.grey_50}{i.ShiftStart.strftime("%A")} of {Fore.grey_70}Week {i.ShiftStart.strftime("%W")}|{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {rsCt} -> {Fore.cyan}{selectedPerson.LastName},{Fore.light_magenta}{selectedPerson.FirstName} [{Fore.light_yellow}{dptName}{Fore.light_magenta}] - {Fore.light_green}SS({i.ShiftStart})/{Fore.light_red}SE({i.ShiftEnd})/{Fore.light_yellow}LS({i.ShiftLunchStart})/{Fore.dark_goldenrod}LE({i.ShiftLunchEnd}){self.shiftDuration_wo_lunch(i)}{Style.reset}"""
				#msg=f'''{num}/{num+1} of {rsCt} -> {selectedPerson.LastName},{selectedPerson.FirstName} [{dptName}] - SS({i.ShiftStart})/SE({i.ShiftEnd})/LS({i.ShiftLunchStart})/LE({i.ShiftLunchEnd})'''
				print(msg)
		self.legend()

	def saRosterShift(self):
		with Session(ENGINE) as session:
			while True:
				whoSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Who are you searching?",helpText="firstname/lastname",data="string")
				if whoSearch in [None,]:
					return
				elif whoSearch in ['d',]:
					who=session.query(Roster).order_by(Roster.LastName).all()
				else:
					who=session.query(Roster).filter(or_(Roster.FirstName.icontains(whoSearch),Roster.LastName.icontains(whoSearch))).order_by(Roster.LastName.asc()).all()
				whoCt=len(who)
				if whoCt == 0:
					print("There is no one by that name")
					continue
				for num,i in enumerate(who):
					msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {whoCt} -> {Fore.cyan}{i.LastName},{Fore.light_magenta}{i.FirstName}{Style.reset}"""
					print(msg)
				which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left of the screen",data="integer")
				if which in [None,]:
					return
				elif which in ['d']:
					which=0
				selectedPerson=who[which]
				RS=session.query(RosterShift).filter(RosterShift.RoId==selectedPerson.RoId).order_by(RosterShift.ShiftStart.asc()).all()
				rsCt=len(RS)
				if rsCt == 0:
					print("No Shifts scheduled")
					return
				for num,i in enumerate(RS):
					dpt=session.query(Department).filter(Department.dptId==i.dptId).first()
					if dpt:
						dptName=f"{dpt.Name}.{dpt.Position} - {dpt.Number}"
					else:
						dptName=f"N/A - N/A"
					if i.ShiftStart.hour >= 12:
						dayEnd=f"{Style.bold}After 12PM "
					else:
						dayEnd=f'{Style.dim}Before 12PM '
						if i.ShiftStart.hour == 0:
							yesterday=datetime(i.ShiftStart.year,i.ShiftStart.month,i.ShiftStart.day)-timedelta(days=1)
							dayEnd+=f'{Fore.light_cyan}(Might Be {yesterday.strftime("%A")})'
					msg=f"""{dayEnd}{Fore.grey_50}{Fore.grey_50}{i.ShiftStart.strftime("%A")} of {Fore.grey_70}Week {i.ShiftStart.strftime("%W")}|{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {whoCt} -> {Fore.cyan}{selectedPerson.LastName},{Fore.light_magenta}{selectedPerson.FirstName} [{Fore.light_yellow}{dptName}{Fore.light_magenta}] - {Fore.light_green}SS({i.ShiftStart})/{Fore.light_red}SE({i.ShiftEnd})/{Fore.light_yellow}LS({i.ShiftLunchStart})/{Fore.dark_goldenrod}LE({i.ShiftLunchEnd}){self.shiftDuration_wo_lunch(i)}{Style.reset}"""
					#msg=f'''{num}/{num+1} of {rsCt} -> {selectedPerson.LastName},{selectedPerson.FirstName} [{dptName}] - SS({i.ShiftStart})/SE({i.ShiftEnd})/LS({i.ShiftLunchStart})/LE({i.ShiftLunchEnd})'''
					print(msg)
				self.legend()

	def whosHereTomorrow(self):
		with Session(ENGINE) as session:
			tdy=datetime.today()
			today=datetime(tdy.year,tdy.month,tdy.day)+timedelta(days=1)
			tmro=today+timedelta(days=1)
			RS=session.query(RosterShift).filter(RosterShift.ShiftStart>=today,tmro>=RosterShift.ShiftStart).all()
			rsCt=len(RS)
			if rsCt == 0:
				print("No Shifts scheduled")
				return
			dpts=session.query(Department).all()
			dptsCt=len(dpts)
			helpText=''
			totalplp=0
			dptShow=[]
			for num,i in enumerate(dpts):
				msg=f"{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{dptsCt} -> {Fore.light_steel_blue}{i.Name}.{Fore.light_magenta}{i.Position} {Fore.medium_violet_red}{i.Number}{Style.reset}\n"
				helpText+=msg
			print(helpText)
			whichDpts=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which department indexes? ",helpText=helpText,data="list")
			if whichDpts in [None,]:
				return
			elif whichDpts in ['d',[]]:
				whichDpts=[i.dptId for i in dpts]
			else:
				try:
					tmp=[]
					for i in whichDpts:
						try:
							tmp.append(dpts[int(i)].dptId)
						except Exception as e:
							print(e)
					whichDpts=tmp
				except Exception as e:
					print(e)
			for num,i in enumerate(RS):
				dpt=session.query(Department).filter(Department.dptId==i.dptId).first()
				if dpt.dptId in whichDpts:
					selectedPerson=session.query(Roster).filter(Roster.RoId==i.RoId).first()
					if not selectedPerson:
						continue
					if dpt:
						dptName=f"{dpt.Name}.{dpt.Position} - {dpt.Number}"
					else:
						dptName=f"N/A - N/A"
					if i.ShiftStart.hour >= 12:
						dayEnd=f"{Style.bold}After 12PM "
					else:
						dayEnd=f'{Style.dim}Before 12PM '
						if i.ShiftStart.hour == 0:
							yesterday=datetime(i.ShiftStart.year,i.ShiftStart.month,i.ShiftStart.day)-timedelta(days=1)
							dayEnd+=f'{Fore.light_cyan}(Might Be {yesterday.strftime("%A")})'
					msg=f"""{dayEnd}{Fore.grey_50}{i.ShiftStart.strftime("%A")} of {Fore.grey_70}Week {i.ShiftStart.strftime("%W")}|{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {rsCt} -> {Fore.cyan}{selectedPerson.LastName},{Fore.light_magenta}{selectedPerson.FirstName} [{Fore.light_yellow}{dptName}{Fore.light_magenta}] - {Fore.light_green}SS({i.ShiftStart})/{Fore.light_red}SE({i.ShiftEnd})/{Fore.light_yellow}LS({i.ShiftLunchStart})/{Fore.dark_goldenrod}LE({i.ShiftLunchEnd}){self.shiftDuration_wo_lunch(i)}{Style.reset}"""
					#msg=f'''{num}/{num+1} of {rsCt} -> {selectedPerson.LastName},{selectedPerson.FirstName} [{dptName}] - SS({i.ShiftStart})/SE({i.ShiftEnd})/LS({i.ShiftLunchStart})/LE({i.ShiftLunchEnd})'''
					print(msg)
					totalplp+=1
					if dptName not in dptShow:
						dptShow.append(dptName)
			print(f'''Showing {totalplp} individuals for {','.join(dptShow)} Departments.''')
		self.legend()

	def whosHere(self):
		with Session(ENGINE) as session:
			tdy=datetime.today()
			today=datetime(tdy.year,tdy.month,tdy.day)
			tmro=today+timedelta(days=1)
			RS=session.query(RosterShift).filter(RosterShift.ShiftStart>=today,tmro>RosterShift.ShiftStart).all()
			rsCt=len(RS)
			if rsCt == 0:
				print("No Shifts scheduled")
				return
			dpts=session.query(Department).all()
			dptsCt=len(dpts)
			helpText=''
			totalplp=0
			dptShow=[]
			for num,i in enumerate(dpts):
				msg=f"{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{dptsCt} -> {Fore.light_steel_blue}{i.Name}.{Fore.light_magenta}{i.Position} {Fore.medium_violet_red}{i.Number}{Style.reset}\n"
				helpText+=msg
			print(helpText)
			whichDpts=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which department indexes? ",helpText=helpText,data="list")
			if whichDpts in [None,]:
				return
			elif whichDpts in ['d',[]]:
				whichDpts=[i.dptId for i in dpts]
			else:
				try:
					tmp=[]
					for i in whichDpts:
						try:
							tmp.append(dpts[int(i)].dptId)
						except Exception as e:
							print(e)
					whichDpts=tmp
				except Exception as e:
					print(e)
			for num,i in enumerate(RS):
				dpt=session.query(Department).filter(Department.dptId==i.dptId).first()
				if dpt.dptId in whichDpts:
					selectedPerson=session.query(Roster).filter(Roster.RoId==i.RoId).first()
					if not selectedPerson:
						continue
					if dpt:
						dptName=f"{dpt.Name}.{dpt.Position} - {dpt.Number}"
					else:
						dptName=f"N/A - N/A"
					if i.ShiftStart.hour >= 12:
						if i.ShiftStart.hour >= 12:
							dayEnd=f"{Style.bold}After 12PM "
					else:
						dayEnd=f'{Style.dim}Before 12PM '
						if i.ShiftStart.hour == 0:
							yesterday=datetime(i.ShiftStart.year,i.ShiftStart.month,i.ShiftStart.day)-timedelta(days=1)
							dayEnd+=f'{Fore.light_cyan}(Might Be {yesterday.strftime("%A")})'
					msg=f"""{dayEnd}{Fore.grey_50}{i.ShiftStart.strftime("%A")} of {Fore.grey_70}Week {i.ShiftStart.strftime("%W")}|{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {rsCt} -> {Fore.cyan}{selectedPerson.LastName},{Fore.light_magenta}{selectedPerson.FirstName} [{Fore.light_yellow}{dptName}{Fore.light_magenta}] - {Fore.light_green}SS({i.ShiftStart})/{Fore.light_red}SE({i.ShiftEnd})/{Fore.light_yellow}LS({i.ShiftLunchStart})/{Fore.dark_goldenrod}LE({i.ShiftLunchEnd}){self.shiftDuration_wo_lunch(i)}{Style.reset}"""
					#msg=f'''{num}/{num+1} of {rsCt} -> {selectedPerson.LastName},{selectedPerson.FirstName} [{dptName}] - SS({i.ShiftStart})/SE({i.ShiftEnd})/LS({i.ShiftLunchStart})/LE({i.ShiftLunchEnd})'''
					print(msg)
					totalplp+=1
					if dptName not in dptShow:
						dptShow.append(dptName)
			print(f'''Showing {totalplp} individuals for {','.join(dptShow)} Departments.''')
		self.legend()

	def shiftDuration_wo_lunch(self,RS):
		#{self.shiftDuration_wo_lunch(i)}
		shift_duration=RS.ShiftEnd-RS.ShiftStart
		total=timedelta(seconds=0)
		total_lunch=timedelta(seconds=0)
		with Session(ENGINE) as session:
			rss=session.query(RosterShift).filter(RosterShift.RoId==RS.RoId).all()
			for i in rss:
				total+=(i.ShiftEnd-i.ShiftStart)
				try:
					total_lunch+=(i.ShiftLunchEnd-i.ShiftLunchStart)
				except Exception as e:
					pass
		weekly_hours=total-total_lunch
		weekly_hours=f'{weekly_hours.total_seconds()/60/60} Hours'
		try:
			lunch_duration=RS.ShiftLunchEnd-RS.ShiftLunchStart
			return f'''{Fore.light_steel_blue}\n\tShift Duration: {Fore.orange_red_1}{shift_duration-lunch_duration}\n\t{Fore.light_steel_blue}Lunch Duration: {Fore.orange_red_1}{lunch_duration}\n\t{Fore.light_steel_blue}Weekly: {Fore.orange_red_1}{weekly_hours}{Fore.light_yellow}'''
		except Exception as e:
			return f'''{Fore.light_steel_blue}\n\tShift Duration: {Fore.orange_red_1}{shift_duration}\n\t{Fore.light_steel_blue}Lunch Duration: {Fore.orange_red_1}No Lunch\n\t{Fore.light_steel_blue}Weekly: {Fore.orange_red_1}{weekly_hours}{Fore.light_yellow}'''


	def rmRosterShift(self):
		with Session(ENGINE) as session:
			while True:
				whoSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Who are you searching?",helpText="firstname/lastname",data="string")
				if whoSearch in [None,]:
					return
				elif whoSearch in ['d',]:
					who=session.query(Roster).order_by(Roster.LastName).all()
				else:
					who=session.query(Roster).filter(or_(Roster.FirstName.icontains(whoSearch),Roster.LastName.icontains(whoSearch))).order_by(Roster.LastName.asc()).all()
				whoCt=len(who)
				if whoCt == 0:
					print("There is no one by that name")
					continue
				for num,i in enumerate(who):
					msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {whoCt} -> {Fore.cyan}{i.LastName},{Fore.light_magenta}{i.FirstName}{Style.reset}"""
					print(msg)
				which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left of the screen",data="integer")
				if which in [None,]:
					return
				elif which in ['d']:
					which=0
				selectedPerson=who[which]
				RS=session.query(RosterShift).filter(RosterShift.RoId==selectedPerson.RoId).order_by(RosterShift.ShiftStart.asc()).all()
				rsCt=len(RS)
				if rsCt == 0:
					print("No Shifts scheduled")
					return
				for num,i in enumerate(RS):
					dpt=session.query(Department).filter(Department.dptId==i.dptId).first()
					if dpt:
						dptName=f"{dpt.Name}.{dpt.Position} - {dpt.Number}"
					else:
						dptName=f"N/A - N/A"
					if i.ShiftStart.hour >= 12:
						if i.ShiftStart.hour >= 12:
							dayEnd=f"{Style.bold}After 12PM "
					else:
						dayEnd=f'{Style.dim}Before 12PM '
						if i.ShiftStart.hour == 0:
							yesterday=datetime(i.ShiftStart.year,i.ShiftStart.month,i.ShiftStart.day)-timedelta(days=1)
							dayEnd+=f'{Fore.light_cyan}(Might Be {yesterday.strftime("%A")})'
					msg=f"""{dayEnd}{Fore.grey_50}{i.ShiftStart.strftime("%A")} of {Fore.grey_70}Week {i.ShiftStart.strftime("%W")}|{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {rsCt} -> {Fore.cyan}{selectedPerson.LastName},{Fore.light_magenta}{selectedPerson.FirstName} [{Fore.light_yellow}{dptName}{Fore.light_magenta}] - {Fore.light_green}SS({i.ShiftStart})/{Fore.light_red}SE({i.ShiftEnd})/{Fore.light_yellow}LS({i.ShiftLunchStart})/{Fore.dark_goldenrod}LE({i.ShiftLunchEnd}){self.shiftDuration_wo_lunch(i)}{Style.reset}"""
					print(msg)
				which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left of the screen",data="integer")
				if which in [None,]:
					return
				elif which in ['d']:
					which=0
				selectedShift=RS[which]
				session.delete(selectedShift)
				session.commit()
				session.flush()
				break


	def saPerson(self):
		with Session(ENGINE) as session:
			while True:
				whoSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Who are you searching?",helpText="firstname/lastname",data="string")
				if whoSearch in [None,]:
					return
				elif whoSearch in ['d',]:
					who=session.query(Roster).order_by(Roster.LastName).all()
				else:
					who=session.query(Roster).filter(or_(Roster.FirstName.icontains(whoSearch),Roster.LastName.icontains(whoSearch))).order_by(Roster.LastName.asc()).all()
				whoCt=len(who)
				if whoCt == 0:
					print("There is no one by that name")
					continue
				for num,i in enumerate(who):
					msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {whoCt} -> {Fore.cyan}{i.LastName},{Fore.light_magenta}{i.FirstName}{Style.reset}"""
					print(msg)

	def rmPerson(self):
		with Session(ENGINE) as session:
			while True:
				whoSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="Who are you removing?",helpText="firstname/lastname",data="string")
				if whoSearch in [None,]:
					return
				elif whoSearch in ['d',]:
					who=session.query(Roster).order_by(Roster.LastName).all()
				else:
					who=session.query(Roster).filter(or_(Roster.FirstName.icontains(whoSearch),Roster.LastName.icontains(whoSearch))).order_by(Roster.LastName.asc()).all()
				whoCt=len(who)
				if whoCt == 0:
					print("There is no one by that name")
					continue
				for num,i in enumerate(who):
					msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} {Fore.orange_red_1}of {whoCt} -> {Fore.cyan}{i.LastName},{Fore.light_magenta}{i.FirstName}{Style.reset}"""
					print(msg)
				which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left of the screen",data="integer")
				if which in [None,]:
					return
				elif which in ['d']:
					which=0
				selectedPerson=who[which]
				session.delete(selectedPerson)
				session.commit()
				session.flush()
				break


	def saDepartment(self):
		with Session(ENGINE) as session:
			while True:
				whoSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What Department are you searching?",helpText="Name/Position/Number",data="string")
				if whoSearch in [None,]:
					return
				elif whoSearch in ['d',]:
					who=session.query(Department).order_by(Department.Name)
				else:
					who=session.query(Department).filter(or_(Department.Position.icontains(whoSearch),Department.Name.icontains(whoSearch)))
					try:
						whoSearchInteger=int(eval(whoSearch))
						who=who.filter(or_(Department.Number==whoSearchInteger))
					except Exception as e:
						print(e)
						try:
							whoSearchInteger=int(whoSearch)
							who=who.filter(or_(Department.Number==whoSearchInteger))
						except Exception as ee:
							print(ee)

				who=who.all()
				whoCt=len(who)
				if whoCt == 0:
					print("There is no one by that name")
					continue
				for num,i in enumerate(who):
					#msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{whoCt} -> {Fore.cyan}{i.Name} {Fore.light_magenta}{i.Number}{Style.reset}"""
					msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{whoCt} -> {Fore.cyan}{i.Name}.{i.Position} {Fore.light_magenta}{i.Number}{Style.reset}"""
					print(msg)

	def rmDepartment(self):
		with Session(ENGINE) as session:
			while True:
				whoSearch=Prompt.__init2__(None,func=FormBuilderMkText,ptext="what department are you removing?",helpText="name",data="string")
				if whoSearch in [None,]:
					return
				elif whoSearch in ['d',]:
					who=session.query(Department).order_by(Department.Name).all()
				else:
					who=session.query(Department).filter(or_(Department.Position.icontains(whoSearch),Department.Name.icontains(whoSearch))).order_by(Department.Name.asc()).all()
				whoCt=len(who)
				if whoCt == 0:
					print("There is no dptment by that name")
					continue
				for num,i in enumerate(who):
					msg=f"""{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{whoCt} -> {Fore.cyan}{i.Name}.{i.Position} {Fore.light_magenta}{i.Number}{Style.reset}"""
					print(msg)
				which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?",helpText="the number farthest to the left of the screen",data="integer")
				if which in [None,]:
					return
				elif which in ['d']:
					which=0
				selectedDepartment=who[which]
				session.delete(selectedDepartment)
				session.commit()
				session.flush()
				break

	def addDepartment(self):
		with Session(ENGINE) as session:
			excludes=['dptId',]
			fields={str(i.name):{'default':None,'type':str(i.type)} for i in Department.__table__.columns if str(i.name) not in excludes}
			fields['DTOE']['type']='datetime-'
			fd=FormBuilder(data=fields)
			department=Department(**fd)
			session.add(department)
			session.commit()
			session.flush()
			session.refresh(department)
			print(department)

	def addPerson(self):
		with Session(ENGINE) as session:
			excludes=['RoId',]
			fields={str(i.name):{'default':None,'type':str(i.type)} for i in Roster.__table__.columns if str(i.name) not in excludes}
			fields['DTOE']['type']='datetime-'
			fd=FormBuilder(data=fields)
			person=Roster(**fd)
			session.add(person)
			session.commit()
			session.flush()
			session.refresh(person)
			print(person)
	def __init__(self):
		fieldname='Menu'
		mode='Roster'
		h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
		menutext=f'''
{Fore.cyan}'ap','ad person','add person','add personnel','ad personnl' {Fore.light_red}-{Fore.orange_red_1} add a person to Roster table, checking to ensure that name is not duplicated before adding{Style.reset}
{Fore.cyan}'rp','rm person','rmperson','del person','delperson','del taco','deltaco' {Fore.light_red}-{Fore.orange_red_1} remove a person{Style.reset}
{Fore.cyan}'sap','sa person','saperson','sa person','walk the planck' {Fore.light_red}-{Fore.orange_red_1} search persons{Style.reset}

{Fore.cyan}'ad','ad dpt','add department','add dpt','addpt' {Fore.light_red}-{Fore.orange_red_1} add a department to tables{Style.reset}
{Fore.cyan}'rd','rm department','rmdpt','del dpt','deldpt'{Fore.light_red}-{Fore.orange_red_1} remove a department{Style.reset}
{Fore.cyan}'sad','sa department','sadpt','sa dpt' {Fore.light_red}-{Fore.orange_red_1} search department{Style.reset}

{Fore.cyan}'rars','rm roster shift'{Fore.light_red}-{Fore.orange_red_1} delete a scheduled day{Style.reset}
{Fore.cyan}'whos here','personel','prsnl','today','tdy'{Fore.light_red}-{Fore.orange_red_1} show who's here today{Style.reset}
{Fore.cyan}'whos here tmro','future 1day','prsnl tmro','tmro','tomorrow'{Fore.light_red}-{Fore.orange_red_1} show who's here tomorrow{Style.reset}
{Fore.cyan}'sars','sa rostershift'{Fore.light_red}-{Fore.orange_red_1} search RosterShift{Style.reset}
{Fore.cyan}'cars','ca rostershift','clear all rostershift'{Fore.light_red}-{Fore.orange_red_1}clear all schedules{Style.reset}
{Fore.cyan}'cad','ca dpt','clear all departments'{Fore.light_red}-{Fore.orange_red_1}clear all dpts{Style.reset}
{Fore.cyan}'cap','ca personnl','clear all people'{Fore.light_red}-{Fore.orange_red_1}clear all people{Style.reset}
{Fore.cyan}'ars','ad roster shift','add roster shift','adrstrshft' {Fore.light_red}-{Fore.orange_red_1} using Roster and Departments tables, update the RosterShift table with available shift data{Style.reset}
{Fore.cyan}'lars','list all roster shift','ls * rs' {Fore.light_red}-{Fore.orange_red_1} list ALL RosterShift's/Schedules{Style.reset}
{Fore.light_magenta}fromblog{Fore.light_yellow}clear current rostershift and load from blog{Style.reset}
		'''
		while True:
			try:
				cmd=Prompt.__init2__(self,func=FormBuilderMkText,ptext=f"{h}Do what?",helpText=menutext,data="string")
				if cmd in [None,]:
					return
				elif cmd.lower() in ['d',]:
					print(menutext)
				elif cmd.lower() in ['ap','ad person','add person','add personnel','ad personnl']:
					self.addPerson()
				elif cmd.lower() in ['rp','rm person','rmperson','del person','delperson','del taco','deltaco']:
					self.rmPerson()
				elif cmd.lower() in ['sap','sa person','saperson','sa person','walk the planck']:
					self.saPerson()	
				elif cmd.lower() in ['ad','ad dpt','add department','add dpt','addpt']:
					self.addDepartment()
				elif cmd.lower() in ['rd','rm department','rmdpt','del dpt','deldpt']:
					self.rmDepartment()
				elif cmd.lower() in ['sad','sa department','sadpt','sa dpt']:
					self.saDepartment()
				elif cmd.lower() in ['ars','ad roster shift','add roster shift','adrstrshft']:
					self.addShift()
				elif cmd.lower() in ['sars','sa roster shift']:
					self.saRosterShift()
				elif cmd.lower() in ['cars','ca rostershift','clear all rostershift']:
					self.caRosterShift()
				elif cmd.lower() in ['cad','ca dpt','clear all departments']:
					self.caDepartments()
				elif cmd.lower() in ['cap','ca personnl','clear all people']:
					self.caPeople()
				elif cmd.lower() in ['lars','list all roster shift','ls * rs']:
					self.laRosterShift()
				elif cmd.lower() in ['whos here','personel','prsnl','prsnl','today','tdy']:
					self.whosHere()
				elif cmd.lower() in ['whos here tmro','future 1day','prsnl tmro','tmro','tomorrow']:
					self.whosHereTomorrow()
				elif cmd.lower() in ['rars','rm roster shift']:
					self.rmRosterShift()
				elif cmd.lower() in ['fromblog',]:
					self.fromBlog()
				elif cmd.lower() in ['fromexcel','fe']:
					self.fromEXCEL()
				elif cmd.lower() in ['drangetest',]:
					drange=Prompt.__init2__(None,func=FormBuilderMkText,ptext="schedule format text:",helpText="month/day/year@hh:mm(FROM)-hh:mm(TO)",data="datetime~")
					print(drange)
				else:
					print(menutext)
			except Exception as e:
				print(e)