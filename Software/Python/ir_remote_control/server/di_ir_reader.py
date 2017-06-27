#!/usr/bin/env python
from subprocess import Popen, PIPE, STDOUT, call
import time
import socket
import time
import sys
import signal
import os

call("sudo /etc/init.d/lirc stop", shell=True)
debug = 1

# class for exiting gracefully
# use as "with GracefullExiter as exiter:" and then keep on checking [exit_now]
class GracefullExiter:
    exit_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def __exit__(self, exc_type, exc_value, traceback):
        self.exit_now = True

        # if encountered exception
        if exc_type is not None:
            print(exc_type, exc_value, traceback)
            return False
        else:
            return True

    def __enter__(self):
        return self

    def exit_gracefully(self, signum, frame):
        self.exit_now = True


# Compare the key value which was read by the IR receiver with the fingerprints that we had recorded for each value
def compare_with_button(inp):
    found_flag=0
    keys={  0:"KEY_1",
            1:"KEY_2",
            2:"KEY_3",
            3:"KEY_4",
            4:"KEY_5",
            5:"KEY_6",
            6:"KEY_7",
            7:"KEY_8",
            8:"KEY_9",
            9:"KEY_0",
            10:"KEY_UP",
            11:"KEY_DOWN",
            12:"KEY_LEFT",
            13:"KEY_RIGHT",
            14:"KEY_OK",
            15:"KEY_H",
            16:"KEY_S",
            }

    key_map =[  #KEY_1
                [588,531,571,552,
                571,527,595,528,564,560,
                562,534,589,535,567,556,
                567,1650,564,1655,590,1654,
                571,1647,567,1651,594,1650,
                564,1656,569,1647,588,536,
                566,1652,593,1651,564,537,
                584,1656,570,527,595,529,
                563,560,563,1655,569,554,
                569,532,590,1651,564,533,
                589,1655,570,1647,568,1652,
                593],

                #KEY_2
                [564,538,585,534,
                568,556,566,531,592,532,
                570,554,568,530,592,532,
                561,1661,584,1656,568,1651,
                575,1644,590,1655,569,1654,
                561,1653,592,1654,570,1649,
                566,558,564,538,585,1655,
                569,1651,564,560,562,536,
                597,527,565,558,564,1660,
                565,1650,594,531,561,563,
                570,1648,567,1657,587,1654,
                571],

                #KEY_3
                [595,503,619,504,
                598,526,596,501,621,503,
                590,537,586,507,595,529,
                563,1655,620,1624,591,1628,
                596,1626,619,1622,592,1627,
                568,1650,595,1652,562,1651,
                564,560,563,1654,560,1657,
                588,535,567,554,569,528,
                594,528,564,559,564,1653,
                561,561,562,534,588,1660,
                566,1647,567,1651,594,1649,
                566],

                #KEY_4
                [564,534,588,536,
                567,557,595,503,624,500,
                567,556,567,530,593,532,
                570,1648,597,1648,597,1625,
                589,1625,620,1625,569,1649,
                566,1652,627,1618,562,536,
                617,507,565,1652,622,1623,
                593,504,622,501,587,537,
                565,532,591,1652,562,1657,
                568,555,567,530,597,1647,
                563,1655,590,1628,617,1628,
                566],

                #KEY_5
                [591,533,599,499,
                623,500,592,534,589,503,
                619,505,598,525,597,500,
                622,1623,592,1626,599,1624,
                621,1620,594,1624,600,1620,
                625,1623,592,1624,591,533,
                599,498,625,499,593,1625,
                620,1628,596,499,623,500,
                593,530,593,1625,589,1628,
                617,1631,593,501,622,502,
                590,1628,617,1629,596,1622,
                593],

                #KEY_6
                [591,530,562,561,
                561,536,587,536,566,557,
                566,531,591,532,570,554,
                573,1644,567,1651,592,1653,
                563,1654,571,1648,597,1647,
                567,1650,564,1654,591,533,
                569,1652,583,1657,568,1651,
                563,1656,589,535,568,1655,
                589,531,561,1657,589,536,
                565,559,564,534,588,536,
                566,1657,587,533,571,1648,
                597],

                #KEY_7
                [570,527,595,527,
                565,558,565,536,586,533,
                569,553,570,528,595,528,
                564,1655,590,1654,570,1649,
                567,1652,592,1653,562,1656,
                568,1655,591,1650,564,534,
                588,535,568,556,566,1652,
                563,561,562,539,593,527,
                565,558,565,1652,563,1655,
                589,1655,570,531,592,1648,
                567,1652,562,1656,589,1656,
                569],

                #KEY_8
                [567,530,590,534,
                569,554,567,530,593,531,
                562,561,571,527,597,527,
                564,1658,586,1655,571,1647,
                567,1652,593,1651,568,1651,
                569,1649,596,1648,567,530,
                592,532,571,1650,595,1646,
                568,1648,567,558,564,533,
                589,534,568,1654,591,1650,
                564,534,589,534,568,556,
                567,1651,563,1659,585,1656,
                570],

                #KEY_9
                [569,555,567,531,
                592,532,570,554,568,530,
                592,531,572,552,570,528,
                595,1650,568,1650,561,1657,
                587,1657,568,1649,566,1655,
                589,1650,565,1653,561,561,
                561,1657,568,554,572,1646,
                565,1652,593,529,563,1656,
                589,531,571,1650,585,534,
                568,1648,597,525,567,555,
                567,1650,565,557,569,1648,
                563],

                #KEY_0
                [570,553,569,527,
                595,527,565,558,565,531,
                591,531,563,558,564,533,
                589,1654,570,1647,568,1649,
                595,1653,562,1651,563,1654,
                591,1651,564,1654,564,558,
                561,1656,569,553,568,528,
                595,1650,565,530,592,1655,
                560,532,641,1601,563,534,
                588,1655,560,1656,573,549,
                569,1648,567,555,567,1650,
                565],

                #KEY_UP
                [584,534,568,555,
                566,532,592,531,571,553,
                569,530,592,533,569,554,
                569,1649,565,1655,590,1656,
                568,1652,564,1655,589,1656,
                568,1651,563,1657,598,528,
                565,1654,591,1654,570,528,
                595,529,562,562,561,1663,
                562,558,564,1656,569,556,
                566,533,590,1656,568,1656,
                559,1657,587,537,566,1654,
                591],

                #KEY_DOWN
                [564,534,588,535,
                567,557,566,532,590,533,
                569,554,569,529,597,526,
                562,1657,588,1657,568,1650,
                564,1656,593,1652,619,1600,
                563,1656,589,1656,569,1655,
                559,560,622,1598,567,556,
                567,1652,562,561,561,537,
                612,512,565,559,563,1656,
                568,556,567,1653,571,553,
                570,1655,559,1656,589,1657,
                568],

                #KEY_LEFT
                [564,559,563,534,
                588,535,568,554,569,530,
                592,530,623,500,562,535,
                587,1656,568,1649,566,1661,
                584,1649,565,1652,564,1653,
                590,1655,560,1657,568,554,
                568,529,644,1600,563,534,
                589,534,568,558,565,1649,
                565,558,565,1651,563,1655,
                590,533,569,1653,591,1649,
                566,1652,562,561,562,1656,
                568],

                #KEY_RIGHT
                [592,531,561,562,
                570,526,596,527,566,557,
                565,531,592,531,561,562,
                570,1647,568,1649,595,1647,
                568,1650,564,1653,592,1651,
                562,1659,557,1656,588,1655,
                570,1647,567,556,567,530,
                592,535,557,561,622,1596,
                568,553,569,528,595,528,
                564,1653,591,1656,559,1654,
                570,1648,587,535,567,1650,
                595],

                #KEY_OK
                [584,534,569,555,
                567,531,591,532,570,554,
                568,529,594,530,562,561,
                572,1646,568,1651,594,1651,
                563,1655,569,1655,590,1651,
                564,1654,570,1649,596,528,
                564,560,564,533,588,536,
                566,556,567,530,592,1653,
                561,536,597,1648,570,1648,
                563,1657,588,1657,567,1652,
                563,1660,585,535,567,1651,
                593],

                #KEY_H
                [595,528,565,558,
                564,533,589,535,567,556,
                567,530,592,533,574,550,
                568,1651,564,1655,589,1656,
                569,1649,570,1647,594,1655,
                558,1654,562,1656,589,535,
                571,1647,593,530,563,1655,
                590,534,568,556,566,1652,
                562,562,561,1656,569,555,
                567,1651,564,560,562,1656,
                573,1646,595,529,563,1656,
                589],


                #KEY_S
                [614,507,560,562,
                571,526,596,528,564,559,
                563,534,589,535,568,556,
                566,1652,561,1657,589,1655,
                569,1650,569,1649,592,1653,
                561,1657,568,1650,594,528,
                568,1650,591,533,569,555,
                568,529,593,530,562,1657,
                588,536,570,1649,592,531,
                571,1647,598,1647,567,1652,
                563,1655,589,535,567,1651,
                594]
                ]

    for key in range(len(key_map)):
        total_diff=0
        for i in range(len(inp)):
            diff=abs(inp[i]-key_map[key][i])
            if diff<100:
                diff=0
            total_diff+=diff
            # print total_diff,
        if total_diff < 1500:
            found_flag=1
            break

    # Send to socket client
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 21852)
        # print 'connecting to %s port %s' % server_address
        sock.connect(server_address)

        # print 'sending "%s"' % str(i)
        if found_flag:
            print keys[key]
            sock.sendall(keys[key])
        else:
            print "NO_MATCH"
            sock.sendall("NO_MATCH")
    except socket.error:
        print "Unable to connect to the server"
    finally:
        # print 'Closing socket'
        sock.close()

