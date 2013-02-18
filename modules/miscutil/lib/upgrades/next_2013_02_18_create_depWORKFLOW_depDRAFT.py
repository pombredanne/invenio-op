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

from invenio.dbquery import run_sql


depends_on = ['next_initial']


def info():
    return "Create tables depWORKFLOW and depDRAFT"


def do_upgrade():
    """ Implement your upgrades here  """
    run_sql("""
        CREATE TABLE IF NOT EXISTS depWORKFLOW (
          uuid VARCHAR(36) NOT NULL,
          deposition_type VARCHAR(45) NOT NULL,
          obj_json TEXT NOT NULL,
          current_step INTEGER(15) UNSIGNED NOT NULL,
          status INTEGER(10) UNSIGNED NOT NULL,
          PRIMARY KEY (uuid)
        )ENGINE=MyISAM;
    """)

    run_sql("""
        CREATE TABLE IF NOT EXISTS depDRAFT (
          uuid VARCHAR(36) NOT NULL,
          deposition_type VARCHAR(45) NOT NULL,
          step INTEGER(15) UNSIGNED NOT NULL,
          user_id INTEGER(15) UNSIGNED NOT NULL,
          form_type VARCHAR(45) NOT NULL,
          form_values TEXT NOT NULL,
          timestamp DATETIME NOT NULL,
          PRIMARY KEY (uuid, step),
          FOREIGN KEY(uuid) REFERENCES depWORKFLOW (uuid)
        ) ENGINE=MyISAM;
    """)


def estimate():
    return 1
