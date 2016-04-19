#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from subprocess import Popen
import time
import atexit
try:
    from py4j.java_gateway import ( JavaGateway, launch_gateway , GatewayParameters )
except ImportError:
    pass

from . import utils

gateway=None
javaChild=None

class JvmError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def shutdown_jvm():
    global gateway
    # global javaChild

    if gateway != None:
        gateway.shutdown()
        # javaChild.wait()

def init_jvm():
    global gateway
    # global javaChild

    """Initializes the Java virtual machine (JVM).
    """
    if gateway != None:
        return



    folder_suffix = [
        u'{0}', u'{0}{1}bin',
        u'{0}{1}jhannanum-0.8.4.jar',
        u'{0}{1}kkma-2.0.jar',
        u'{0}{1}komoran-2.4-e.jar',
        u'{0}{1}shineware-common-2.0.jar', u'{0}{1}shineware-ds-1.0.jar',
        u'{0}{1}snakeyaml-1.12.jar', u'{0}{1}scala-library-2.11.4.jar', u'{0}{1}twitter-korean-text-2.4.3.jar', u'{0}{1}twitter-text-1.10.1.jar',
        u'{0}{1}*']

    javadir = u'%s%sjava' % (utils.installpath, os.sep)
    args = [javadir, os.sep]
    classpath = os.pathsep.join(f.format(*args) for f in folder_suffix)
    py4jpath = u'{0}{1}py4j-0.9.2.jar'.format(*args)

    port = launch_gateway(jarpath=py4jpath, classpath=classpath, javaopts=['-Dfile.encoding=UTF8', '-ea', '-Xmx768m'])
    # javaChild = Popen(['java',
    #     '-cp', classpath,
    #     '-Dfile.encoding=UTF8',
    #     '-ea', '-Xmx768m',
    #     'kr.lucypark.py4j.KonlpyGateway']);

    print "Initializing JAVA frameworks..."
    time.sleep(1)
    jvm_e = None
    for i in range(0, 10):
        try:
            time.sleep(1)
            gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))
        except Exception as e:
            gateway = None
            jvm_e = e;
            continue
        break
    if gateway == None:
        if jvm_e != None:
            raise jvm_e
        raise JvmError("Could not connect to JVM. unknown error");

    print "JAVA frameworks initialized."
    atexit.register(shutdown_jvm);

def get_jvm():
    global gateway
    if gateway != None:
        return gateway.jvm

    return None;
