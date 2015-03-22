import sys
from nltk.util import ngrams


class Record:
	def __init__(self,id,score,type):
		self.id = id
		self.score = score
		self.type = type

recordList = []
inputList = []
lUser = []
lTopic = []
lQues = []
lBoard = []

wordDic = {}
triDic = {}
biDic = {}
idContentDic = {}

#commandList.append(1)

def addCmd(cmdArray):
	
	#ADD user u1 1.0 Adam D’Angelo
	
	currArray = []
	id = cmdArray[2]
	score = float(cmdArray[3])
	content = ' '.join(cmdArray[4:])
	content = content.lower()

	idContentDic[id] = content
	recordObj = Record(id,score,cmdArray[1])
	recordList.append(recordObj)

	for token in cmdArray[4:]:
		token = token.lower()
		listId = []
		listId.append(recordObj)
		
		if(token in wordDic):
		  listId = wordDic[token]
		  if recordObj not in listId:
		  	listId.append(recordObj)

		wordDic[token] = listId

	for i in range(0,len(content)-2):
		tg = content[i]+content[i+1]+content[i+2]
		kvP = {}
		if(tg in triDic):
			kvP = triDic[tg]

		lst = []
		if id in kvP:
			lst = kvP[id]
		lst.append(i)
		kvP[id] = lst

		triDic[tg] = kvP
			
	'''
	for i in range(0,len(token)-1):
			tg = token[i]+token[i+1]
			if(tg not in biDic):
				lst = []
			else:
				lst = biDic[tg]

			lst.append(token)
			biDic[tg] = lst
	'''

	if(cmdArray[1]=='user'):
		currArray = lUser
	elif(cmdArray[1]=='topic'):
		currArray = lTopic
	elif(cmdArray[1]=='question'):
		currArray = lQues
	else:
		currArray = lBoard

	currArray.append(recordObj)




def queryCmd(command):

	noOfResults = int(command[1])
	query = ' '.join(command[2:])
	query = query.lower()

	if(query in wordDic):
		lst = wordDic[query]
		lst.sort(key=lambda x: x.score, reverse=True)
		output = ' '
		for obj in lst:
			output = output + obj.id + ' '
		print(output.strip())
	else:
		kvP = {}
		glb = []
		isPresent = True

		for i in range(0,len(query)-2):
			tg = query[i]+query[i+1]+query[i+2]
			if(tg in triDic):
				print(tg)
				print(triDic[tg])
				print('--')
				kvP = triDic[tg]
				localLst = []
				for k,v in kvP.items():
					if(i==0):
						glb.append(k)
					else:
						localLst.append(k)
				if(i!=0):
					glb = list(set(glb).intersection(localLst))
			else:
				print('')
				isPresent = False
				return

		for id in glb:
			if(query not in idContentDic[id]):
				glb.remove(id)
		output = ''
		for id in glb:
			output = output + id + ' '
		print(output.strip())


def delCmd(command):
	id = command[1]
	content = idContentDic[id]
	tokens = content.split(' ')
	for token in tokens:
		lst = wordDic[token.lower()]
		lst.remove(id)
		wordDic[token.lower()] = lst

	'''
	for i in range(0,len(query)-2):
			tg = query[i]+query[i+1]+query[i+2]
			if(tg in triDic):
	'''	



def wQuery(command):
	print(inputList)

def printAll():
	for obj in recordList:
		print('-------')
		print(obj.score)
		print(obj.id)
		print(obj.type)

totalline = input()

for cmd in range(0,int(totalline)):
	inputList.append(input())

for command in inputList:
	command = command.split(' ')
	if(command[0]=='ADD'):
		addCmd(command)
	elif(command[0]=='QUERY'):
		queryCmd(command)
	elif(command[0]=='DEL'):
		delCmd(command)
	else:
		wQuery(command)

#printAll()