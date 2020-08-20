###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import os
import shutil
import tempfile
import unittest

from scibiomart import SciBiomart
from scibiomart.errors import *


class SciBiomartApi(SciBiomart):

    def __init__(self):
        super().__init__()

    def get_human_default(self, filter_dict=None, attr_list=None, dataset=None, mart=None):
        mart = mart or 'ENSEMBL_MART_ENSEMBL'
        dataset = dataset or 'hsapiens_gene_ensembl'
        self.set_mart(mart)
        self.set_dataset(dataset)
        filter_dict = filter_dict or {}
        attr_list = attr_list or []
        attr_list = ['ensembl_gene_id', 'external_gene_name', 'chromosome_name', 'start_position',
                     'end_position', 'strand'] + attr_list
        # Here we just run the query
        results_df = self.run_query(filter_dict, attr_list)
        return results_df

    def get_mouse_default(self, filter_dict=None, attr_list=None, dataset=None, mart=None):
        mart = mart or 'ENSEMBL_MART_ENSEMBL'
        dataset = dataset or 'mmusculus_gene_ensembl'
        self.set_mart(mart)
        self.set_dataset(dataset)
        filter_dict = filter_dict or {}
        attr_list = attr_list or []
        attr_list = ['ensembl_gene_id', 'external_gene_name', 'chromosome_name', 'start_position',
                     'end_position', 'strand'] + attr_list
        # Here we just run the query
        results_df = self.run_query(filter_dict, attr_list)
        return results_df