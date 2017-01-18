

### ------- picture compare tool----------------------- ########


from PIL import Image
import imagehash


def count(path):

	return imagehash.average_hash(Image.open( path ),512)
	## return to numberic , 512 , the number higher means compare more detail

def main(argv):

	return str(count(argv[0])) == str(count(argv[1]))
	### return bool of comparation of two pictures's hash number


if __name__ == "__main__":
	import sys
	print main(sys.argv[1:])
	## get last 2 argv to run def
	## there have 3 arguement in sys.argv


# ------ exec line ---------- #####

## run the script external and just return output
## as argv, except python for exec , 1st: ScriptPath , 2nd: two argv for Compare

# variable = subprocess.check_output(["python", "D:\\..\\Script\\PicCompareExternalExec.py", path , path2]) 

#print variable 
#>>> True or False (same or difference picture)

# ------ exec line ---------- #####


