## This file is part of Invenio.
## Copyright (C) 2012 CERN.
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

from functools import wraps
from invenio.bibworkflow_client import run_workflow, restart_workflow
from invenio.bibworkflow_engine import BibWorkflowEngine
from invenio.bibworkflow_object import BibWorkflowObject
from invenio.bibworkflow_model import Workflow, WfeObject
from invenio.bibworkflow_config import CFG_OBJECT_VERSION
from invenio.errorlib import register_exception


def set_db_context(f):
    def initialize(*args, **kwargs):
        """
        Initializes Flask and returns the given function with the
        correct context in order to run
        """
        # FIXME: This is from flaskshell.py
        # We kept the db initialization functions here instead of import *
        # as it could be good to keep it in case flaskshell will provide a function
        # instead of using import *

        # STEP 1 - Import Invenio Flask Application constructor and database object.
        from invenio.webinterface_handler_flask import create_invenio_flask_app
        from invenio.sqlalchemyutils import db

        # STEP 2 - Create application object and initialize database.
        app = create_invenio_flask_app()
        db.init_invenio()
        db.init_cfg(app)
        db.init_app(app)

        # STEP 3 - Create fake application request context and use it.
        ctx = app.test_request_context()
        ctx.push()
        # For explanation see: http://flask.pocoo.org/docs/shell/#firing-before-after-request
        app.preprocess_request()
        with app.app_context():
            return f(*args, **kwargs)
    return wraps(f)(initialize)


def runit(wname, data, external_save=None):
    """
    Runs workflow with given name and given data.
    Data can be specified as list of objects or
    single id of WfeObject/BibWorkflowObjects.
    """
    wfe = BibWorkflowEngine(wname, user_id=0, module_name="aa")
    wfe.setWorkflowByName(wname)
    wfe.setCounterInitial(data)
    wfe.save()

    objects = []
    for d in data:
        if isinstance(d, int):
            # Load list of object ids
            obj_old = WfeObject.query.filter(WfeObject.id == d).first()
            if obj_old.version != CFG_OBJECT_VERSION.INITIAL:
                obj = WfeObject()
                obj.copy(obj_old)
                objects.append(BibWorkflowObject(obj, wfe.db_obj.uuid, extra_object_class=external_save))
            else:
                obj = obj_old
                objects.append(BibWorkflowObject(obj, obj.workflow_id, extra_object_class=external_save))
        elif isinstance(d, BibWorkflowObject):
            objects.append(d)
        else:
            parsed_dict = parseDictionary(d, wfe.db_obj.uuid)
            objects.append(BibWorkflowObject(data = parsed_dict['data'],
                                             workflow_id = parsed_dict['workflow_id'],
                                             version = parsed_dict['version'],
                                             parent_id = parsed_dict['parent_id'],
                                             id = parsed_dict['id'],
                                             extra_data = parsed_dict['extra_data'],
                                             task_counter = parsed_dict['task_counter'],
                                             user_id = parsed_dict['user_id'],
                                             extra_object_class=external_save,
                                             data_type = parsed_dict['data_type'],
                                             uri = parsed_dict['uri']))

    run_workflow(wfe, objects)
    return wfe


def restartit(wid, data=None, restart_point="beginning", external_save=None):
    """
    Restarts workflow with given id (wid) and given data. If data are not
    specified then it will load all initial data for workflow. Depending on
    restart_point function can load initial or current objects.

    Data can be specified as list of objects
    or single id of WfeObject/BibWorkflowObjects.
    """
    if data is None:
        if isinstance(restart_point, str):
            data = WfeObject.query.filter(WfeObject.workflow_id == wid,
                                          WfeObject.version == 0)
        else:
            data = WfeObject.query.filter(WfeObject.workflow_id == wid,
                                          WfeObject.child_objects is None)
    else:
        #restart for oid, only one object
        if isinstance(data[0], (int, long)):
            data = [WfeObject.query.filter(WfeObject.id == data[0]).first()]

    workflow = Workflow.query.filter(Workflow.uuid == wid).first()
    wfe = BibWorkflowEngine(None, uuid=None, user_id=0, workflow_object=workflow,
                            module_name="module")
    wfe.setWorkflowByName(workflow.name)

    # do only if not this type already
    data = [BibWorkflowObject(d, wfe.uuid, extra_object_class=external_save) for d in data]
    
    #objects = []
    #for d in data:
    #    parsed_dict = parseDictionary(d)
    #    objects.append(BibWorkflowObject(data = parsed_dict['data'],
    #                                         workflow_id = parsed_dict['workflow_id'],
    #                                         version = parsed_dict['version'],
    #                                         parent_id = parsed_dict['parent_id'],
    #                                         id = parsed_dict['id'],
    #                                        extra_data = parsed_dict['extra_data'],
    #                                        task_counter = parsed_dict['task_counter'],
    #                                         user_id = parsed_dict['user_id'],
    #                                         extra_object_class=external_save,
    #                                         data_type = parsed_dict['data_type'],
    #                                         uri = parsed_dict['uri']))
    #wfe.setCounterInitial(objects)
    #wfe.save()
    #restart_workflow(wfe, objects, restart_point)
    
    wfe.setCounterInitial(data)
    wfe.save()
    restart_workflow(wfe, data, restart_point)

def parseDictionary(d, wfe_id=None):
    try:
        data = d['data']
    except:
        register_exception(prefix="Data field in dictionary passed to \
                           workflow is empty!")
        raise
        
    try:
        workflow_id = d['workflow_id']
    except:
        workflow_id = wfe_id
        
    try:
        version = d['version']
    except:
        version = CFG_OBJECT_VERSION.INITIAL
        
    try:
        parent_id = d['parent_id']
    except:
        parent_id = None
        
    try:
        id = d['id']
    except:
        id = None
        
    try:
        extra_data = d['extra_data']
    except:
        extra_data = None
    
    try:
        task_counter = d['task_counter']
    except:
        task_counter = [0]
    
    try:
        user_id = d['user_id']
    except:
        user_id = 0
    
    print d['data']
    try:
        if d['data_type'] == 'auto':
            data_type = BibWorkflowObject.determineDataType(d['data'])
        elif isinstance(d['data_type'], string):
            data_type = d['data_type']
    except:
        data_type = None
        
    print "data type: %s" % data_type
    
    try:
        uri = d['uri']
    except:
        uri = None
        
    return {'data': data, 'workflow_id': workflow_id, 'version':version,
            'parent_id': parent_id, 'id':id, 'extra_data': extra_data,
            'task_counter': task_counter, 'user_id': user_id,
            'data_type': data_type, 'uri': uri}
    