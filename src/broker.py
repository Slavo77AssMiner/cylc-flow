#!/usr/bin/env python


import sys

# BROKER:
# A collection of output messages with associated owner ids (of the
# originating tasks) representing the outputs of ALL TASKS in the
# suite, and initialised from the outputs of all the tasks.
# "Satisfied" => the output has been completed.

class broker(object):
    # A broker aggregates output messages from many objects.
    # Each task registers its outputs with the suite broker, then each
    # task tries to get its prerequisites satisfied by the broker's
    # outputs.

    def __init__( self ):
        self.all_outputs = {}   # all_outputs[ taskid ] = [ taskid's requisites ]

    def register( self, task ):
        # because task ids are unique, and all tasks register their
        # outputs anew in each dependency negotiation round, register 
        # should only be called once by each task

        owner_id = task.id
        outputs = task.outputs

        if owner_id in self.all_outputs.keys():
            print "ERROR:", owner_id, "has already registered its outputs"
            sys.exit(1)

        self.all_outputs[ owner_id ] = outputs

        # TO DO: SHOULD WE CHECK FOR SYSTEM-WIDE DUPLICATE OUTPUTS?
        # (note that successive tasks of the same type can register
        # identical outputs if they write staggered restart files).

    def reset( self ):
        # throw away all messages
        self.all_outputs = {}

    def dump( self ):
        # for debugging
        print "BROKER DUMP:"
        for id in self.all_outputs.keys():
            print " " + id
            for output in self.all_outputs[ id ].get_list():
                print " + " + output
               
    def negotiate( self, task ):
        # can my outputs satisfy any of task's prerequisites
        for id in self.all_outputs.keys():
            # TO DO: if task becomes fully satsified mid-loop we could
            # bail out with the following commented-out conditional, but
            # is the cost of doing the test every time more than that of
            # continuing when task is fully satisfied?
            # CONDITIONAL: if task.not_fully_satisfied():
            task.satisfy_me( self.all_outputs[ id ] )

