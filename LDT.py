
import os,sys,getpass,time



class superDict(dict):
	# AutoVivifications
	"""Implementation of perl's autovivification feature."""
	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			value = self[item] = type(self)()
			return value

def read_in_chunks(filePath, chunk_size=1024*1024):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1M
    You can set your own chunk size 
    """
    file_object = open(filePath)
    while True:
        chunk_data = file_object.read(chunk_size)
        if not chunk_data:
            break
        yield chunk_data

def copyfile(source,dest):

	dst = open(dest,'wb')
	src = open(source,'rb')
	# with open(source,'rb') as f:
	# 	print "read!"
		# for line in f:
	 # 		dst.write(line)

	dst.write(src.read() )

	dst.close()
	src.close()

def reRange(Num1,Num2,Num3,Num4,Num5 = None):
	
	if Num5==None:
		oldRangeMin = float(Num1)
		oldRangeMax = float(Num2)
		newRangeMin = float(Num3)
		newRangeMax = float(Num4)

		Key = ( newRangeMax - newRangeMin ) / ( oldRangeMax - oldRangeMin )	
		# return string ( value - oldRangeMin ) * Key + newRangeMin
		# can be used like: exec "answer = "+ 
		return "(%s - %s) * %s + %s" %("value",oldRangeMin,Key,newRangeMin)

	else:
		value       = float(Num1)
		oldRangeMin = float(Num2)
		oldRangeMax = float(Num3)
		newRangeMin = float(Num4)
		newRangeMax = float(Num5)

		Key = ( newRangeMax - newRangeMin ) / ( oldRangeMax - oldRangeMin )	
		##          range                key     offset
		return ( value - oldRangeMin ) * Key + newRangeMin

def ProxyPath(Address):

	if Address == "Desktop":
		return "C:\Users\Liam\Desktop"
	elif Address == "TestPath":
		return "D:\Kialiam\Work\Personal\Test"
	else:
		return "Just Desktop or TestPath"

def DirTree( Dir , level = 0 , Key = "" ):
	if level == 0:
		global Dict
		Dict = superDict() 
		global local
		local = "/"
		global basePath
		basePath = Dir
		ischinesse = False

	if os.path.isdir( Dir ):

		Child = os.listdir( Dir ) 

	else:
		Child = []                                

	for x in Child:

		##########--if Filename chinese--##########
		try:										#
			x.encode('utf-8')						#
			ischinesse = False						#
		except:										#
			ischinesse = True						#	

		if ischinesse == False:						#

		###########################################			
			# print level
			# print x
			# print Dir + "/%s" %x

		####-----------------if it is Folder-----------------------#################

			if os.path.isdir( Dir + "/%s" %x ):																				

				# print "is dir"

				exec "Dict[basePath]%s[%s]" %( Key ,'x')

				NewDir = Dir +"/%s" %x

				#########------repeat the action to nect level for child of folder--------------#########

				DirTree( NewDir  , level + 1 , Key + '["%s"]' %x )        							#

				#########################################################################################
			
			else:
		######--------------if it is file------------------------###################

				# print Key
				exec "Temp = Dict[basePath]%s[%s]" %( Key , 'local' )
				# print "Temp"
				# print x

				if len( Temp ) == 0:
					exec "Dict[basePath]%s[%s] = %s" %( Key , 'local' , '[x]')
					# print "yes"
				else:
					exec "Dict[basePath]%s[%s].append( %s )" %( Key , 'local' , 'x')
					# print "no"

	return Dict

def FilterFileInTree( Dict , ext ,  level = 0 , path = '' , keys = '' ):

	if level == 0:

		################################
		# Dict = DirTree( Dict )
		################################
		global mainDict
		mainDict = Dict
		global base
		base = mainDict.keys()[0]
		Dict = mainDict[base].keys()
		path = mainDict.keys()[0]
		global FileList
		FileList = []

	for key in Dict:
		if os.path.isdir( path + "/" + key ):
			if key != "/":

				exec "Dict = mainDict[base]%s%s.keys()" %(keys,'[key]')

				#######################################################################################

				FilterAllFile( Dict , ext , level +1 , path + "/" + key , keys + "['"+key+"']" )	 		#

				#######################################################################################

			else:
				exec "Dict = mainDict[base]%s%s" %(keys,'[key]')
				for value in Dict:
					if type(ext) == str:
						if ext in value:
							FileList.append( path + "/" + value )
					else:
						for e in ext:
							if e in value:
								FileList.append( path + "/" + value )

def FileWith( Dir , ext ):

	FileList = []
	Target = os.listdir( Dir )
	for value in Target:
		if type(ext) == str:
			if ext in value:
				FileList.append( Dir + "/" + value )
		else:
			for e in ext:
				if e in value:
					FileList.append( Dir + "/" + value )

	return FileList	

def AvoidExistsFolder( Folder ):

	i = True
	num = 0

	if len(Folder.split("(")[-1]) == 2:
		Folder = Folder.split("(",-1)[0]

	TempF = Folder

	while i == True:
		if os.path.exists( Folder ):
			i = True
			num += 1
			Folder = TempF+"(%s)" %str(num)
		else:
			i = False
			Folder = Folder

	return Folder

# def AvoidExistsObj( Obj , tail = "None"):

# 	import maya.cmds as cmds
# 	import string

# 	i = True
# 	num = 0 if tail != "alpha" else 1

# 	TempF = Obj

# 	while i == True:
# 		if cmds.objExists( Obj ):
# 			i = True
# 			num += 1
# 			if tail == "alpha" or tail == "None":
# 				Obj = TempF+"_%.2d" %num


# 			elif tail == "digit":

# 				Alpha = list(string.uppercase)
# 				NUMBER = num
# 				stringdigit = "%s"%(Alpha[NUMBER%26-1])

# 				while NUMBER>26:
# 					# when it is ZZ, (26,26) , count by math it will add 1 at front, but make a exception and wont become AZZ after ZY
# 					if not (NUMBER/26 == 1 and num%26 == 0):
						
# 						# it add one Alpha when it is Z indeed of A (after Z), so when it still Z, minus one to delay it 
# 						if not (NUMBER/26 != 1 and NUMBER%26 == 0):
# 							stringdigit =  Alpha[(NUMBER/26%26)-1] + stringdigit   
# 						else:
# 							stringdigit = Alpha[(NUMBER/26%26)-2] + stringdigit
							
# 					NUMBER = NUMBER/26

# 				#if NUMBER > 26

# 				Obj = TempF+"_%s" %stringdigit
# 			else:
# 				None
# 		else:
# 			i = False
# 			Obj = Obj

# 	# return Obj

def AvoidExistsObj( Obj , tail = "None"):

	import maya.cmds as cmds
	import string

	i = True
	num = 1 if tail != "digit" else 1
	NUMBER = num
	TempF = Obj

	if tail == "digit":
		while i == True:
			Obj = TempF + "_%.2d" %num 
			if cmds.objExists( Obj ):
				i = True
				num += 1
			else:
				i = False
				Obj = TempF + "_%.2d" %num 
				return Obj
				
	elif tail == "alpha" or tail == "None":
		Alpha = list(string.uppercase)
		while i == True:
			stringdigit = "%s"%(Alpha[NUMBER%26-1])
			if cmds.objExists( Obj +"_%s" %stringdigit ):
				num += 1
				NUMBER = num
				i = True
				while NUMBER>26:
					## when it is ZZ, (26,26) , count by math it will add 1 at front, but make a exception and wont become AZZ after ZY
					if not (NUMBER/26 == 1 and num%26 == 0):
						
						## it add one Alpha when it is Z indeed of A (after Z), so when it still Z, minus one to delay it 
						if not (NUMBER/26 != 1 and NUMBER%26 == 0):
							stringdigit =  Alpha[(NUMBER/26%26)-1] + stringdigit   
						else:
							stringdigit = Alpha[(NUMBER/26%26)-2] + stringdigit
							
					NUMBER = NUMBER/26
			else:
				i = False
				Obj = TempF+"_%s" %stringdigit
				return Obj
	else:
		print "argument wrong"


def rename(path,old,new,mount = 1):

	Path = path
	Num = 0

	if os.path.isdir(Path):

		Items = os.listdir(Path)

		for name in Items:
			if old in name:
				NewName = name.replace(old,new,mount)
				os.rename(Path+"/"+name,Path+"/"+NewName)
				Num += 1

		if Num == 0:
			print "No Name is matched!!"
		else:
			print str(Num)+" object have been renamed"

	else:
		print "No Path exists!!"

def ConnectionTree( base , level = 0 , Key = "" ):

	import maya.cmds as cmds

	if level == 0:
		global Dict
		Dict = superDict() 
		global basePath
		base = base if type(base) is not str else [base]
		basePath = base
		global framedEle
		framedEle = base

	for b in base:
		if cmds.objExists( b ):
			Key = "['%s']"%b if level==0 else Key
			Child = []
			# [Child.append(x) for x in cmds.listConnections( base , d = False) if x not in framedEle x]

			try:
				## listConnections may cause "NoneType" return value issue ...
				for x in cmds.listConnections( b , d = False):
					
					if x not in framedEle:
						framedEle.append( x )
						# print str(level) + " "+x
						Child.append(x)
			except:
				pass

			# print level

		else:
			Child = []
			print "no Connections"                                

		for x in Child:
			####-----------------if it is exists-----------------------#################

			if cmds.objExists( x ):																				

				# print "is dir"

				exec "Dict%s[%s]" %( Key ,'x') in globals(), locals()

				NewDir = [x]

				#########------repeat the action to nect level for child of Node--------------#########

				ConnectionTree( NewDir  , level + 1 , Key + '["%s"]' %x )        							#

				#########################################################################################
				# print 1

	return Dict
	print "Obj Connections Dictionary Done !"
	
def ListTreeKeys(Dict, path = "" , level = 0):

	if level == 0:
		global base
		base = Dict
		global AllObj
		AllObj = []
		global Node
		Node = []
		keys = Dict.keys()
	else:
		keys = Dict


	for key in keys:

		exec "List = base%s['%s'].keys()"%(path,key) 
		
		Node.append(key)

		ListTreeKeys( List , path + "['%s']"%key , level +1 ) 

	return Node

def findStrCaseIndex( string , Case = "Upper" ):

	index = []
	Alpha = [x for x in string]
	Num = len(Alpha)
	for x,y in zip(Alpha,range(0,Num)):
		if Case == "Upper":
			if x.isupper():
				index.append(y)
		else:
			if x.islower():
				index.append(y)

	return index
