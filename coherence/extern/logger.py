# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2006, Frank Scholz <coherence@beebits.net>

import os, sys, logging

#from twisted.python import log

LOG_UNSET       =  0
LOG_INFO        = 10
LOG_DEBUG       = 20
LOG_WARNING     = 30
LOG_ERROR       = 40
LOG_CRITICAL    = 50

class _Logger(object):
    """ a singleton LOG class
    """

    def __new__(cls, *args, **kwargs):
        obj = getattr(cls,'_instance_',None)
        if obj is not None:
            return obj
        else:
            obj = super(_Logger, cls).__new__(cls, *args, **kwargs)
            cls._instance_ = obj
            #log.startLogging(sys.stdout)
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s',
                                datefmt='%d %b %Y %H:%M:%S',)
            obj.log = logging.getLogger('.')
            obj.log.setLevel(logging.INFO)
            obj.feeds = {}
            return obj

    def __init__(self,name='',level=LOG_DEBUG):
        """ a LOG feed registers with us """
        if not self.feeds.has_key(name):
            self.feeds[name] = {'active':True,'level':level}
        
    def send(self, name, level, *args):
        try:
            if self.feeds[name]['active'] == False:
                return
            if level >= self.feeds[name]['level']:
                msg = ' '.join((str(i) for i in args)) 
                self.log.info('%s: %s' % (name, msg))
        except KeyError:
            self.log.log(level, "Logger msg error, feed %s not found" % name)

    def enable(self, name):
        try:
            self.feeds[name]['active'] = True
        except KeyError:
            self.feeds[name] = {'active':True,'level':LOG_DEBUG}

    def disable(self, name):
        try:
            self.feeds[name]['active'] = False
        except KeyError:
            self.feeds[name] = {'active':False,'level':LOG_DEBUG}
            
    def set_level(self, name, level):
        try:
            self.feeds[name]['level'] = level
        except KeyError:
            self.feeds[name] = {'active':False,'level':level}
        
class Logger:
    
    def __init__(self, name='', level=LOG_DEBUG):
        self.name = name
        self.log = _Logger(name,level)
        
    def send(self, level, *args):
        self.log.send( self.name, LOG_UNSET, *args)
        
    def msg(self, *args):
        self.log.send( self.name, LOG_DEBUG, *args)
        
    def info(self, *args):
        self.log.send( self.name, LOG_INFO, *args)
        
    def debug(self, *args):
        self.log.send( self.name, LOG_DEBUG, *args)

    def warning(self, *args):
        self.log.send( self.name, LOG_WARNING, *args)
        
    def error(self, *args):
        self.log.send( self.name, LOG_ERROR, *args)
        
    def critical(self, *args):
        self.log.send( self.name, LOG_CRITICAL, *args)

    def enable(self, name=None):
        if name == None:
            name=self.name
        self.log.enable(name)
        
    def disable(self, name=None):
        if name == None:
            name=self.name
        self.log.disable(name)
        
    def set_level(self, name=None, level=LOG_INFO):
        if name == None:
            name=self.name
        self.log.set_level(name,level)
        
    def overwrite(self,name,level=None,active=None):
        if level:
            self.log.set_level(name,level)
        if active != None:
            if active == True:
                self.log.enable(name)
            else:
                self.log.disable(name)
    
if __name__ == '__main__':

    from twisted.internet import reactor
    
    def test1():
        l1 = Logger('Test 1')
        l1.send( 'Dies', 'ist', 'ein', 'Send', 'Test')
        l1.info( 'Dies', 'ist', 'ein', 'Info', 'Test')
        
        l2 = Logger('Test 2')
        l2.info( 'Dies', 'ist', 'ein', 'Info', 'Test')

        l3 = Logger('Test 3')
        l3.error( 'Dies', 'ist', 'ein', 'Error', 'Test')
        l2.disable(name='Test 1')

        l1.info( 'Dies', 'ist', 'ein', 'Info', 'Test')
        
        l2.enable(name='Test 1')
        
        l1.info( 'Dies', 'ist', 'ein', 'Info', 'Test')

        l3.set_level(name='Test 1',level=LOG_ERROR)
        
        l1.info( 'Dies', 'ist', 'ein', 'Info', 'Test')
        l1.error( 'Dies', 'ist', 'ein', 'Error', 'Test')
        
    reactor.callWhenRunning( test1)

    reactor.run()