#----------------------------------------------------------------------------------------------------------------------
# Class: Thread
# Component of: benthysplitwf (https://vhub.org/tools/benthysplitwf)
# Called from: Imported from Benthysplitwf_GUI and Wrapper
# Purpose: Thread class derived from parent threading class
# Author: Renette Jones-Ivey
# Date: 08 Sept 2018
# ---------------------------------------------------------------------------------------------------------------------
import threading
import os
import signal

#  Thread class derived from parent threading class to allow thread to kill a forked process
#  Reference: https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python

class Thread(threading.Thread):

    # global access
    # Rappture.tools.commandPid does appear to be accessible via threading from the GUI
    rapptureCommandPid = -1

    def terminate(self):

        self.rapptureCommandTerminate = True

        if self.rapptureCommandPid < 0:
            print ("In Thread.terminate - rapptureCommandPid < 0\n")
        else:
            if self.rapptureCommandPid == 0:
                print ("In Thread.terminate - rapptureCommandPid == 0 (child process)\n")
            else:
                print ("In Thread.terminate - rapptureCommandPid > 0 (parent process)\n")
                print ("Terminating the workflow\n")
                os.kill(self.rapptureCommandPid, signal.SIGTERM)