def match_with_button(inp):
    list_to_parse=[]
    large_val_found=0
    if debug:
        print inp,len(inp)

	#The ir signals are 65 bytes long with either a pulse length of ~500 us or ~1600us.
	#Sometime because of noise which cannot be filtered out, we have smaller chunks of signal also present in the bytearray
	#Something like a 1600us signal breaks into 500,600 and 500 us signal
	#This checks and skips those signals because they are very hard to filter out.
    if len(inp)==65:
        compare_with_button(inp)

#####################################################################
#####################################################################

# Variables for main function

######################################
# IR signals
# first pulse   : low of ~9000 us
# second pulse  : high of ~4200 us
# 65 pulses between ~500us or ~1600 us for 1 or 0 in the IR signal
# goes high again until the next pulse comes
# all the time is in microseconds
sig_thresh_len_before_header= 2000 # wait for a signal of at least this much length before looking for a signal

before_header_flag=0

# The signals have a big threshold to compensate for noise coming in the signal

# Noise is of 3 types
#   * a signal of less than 50 us, we just neglect these noises
#   * a very small signal which is not measured but causes the reading to stop and start again. We compensate for this by looking for 2 consecutive pulse or space from LIRC, if we see them, then we just add the next signal

# looking for the 1st signal
header_thresh=9000
header_margin=200   #signal length b/w 8800 and 9200
header_detected_flag=0

