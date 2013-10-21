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

from invenio.scriptutils import Manager

manager = Manager(usage="Perform upgrade engine operations.")


@manager.command
def run():
    """
    Command for applying upgrades
    """
    from invenio.inveniocfg_upgrader import cmd_upgrade
    cmd_upgrade()


@manager.command
def check():
    """
    Command for checking upgrades
    """
    from invenio.inveniocfg_upgrader import cmd_upgrade_check
    cmd_upgrade_check()


show = Manager(usage="Display pending or applied upgrades.")
manager.add_command("show", show)


@show.command
def pending():
    """
    Command for showing upgrades ready to be applied
    """
    from invenio.inveniocfg_upgrader import cmd_upgrade_show_pending
    cmd_upgrade_show_pending()


@show.command
def applied():
    """
    Command for showing all upgrades already applied.
    """
    from invenio.inveniocfg_upgrader import cmd_upgrade_show_applied
    cmd_upgrade_show_applied()


create = Manager(usage="Display pending or applied upgrades.")
manager.add_command("create", create)


@create.option('-p', '--path', dest='path')
@create.option('-r', '--repository', dest='repository', default='invenio')
def release(path, repository):
    """
    Create a new release upgrade recipe (for developers).
    """
    from invenio.inveniocfg_upgrader import cmd_upgrade_create_release_recipe
    cmd_upgrade_create_release_recipe(path, repository)


@create.option('-p', '--path', dest='path')
@create.option('-r', '--repository', dest='repository', default='invenio')
@create.option('-d', '--depends_on', dest='depends_on')
@create.option('--release', dest='release', action='store_true')
def recipe(path, repository, depends_on=None, release=False):
    """
    Create a new upgrade recipe (for developers).
    """
    from invenio.inveniocfg_upgrader import cmd_upgrade_create_standard_recipe
    cmd_upgrade_create_standard_recipe(path, repository, depends_on=depends_on,
                                       release=release)


@manager.command
def inspectdb():
    """Inspect database for missing tables"""

    print ">>> Checking database..."

    from sqlalchemy import event
    from invenio.inveniocfg import test_db_connection
    from invenio.sqlalchemyutils import db, autodiscover_models

    test_db_connection()
    autodiscover_models()
    tables = db.metadata.sorted_tables

    missing = 0
    for i, table in enumerate(tables):
        if not table.exists(bind=db.engine):
            print '>>> Found missing table', table
            missing += 1

    if missing == 0:
        print ">>> No tables missing for models."
    else:
        print "ERROR: Found %s missing tables." % missing


def main():
    from invenio.webinterface_handler_flask import create_invenio_flask_app
    app = create_invenio_flask_app()
    manager.app = app
    manager.run()

if __name__ == '__main__':
    main()
