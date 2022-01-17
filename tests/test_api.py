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

from scibiomart import SciBiomartApi


class TestApi(unittest.TestCase):

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
        # shutil.rmtree(self.tmp_dir)
        # Close any hanging sessions
        self.sb.close_session()

    def test_human_default(self):
        sb = SciBiomartApi()
        results_df = sb.get_human_default({'ensembl_gene_id': 'ENSG00000091483'})
        results_df = sb.sort_df_on_starts(results_df)
        assert results_df['external_gene_name'][0] == 'FH'
        self.sb = sb

    def test_mouse_default(self):
        sb = SciBiomartApi()
        results_df = sb.get_mouse_default({'ensembl_gene_id': 'ENSMUSG00000029844,ENSMUSG00000032446'})
        print(results_df.head())
        assert results_df['end_position'][0] == '52135297' #'52158317' hmm recently changed for hoxa1?
        self.sb = sb

    def test_sort_df_on_starts(self):
        sb = SciBiomartApi()
        results_df = sb.get_mouse_default({'ensembl_gene_id': 'ENSMUSG00000029844,ENSMUSG00000032446,'
                                                              'ENSMUSG00000020875,ENSMUSG00000038210',
                                           })
        print(results_df.values)

        # Now let's sort it
        results_df = sb.sort_df_on_starts(results_df)
        assert results_df.values[0][1] == 'Hoxb9' # If we use chr11 it is before chr6 'Hoxa1'
        assert results_df.values[1][1] == 'Hoxa1'
        assert results_df.values[2][1] == 'Hoxa11'
        assert results_df.values[3][1] == 'Eomes'

        self.sb = sb

    def test_hg19(self):
        sb = SciBiomartApi() #url='http://grch37.ensembl.org/biomart/martservice/')
        self.sb = sb
        results_df = sb.get_human_default(attr_list=['entrezgene_id'])
        # Now let's sort it
        results_df = sb.sort_df_on_starts(results_df)
        print(results_df.values)
        sb.save_as_csv(results_df, '.')

    def test_get_gene_flank(self):
        sb = SciBiomartApi()
        self.sb = sb
        results_df = sb.get_mouse_default(filter_dict={'ensembl_gene_id': 'ENSMUSG00000029844,ENSMUSG00000032446,'
                                                              'ENSMUSG00000020875,ENSMUSG00000038210',
                                                       'upstream_flank': 100},
                                          attr_list=['gene_flank', 'entrezgene_id'])
        print(results_df)
        results_df.to_csv('results_df.csv', index=False)

    # def test_hg38(self):
    #     sb = SciBiomartApi()
    #     self.sb = sb
    #     results_df = sb.get_human_default(filter_dict={'upstream_flank': 500},
    #                                       attr_list=['gene_flank', 'entrezgene_id'])
    #     # Now let's sort it
    #     # results_df = sb.sort_df_on_starts(results_df)
    #     #print(results_df.values)
    #     results_df.to_csv('500_flank_results_df.csv', index=False)
    #
    #     sb.save_as_csv(results_df, '.')

    def test_get_entrez(self):
        sb = SciBiomartApi()
        results_df = sb.get_mouse_default({'ensembl_gene_id': 'ENSMUSG00000029844,ENSMUSG00000032446,'
                                                              'ENSMUSG00000020875,ENSMUSG00000038210'},
                                          attr_list=['entrezgene_id'])

        # Now let's sort it
        results_df = sb.sort_df_on_starts(results_df)
        print(results_df.values)
        print(results_df.values[0][6])
        assert results_df.values[0][6] == '15417'
        assert results_df.values[1][6] == '15394'
        assert results_df.values[2][1] == 'Hoxa11'
        assert results_df.values[3][1] == 'Eomes'
        self.sb = sb

