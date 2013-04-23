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


import smtpd
import asyncore

from invenio.config import CFG_MISCUTIL_SMTP_HOST, CFG_MISCUTIL_SMTP_PORT, \
    CFG_MISCUTIL_SMTP_USER, CFG_MISCUTIL_SMTP_PASS, CFG_MISCUTIL_SMTP_TLS
from flask.ext.script import Manager  # , prompt_bool

manager = Manager(usage="Test management commands")


@manager.command
def runmailserver():
    """ Run a test mail server printing all emails to console """
    for v in [CFG_MISCUTIL_SMTP_PASS, CFG_MISCUTIL_SMTP_USER,
              CFG_MISCUTIL_SMTP_TLS]:
        if v:
            print("Invenio will not be able to use this test mail server as %s"
                  " is set in invenio-local.conf. Please leave "
                  "CFG_MISCUTIL_SMTP_PASS, CFG_MISCUTIL_SMTP_USER and "
                  "CFG_MISCUTIL_SMTP_TLS blank in your invenio-local.conf." %
                  v.__name__)

    host = CFG_MISCUTIL_SMTP_HOST
    port = CFG_MISCUTIL_SMTP_PORT

    try:
        print(
            "Now accepting mail at %s:%s (hit CONTROL-C to stop)" % (host, port)
        )
        smtpd.DebuggingServer((host, port), None)
        asyncore.loop()
    except KeyboardInterrupt:
        print 'Exiting...'


def main():
    from invenio.webinterface_handler_flask import create_invenio_flask_app
    app = create_invenio_flask_app()
    manager.app = app
    manager.run()

if __name__ == '__main__':
    main()
