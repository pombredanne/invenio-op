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

from invenio.testutils import make_test_suite, run_test_suite, \
    InvenioTestCase


class WebDepositDepositionTest(InvenioTestCase):
    def clear_tables(self):
        from invenio.bibworkflow_model import Workflow, BibWorkflowObject
        from invenio.sqlalchemyutils import db
        Workflow.query.filter().delete()
        BibWorkflowObject.query.filter().delete()
        db.session.commit()

    def setUp(self):
        self.clear_tables()
        from invenio.webdeposit_models import DepositionType, Registry, \
            Deposition

        def workflow_task(obj, eng):
            d = Deposition(obj)
            draft = d.get_or_create_draft('_default')
            if not draft.is_completed():
                draft.complete()
                d.update()
                eng.halt("Wait")
            d.update()

        def make_sip(obj, eng):
            d = Deposition(obj)
            sip = d.get_latest_sip(sealed=False)
            if sip is None:
                sip = d.create_sip()
            sip.seal()
            d.update()

        class test(DepositionType):
            workflow = [
                workflow_task,
                make_sip,
            ]
            name = "Test upload"
            name_plural = "Test uploads"
            api = True
            deleteable = False
            editable = True
            draft_definitions = {
                '_default': None
            }
        Registry.register(test, default=True)

        super(WebDepositDepositionTest, self).setUp()

    def tearDown(self):
        from invenio.webdeposit_models import Registry
        Registry.unregister('test')
        self.clear_tables()
        super(WebDepositDepositionTest, self).tearDown()

    #
    # Utility methods
    #
    def login_user(self, username='admin'):
        from invenio.websession_model import User
        from invenio.webuser_flask import login_user, current_user
        user_id = User.query.filter_by(nickname=username).one().id
        login_user(user_id)
        assert user_id == current_user.get_id()
        return user_id

    def user_info(self, username='admin'):
        from invenio.websession_model import User
        from invenio.webuser_flask import UserInfo
        user_id = User.query.filter_by(nickname=username).one().id
        return UserInfo(user_id)

    #
    # Tests
    #
    def test_create(self):
        from invenio.bibworkflow_model import Workflow, BibWorkflowObject
        from invenio.bibworkflow_config import CFG_OBJECT_VERSION, \
            CFG_WORKFLOW_STATUS
        from invenio.webdeposit_models import Deposition

        dep = Deposition.create(self.user_info(), type='test')
        dep.save()

        self.assertEqual(
            dep.workflow_object.version, CFG_OBJECT_VERSION.RUNNING
        )
        self.assertEqual(
            dep.workflow_object.workflow.status, CFG_WORKFLOW_STATUS.RUNNING
        )

        self.assertEqual(Workflow.query.count(), 1)
        self.assertEqual(BibWorkflowObject.query.count(), 1)

        dep.delete()

        self.assertEqual(Workflow.query.count(), 0)
        self.assertEqual(BibWorkflowObject.query.count(), 0)

    def test_run(self):
        from invenio.bibworkflow_config import CFG_OBJECT_VERSION, \
            CFG_WORKFLOW_STATUS
        from invenio.webdeposit_models import Deposition, \
            DepositionNotDeletable

        dep = Deposition.create(self.user_info(), type='test')
        dep.save()

        dep.run_workflow()

        self.assertEqual(
            dep.workflow_object.version, CFG_OBJECT_VERSION.HALTED
        )
        self.assertEqual(
            dep.workflow_object.workflow.status, CFG_WORKFLOW_STATUS.FINISHED
        )

        dep.run_workflow()

        self.assertEqual(
            dep.workflow_object.version, CFG_OBJECT_VERSION.FINAL
        )
        self.assertEqual(
            dep.workflow_object.workflow.status, CFG_WORKFLOW_STATUS.COMPLETED
        )

        # Cannot delete after completed workflow
        self.assertRaises(DepositionNotDeletable, dep.delete)

        dep.reinitialize_workflow()
        dep.save()

        for draft in dep.drafts.values():
            self.assertFalse(draft.is_completed())

        self.assertEqual(
            dep.workflow_object.version, CFG_OBJECT_VERSION.RUNNING
        )
        self.assertEqual(
            dep.workflow_object.workflow.status, CFG_WORKFLOW_STATUS.RUNNING
        )

        # Still cannot delete - even after reinitialize
        self.assertRaises(DepositionNotDeletable, dep.delete)

        dep.run_workflow()

        self.assertEqual(
            dep.workflow_object.version, CFG_OBJECT_VERSION.HALTED
        )
        self.assertEqual(
            dep.workflow_object.workflow.status, CFG_WORKFLOW_STATUS.FINISHED
        )

        # Cannot delete after completed workflow
        self.assertRaises(DepositionNotDeletable, dep.delete)


TEST_SUITE = make_test_suite(WebDepositDepositionTest)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
