# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from __future__ import absolute_import
import os
from invenio.sqlalchemyutils import db
from invenio.config import CFG_PREFIX, CFG_LOGDIR
from flask.ext.script import Manager  # , prompt_bool

manager = Manager(usage="Celery management commands")


#@manager.option('-d', '--detached', dest='detached', default=False, action='store_true', help='Run worker in detached mode.')
@manager.option('-l', '--loglevel', dest='loglevel', default='INFO', help="Logging level, choose between DEBUG, INFO, WARNING, ERROR, CRITICAL, or FATAL.")
@manager.option('-b', '--beat', dest='beat', default='INFO', action='store_true', help="Also run the celerybeat periodic task scheduler. Please note that there must only be one instance of this service.")
@manager.option('-Q', '--queues', dest='queues', help="List of queues to enable for this worker, separated by comma. By default all configured queues are enabled. Example: -Q video,image")
def worker(loglevel, beat, queues):
    """ Start Celery worker instance. """
    try:
        # Celery 3.1
        from celery.bin.worker import worker
    except ImportError:
        # Celery 3.0
        from celery.bin.celeryd import WorkerCommand as worker
    argv = [
        'worker', '-A', 'invenio', '-l', loglevel, '-E',
        '--pidfile=%s' % os.path.join(CFG_PREFIX, 'var/run/celery.pid'),
    ]

    argv.extend(['-f', os.path.join(CFG_LOGDIR, 'celery.log')])
    if beat:
        argv.extend([
            '-B', '-s', os.path.join(CFG_PREFIX, 'var/celerybeat-schedule')
        ])
    if queues:
        argv.extend(['-Q', queues])

    print "Executing:"
    print "celery %s" % " ".join(argv)
    print ""

    worker().execute_from_commandline(argv=argv)


@manager.command
def install_daemon():
    """ Generate init.d script for running Celery as a daemon """
    print "Please see http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html for now."
    raise NotImplementedError

def main():
    from invenio.webinterface_handler_flask import create_invenio_flask_app
    app = create_invenio_flask_app()
    manager.app = app
    manager.run()

if __name__ == '__main__':
    main()
