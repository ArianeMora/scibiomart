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


class TestExample(unittest.TestCase):

    def setUp(self):
        # Flag to set data to be local so we don't have to download them repeatedly. ToDo: Remove when publishing.
        self.local = True

        if self.local:
            THIS_DIR = os.path.dirname(os.path.abspath(__file__))
            self.tmp_dir = os.path.join(THIS_DIR, 'data/tmp/')
            if os.path.exists(self.tmp_dir):
                shutil.rmtree(self.tmp_dir)
            os.mkdir(self.tmp_dir)
        else:
            self.tmp_dir = tempfile.mkdtemp(prefix='EXAMPLE_PROJECT_tmp_')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_list_marts(self):
        sb = SciBiomart()
        marts = sb.list_marts()
        expected_marts = ['ENSEMBL_MART_ENSEMBL', 'ENSEMBL_MART_MOUSE', 'ENSEMBL_MART_SEQUENCE',
                          'ENSEMBL_MART_ONTOLOGY', 'ENSEMBL_MART_GENOMIC', 'ENSEMBL_MART_SNP', 'ENSEMBL_MART_FUNCGEN']
        found_marts = []
        # Check that all the marts are in the expected marts list
        count_marts = 0
        for m in marts:
            for mart_attr in m:
                if mart_attr == '@name':
                    assert m[mart_attr] in expected_marts
                    count_marts += 1
                    found_marts.append(m[mart_attr])

        # Now check we had all of them
        print(found_marts)
        print(count_marts, len(expected_marts))

        assert count_marts == len(expected_marts)

    def test_list_datasets(self):
        sb = SciBiomart()
        err = sb.list_datasets()
        # Expect an error if we haven't set a mart.
        assert err['err'] == MART_SET_ERR
        sb.set_mart('ENSEMBL_MART_ENSEMBL')
        datasets = sb.list_datasets()

        check_datasets_exist = ['fcatus_gene_ensembl', 'pcoquereli_gene_ensembl', 'lsdomestica_gene_ensembl']
        found_datasets = []
        for d in datasets['name'].values:
            if d in check_datasets_exist:
                found_datasets.append(d)

        assert len(found_datasets) == len(check_datasets_exist)
        assert len(datasets) == 203

    def test_list_attributes(self):
        sb = SciBiomart()
        err = sb.list_attributes()
        assert err['err'] == MART_SET_ERR
        sb.set_mart('ENSEMBL_MART_ENSEMBL')
        err = sb.list_attributes()
        assert err['err'] == DATASET_SET_ERR
        sb.set_dataset('fcatus_gene_ensembl')
        df = sb.list_attributes(False)
        assert len(df['name'] == 'chromosome_name') > 0
        assert 'name_1059' in df[df['name'] == 'chromosome_name']['id'].values

    def test_list_configs(self):
        sb = SciBiomart()
        err = sb.list_configs()
        assert err['err'] == MART_SET_ERR
        sb.set_mart('ENSEMBL_MART_ENSEMBL')
        err = sb.list_configs()
        assert err['err'] == DATASET_SET_ERR
        sb.set_dataset('fcatus_gene_ensembl')
        configs = sb.list_configs(True)
        check_configs_exist = ['Exportable', 'Importable', 'MainTable']
        found_configs = []
        for d in configs:
            if d in check_configs_exist:
                found_configs.append(d)
        print(len(configs))
        assert len(found_configs) == len(check_configs_exist)
        assert len(configs) == 23

    def test_list_filters(self):
        sb = SciBiomart()
        err = sb.list_filters()
        assert err['err'] == MART_SET_ERR
        sb.set_mart('ENSEMBL_MART_ENSEMBL')
        err = sb.list_filters()
        assert err['err'] == DATASET_SET_ERR
        sb.set_dataset('fcatus_gene_ensembl')
        filters_df = sb.list_filters(False)
        assert filters_df['name'].values[0] == 'chromosome_name'
        assert filters_df['id'].values[3] == 'seq_region_strand_1020'

    def test_run_query(self):
        sb = SciBiomart()
        err = sb.list_filters()
        assert err['err'] == MART_SET_ERR
        sb.set_mart('ENSEMBL_MART_ENSEMBL')
        err = sb.list_filters()
        assert err['err'] == DATASET_SET_ERR
        sb.set_dataset('hsapiens_gene_ensembl')
        results = sb.run_query({'ensembl_gene_id': 'ENSG00000139618,ENSG00000091483'},
                               ['ensembl_gene_id', 'hgnc_symbol', 'uniprotswissprot'])
        assert 'ENSG00000139618' in results['ensembl_gene_id'].values
        assert 'ENSG00000091483' in results['ensembl_gene_id'].values
        assert 'ENSG00000091422' not in results['ensembl_gene_id'].values
        assert 'P07954' in results['uniprotswissprot'].values