# looking for second signal
header_1_thresh=4200
header_1_margin=400     #b/w 3800 and 4600
header_1_detected_flag=0

trailer_min_length=2000 # looks for the last signal to be atleast 2000us

noise_thresh=50 # Noise threshold is 50us

last_pulse_us=0 # last pulse length
last_sig_type=0 # 1 pulse, 0 space
add_next_flag=0

pulse=1
space=0

detected_sig_buf=[]

def main(process_ir):
    global before_header_flag
    global header_detected_flag
    global header_1_detected_flag
    global last_pulse_us
    global last_sig_type
    global add_next_flag
    global detected_sig_buf

    # Read the raw value from the IR receiver
    line = process_ir.stdout.readline()

    # we also remove the trailing whitespace and newlines
    pulse_us_string = line[6:len(line)].rstrip()

    # check if we got a positive integer number
    if str.isdigit(pulse_us_string):
        pulse_us= int(pulse_us_string) # signal length
    else:
        return

    sig_type=  line[0:5]    # signal type : pulse or space

    if sig_type == 'pulse':
        sig_type=pulse
    else:
        sig_type=space

    # If noise was there in current pulse, just skip it
    if pulse_us < noise_thresh:
        if debug:
            print "noise:",pulse_us
        return

    # There are 3 checks to detect the keypresses
    # First is to look for a signal in ~9000 us pulse length
    # Second to look for pulse in ~4000 us length
    # Then to looks for 65 signals in ~500 us or 1600us length
    # Last for the signal to end
    # We do the check in the reverse order and if we are already on the second or third check, then just don;t do the initial checks

    #last check for end of signal
    if header_1_detected_flag==1:
        if pulse_us > trailer_min_length:   # Signal ending after the 65 pulses
            last_flag_state=[before_header_flag,header_detected_flag,header_1_detected_flag]
            header_1_detected_flag=0
            header_detected_flag=0
            before_header_flag=0
            if debug:
                print "de:",pulse_us
            header_1_detected_flag=0
            #*********************************************
            match_with_button(detected_sig_buf)
            detected_sig_buf=[]
        else:
            if add_next_flag:
                add_next_flag = 0
                # remove last sig from buffer
                if debug:
                    print "adding last",pulse_us,
                try:
                    detected_sig_buf.pop()
                except IndexError:
                    return
                pulse_us+=last_pulse_us
                if debug:
                    print pulse_us

            if last_sig_type == sig_type: # if a similar signal type was detected then add it in the next pulse
                add_next_flag=1

            if debug:
                if add_next_flag ==0:
                    print "d:",pulse_us

            detected_sig_buf.append(pulse_us)
    else:
        if debug:
            print "n:",pulse_us

    #Third check for 4k pulse
    if header_detected_flag ==1 and header_1_detected_flag == 0:
        if debug:
            print "checking before_header1_flag==1",pulse_us,header_1_thresh-header_1_margin,header_1_thresh+header_1_margin

        if add_next_flag:
            if debug:
                print "adding 4k pulse"
                print pulse_us,last_pulse_us
            pulse_us+=last_pulse_us

            add_next_flag=0

        if pulse_us > header_1_thresh-header_1_margin and pulse_us < header_1_thresh+header_1_margin:
            # IR signal detected
            if debug:
                print "header_1_detected_flag=1"
            header_1_detected_flag=1
        else:
            if last_sig_type == sig_type:
                if debug:
                    print "setting 4k pulse flag"
                add_next_flag=1
                last_pulse_us=pulse_us
                return
            last_flag_state=[before_header_flag,header_detected_flag,header_1_detected_flag]
            header_detected_flag=0
            before_header_flag=0

    #Second check for 9k pulse
    if before_header_flag==1 and header_detected_flag==0:
        if debug:
            print "checking before_header_flag==1",pulse_us,header_thresh-header_margin,header_thresh+header_margin

        if add_next_flag:
            pulse_us+=last_pulse_us

            add_next_flag=0
            if debug:
                print "checking_again before_header_flag==1",pulse_us,header_thresh-header_margin,header_thresh+header_margin,last_pulse_us

        if pulse_us > header_thresh-header_margin and pulse_us < header_thresh+header_margin:
            header_detected_flag=1
            if debug:
                print "header_detected_flag=1"
        else:
            if last_sig_type == sig_type:
                add_next_flag=1
            last_flag_state=[before_header_flag,header_detected_flag,header_1_detected_flag]
            before_header_flag=0

    #First check for anything over 2k preceeding the start of signal
    if before_header_flag==0 and pulse_us>sig_thresh_len_before_header:
        before_header_flag=1
        if debug:
            print "before_header_flag=1",pulse_us

    last_pulse_us=pulse_us
    last_sig_type= sig_type


if __name__ == "__main__":
    time.sleep(.5)

    process_ir = Popen('mode2 -d /dev/lirc0', stdout = PIPE, stderr = STDOUT, shell = True)

    print "Press any key on the remote to start"

    try:
        with GracefullExiter() as exiter:
            while not exiter.exit_now:
                main(process_ir)

    except Exception as unknown_exception:
        print(str(unknown_exception))

        # send the signal to just this process
        os.killpg(os.getpgid(process_ir.pid), signal.SIGINT)

        sys.exit(1)
