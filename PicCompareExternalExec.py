
from PIL import Image
import imagehash


def count(path):

	return imagehash.average_hash(Image.open( path ),512)

def main(argv):
	# print str(count())
	return str(count(argv[0])) == str(count(argv[1]))
	# return argv
	# print argv

if __name__ == "__main__":
	import sys
	print main(sys.argv[1:])
	## get last 2 argv to run def


#exec line##############
# x = subprocess.check_output(["python", "D:\\Kialiam\\Work\\Personal\\Script\\ScriptBase\\PicCompareExternalExec.py", path , path2])  ## as argv, except python for exec , 1st: ScriptPath , 2nd: two argv for Compare
# print x
#exec line##############


