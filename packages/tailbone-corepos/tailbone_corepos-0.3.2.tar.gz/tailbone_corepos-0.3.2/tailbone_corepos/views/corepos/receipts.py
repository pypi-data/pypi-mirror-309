# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
CORE POS receipt views
"""

from corepos.db.office_op.model import CustomReceiptLine

from .master import CoreOfficeMasterView


class CustomReceiptLineView(CoreOfficeMasterView):
    """
    Master view for custom receipt text
    """
    model_class = CustomReceiptLine
    model_title = "CORE-POS Custom Receipt Line"
    route_prefix = 'corepos.custom_receipt_lines'
    url_prefix = '/core-pos/custom-receipt-lines'


def defaults(config, **kwargs):
    base = globals()

    CustomReceiptLineView = kwargs.get('CustomReceiptLineView', base['CustomReceiptLineView'])
    CustomReceiptLineView.defaults(config)


def includeme(config):
    defaults(config)
