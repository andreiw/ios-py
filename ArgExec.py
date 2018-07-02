import sys
import console

#
# Example use (e.g. in a QR code):
# pythonista://ios-py/ArgExec?action=run&args="console.hud_alert(\"hi there\")"
#
def main():
	if len(sys.argv) == 1:
		console.hud_alert("nothing to do", "error")
		return
	
	arg = sys.argv[1]
	print("gonna execute '%s'" % arg)
	try:
		exec(arg)
	except:
		print("couldn't exec: '%s': %s" % (arg, sys.exc_info()[0]))
		console.hud_alert("error executing", "error")
		return
		
	console.hud_alert("all done", "success")

if __name__ == '__main__':
	main()
