#!/bin/bash
#https://web.archive.org/web/20140530172605/http://markhildreth.me/article/monit-without-pidfiles
#http://stackoverflow.com/questions/23454344/use-monit-monitor-a-python-program
#https://mmonit.com/wiki/Monit/FAQ#pidfile
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GoPiGo)")
PIDFILE=/var/run/di_ir_reader.pid

case $1 in
   start)
       # Launch your program as a detached process
       nohup sudo python $REPO_PATH/Software/Python/ir_remote_control/gobox_ir_receiver_libs/di_ir_reader.py &
       # Get its PID and store it
       echo $! > ${PIDFILE} 
   ;;
   stop)
      kill `cat ${PIDFILE}`
      # Now that it's killed, don't forget to remove the PID file
      rm ${PIDFILE}
	  kill $(ps aux | grep 'mode2 -d /dev/lirc0' | awk '{print $2}')
   ;;
   *)
      echo "usage: di_ir_reader {start|stop}" ;;
esac
exit 0 
