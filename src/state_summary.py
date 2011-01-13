#!/usr/bin/env python


import Pyro.core
import logging

class state_summary( Pyro.core.ObjBase ):
    "class to supply suite state summary to external monitoring programs"

    def __init__( self, config, dummy_mode ):
        Pyro.core.ObjBase.__init__(self)
        self.task_summary = {}
        self.global_summary = {}
        # external monitors should access config via methods in this
        # class, in case config items are ever updated dynamically by
        # remote control
        self.config = config
        self.dummy_mode = dummy_mode
 
    def update( self, tasks, clock, paused, will_pause_at, stopping, will_stop_at ):
        self.task_summary = {}
        self.global_summary = {}

        for task in tasks:
            self.task_summary[ task.id ] = task.get_state_summary()

        self.global_summary[ 'last_updated' ] = clock.get_datetime()
        self.global_summary[ 'dummy_mode' ] = self.dummy_mode
        self.global_summary[ 'dummy_clock_rate' ] = clock.get_rate()
        self.global_summary[ 'paused' ] = paused
        self.global_summary[ 'stopping' ] = stopping
        self.global_summary[ 'will_pause_at' ] = will_pause_at
        self.global_summary[ 'will_stop_at' ] = will_stop_at
           
        # update deprecated old-style summary (DELETE WHEN NO LONGER NEEDED)
        #self.get_summary()

    def get_config( self, item ):
        return self.config[ item ]

    def get_state_summary( self ):
        return [ self.global_summary, self.task_summary ]
