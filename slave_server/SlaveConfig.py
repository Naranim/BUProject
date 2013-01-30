__author__ = 'ciemny'

import os

MasterAddress = "127.0.0.1"
MasterPort = 8090

SlaveName = "slave001"
SlavePort = 7799

FILES_PATH = os.getcwd() + "/file_sys/";
TMP_PATH = os.getcwd() + "/tmp/";

TICKET_TIMEOUT = 10