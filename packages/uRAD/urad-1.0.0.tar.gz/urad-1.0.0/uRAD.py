#!/usr/bin/env python3

#-------------------------------------------------------------------------------------------//
#											
# Description: Python Script that read raw data from uRAD RADAR system, 
#		 when only Continuous Mode operation is Considered.	
#
# Author: Queto Jenkins
# Modified by: Kananelo Chabeli
# Modified Date: 15/ 11/ 2024 
#-------------------------------------------------------------------------------------------//

 #will allow to run python scripts without specifying "python3 script"

#-------------------------------------------------------------------------------------------//
#							Imports
#-------------------------------------------------------------------------------------------//

import lib.uRAD_firmware_lib as uRAD_USB_SDK11	# import uRAD libray
import serial	 #for serial communication with the uRAD ( Kananelo)
from time import time, sleep

import argparse #for reading and validating command line arguments


#-------------------------------------------------------------------------------------------//
#				Read Command Line Arguments (Kananeli
#-------------------------------------------------------------------------------------------//

#wrap everything inside the main function, which serves as the entry point

__version__ = "1.0.0" #version number

def main():

	# Initialize the parser
	parser = argparse.ArgumentParser(description="Reads raw RADAR data from the uRAD RADAR system and saves it in a specified filename for further processing")

	parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"  # Automatically display the script name and version
    )
	# Add the optional --filename/-f argument
	parser.add_argument(
	    "-f", "--filename", 
	    type=str, 
	    help="Specifies the filename where the raw data is saved. If missing, the data is saved to 'outputIQ.txt', in the current directory"
	)

	# Add the required --port/-p argument
	parser.add_argument(
	    "-p", "--port", 
	    type=str, 
	    required=True,  # Makes the argument mandatory
	    help="Specifies the port name where the uRAD is connected. This is required argument and must always be specified."
	)

	# Add '-v', or '--verbose' to print the process as we code executes.
	parser.add_argument(
	    "-v", "--verbose", 
	    action="store_true",  # Makes it a flag that defaults to False
	    help="Enable verbose output which prints the progress to the console as the script runs."
	)

	parser.add_argument(
		"-m","--mode",
		type=int,
		required=False,
		help="Specifies the mode of the uRAD Radar. Must be an integer between 1 and 4 (see uRAD manual for more details). If missing, it defaults to 1(CW Mode)"
		)

	parser.add_argument('-c','--centre-frequency',type=int,
		required=False, 
		help='Specifies the carrier frequency for CW mode or start frequency of modes 2-4 of the uRAD (see uRAD manual for more details). Must be an integer from 5-245 for mode 1 and 5-195 for other modes. If missing, it defaults to 5'
		)


	parser.add_argument('-b','--bandwidth',type=int,required=False,
		help="Specifies the bandwidth of modes 2-4 of the uRAD. It is meaningless for mode 1,"+
		"and therefore ignored if given. If missing, it defaults to 240( maximum BW) for other modes",
		)

	parser.add_argument('-s','--sample-number',type=int,required=False,
		help = 'Specifies the number of samples that uRAD takes of the reflected waves to calculate distnace and velocity(see manual for more details).'+
		'Must be values 50-200. If missing, it defaults to 200(Updated firmware takes upto 800)'
		)

	parser.add_argument('-t','--target-number',type = int, required=False,
		help = "Specifies the number of targets that the uRAD can detect simulteneously. Must be integer between 1 and 5. If missing, it defaults to 1"
		)

	parser.add_argument('-r','--maximum-range',type=int, 
		required=False,
		help="Specifies the maximum range for modes 2-4, and maximum velocity for mode 1 that uRAD can detect.Must be an integer between 0 and 75 If missing, it defaults to 75"
		)

	parser.add_argument('-i','--moving-target-indicator',type=int,required=False,

		help="Specifies whether or not the moving target indicator should be activated( see manual for more details). Must be with 0 or 1. If missing, it defaults to 0"
		)

	parser.add_argument('-a', '--alpha', type = int, required=False,
		help = "Specifies the alpha parameter of CA-CFAR algorithm used to control sensitivity level of the uRAD(see manual for more details). Must be an integer between 3(high) and 25(low). If missing, it defaults to 10"
		)

	parser.add_argument('-S','--sensitivity', type  =int, required=False,
		help= "Specifies the sensitivity of the uRAD. Must be an integer between 0 and 4(see uRAD manual for more details). If missing, it defaults to 0")

	parser.add_argument('-T','--test',action='store_true', help='Runs the scripts only for to test the connection between PC and the uRAD.')

	args = parser.parse_args()

	# Access and validate arguments
	filename = args.filename  # This is None if not specified, the script will save file to 'IQ.txt'
	port = args.port  # This must be specified due to required=T
	verbose = args.verbose #Boolean Flag Verbose


	#-------------------------------------------------------------------------------------------------//
	#				Variable Initialization
	#-------------------------------------------------------------------------------------------------//

	if args.test:
		print('Testing the connection to uRAD...',flush = True)

	if verbose:
		print('Initializing parameters...',end = '', flush = True)
	# True if USB, False if UART
	usb_communication = True

	# Input Configuration Parameters - Defined in Chapter Two of the User Manual
	mode = 1 if args.mode is None else args.mode					# CW Mode
	f0 = 5	if args.centre_frequency is None else args.centre_frequency					# 24.125 GHz ????
	BW = 240 if args.bandwidth is None else args.bandwidth					# Irrelevant in CW Mode
	Ns = 200 if args.sample_number is None else args.sample_number					# 200 samples before Firmware Update - 800 after
	Ntar = 1 if args.target_number is None else args.target_number					# Doesn't apply as only raw data is desired, but would indicate one target
	Rmax = 75 if args.maximum_range is None else args.maximum_range					# Doesn't apply as only raw data is desired, Rmax is actually Vmax for CW mode
	MTI = 0	if args.moving_target_indicator is None else args.moving_target_indicator					# MTI mode disabled becuase CW only deals with moving targets
	Mth = 0	 if args.sensitivity is None else args.sensitivity					# Doesn't apply as only raw data is desired
	Alpha = 10	if args.alpha is None else args.alpha				# Doesn't apply to raw signals

	# Outputs from uRAD Requested - Only want raw IQ Data for Self Processing
	distance_true = False 		# Don't request distance information
	velocity_true = False		# Don't request velocity information
	SNR_true = False 			# Don't request Signal-to-Noise-Ratio information
	I_true = True 				# In-Phase Component (RAW data) requested
	Q_true = True 				# Quadrature Component (RAW data) requested
	movement_true = False 		# Doesn't apply as only raw data is desired - change this to true to see if its a movement detector

	# Serial Port configuration
	ser = serial.Serial()
	if (usb_communication):
		ser.port = port
		ser.baudrate = 1e6
	else:
		ser.port = port
		ser.baudrate = 115200

	# Sleep Time (seconds) between iterations
	timeSleep = 5e-3

	# Other serial parameters
	ser.bytesize = serial.EIGHTBITS
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE
	ser.timeout = 1

	# Method to correctly turn OFF and close uRAD
	def closeProgram():
		# switch OFF uRAD
		return_code = uRAD_USB_SDK11.turnOFF(ser)
		if (return_code != 0):
			exit()

	# Open serial port
	if verbose:
		print(f'done.\nOpening Serial port: {port} ...',end = '', flush = True)
	try:
		ser.open()
	except Exception as e: 
		print('\n',e) #Print error message, comment by Kananelo
		closeProgram()

	if verbose:
		print(f'done.\nOpening uRAD...', end = '', flush = True)
	# switch ON uRAD
	return_code = uRAD_USB_SDK11.turnON(ser)
	if (return_code != 0):
		print("Failed to open the uRAD") #Print error message, comment by Kananelo
		closeProgram()

	if (not usb_communication):
		sleep(timeSleep)

	if verbose:
		print(f'done.\nLoad Configuration parameters...', end = '', flush = True)
	# loadConfiguration uRAD
	return_code = uRAD_USB_SDK11.loadConfiguration(ser, mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth, Alpha, distance_true, velocity_true, SNR_true, I_true, Q_true, movement_true)
	if (return_code != 0):
		print("Failed to load the uRAD Configuration parameters") #print the error message, comment by Kananelo
		closeProgram()

	if (not usb_communication):
		sleep(timeSleep)

	if verbose:
		print('done.',flush=True)
	#read file name specified on command-line: by Kananelo
	if filename is not None:
		resultsFileName = filename
	else:
		resultsFileName = 'outputIQ.txt' #use defualt filename: (Queto)

	if not args.test:
		fileResults = open(resultsFileName, 'a')
	
	iterations = 0
	t_0 = time()


	#if run for testing, detect once, and terminate:
	if args.test:
		return_code, results, raw_results = uRAD_USB_SDK11.detection(ser)
		if return_code!=0:
			print('Failed to communicate with the uRAD.')

		else:
			print('communication status: OK.')	
		exit()
	
	# infinite detection loop
	while True:

		# target detection request
		return_code, results, raw_results = uRAD_USB_SDK11.detection(ser)
		if (return_code != 0):
			print('Failed to read the data') #proint error message, commented by Kananelo
			closeProgram()

		# Extract results from outputs
		I = raw_results[0]
		Q = raw_results[1]

		t_i = time()

		IQ_string = ''
		for index in range(len(I)):
			IQ_string += '%d ' % I[index]
		for index in range(len(Q)):
			IQ_string += '%d ' % Q[index]

		fileResults.write(IQ_string + '%1.3f\n' % t_i)

		iterations += 1
		if verbose:
			if (iterations > 100):
				print('Fs %1.2f Hz' % (iterations/(t_i-t_0)))

		if (not usb_communication):
			sleep(timeSleep)
			
if __name__ == '__main__':
	main()