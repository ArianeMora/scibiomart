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

from scibiomart import SciBiomart


class SciBiomartApi(SciBiomart):

    def __init__(self):
        super().__init__()

    def get_human_default(self, filter_dict=None, attr_list=None, dataset=None, mart=None):
        """ Run a default human query that gets location information and gene names for Ensembl IDs """
        mart = mart or 'ENSEMBL_MART_ENSEMBL'
        dataset = dataset or 'hsapiens_gene_ensembl'
        self.set_mart(mart)
        self.set_dataset(dataset)
        return self.run_default(filter_dict, attr_list)

    def get_mouse_default(self, filter_dict=None, attr_list=None, dataset=None, mart=None):
        """ Run a default mouse query that gets location information and gene names for Ensembl IDs """
        mart = mart or 'ENSEMBL_MART_ENSEMBL'
        dataset = dataset or 'mmusculus_gene_ensembl'
        self.set_mart(mart)
        self.set_dataset(dataset)
        return self.run_default(filter_dict, attr_list)

    def run_default(self, filter_dict=None, attr_list=None):
        """ Run the queries once the datasets have been assigned """
        filter_dict = filter_dict or {}
        attr_list = attr_list or []
        attr_list = ['ensembl_gene_id', 'external_gene_name', 'chromosome_name', 'start_position',
                     'end_position', 'strand'] + attr_list
        # Here we just run the query
        results_df = self.run_query(filter_dict, attr_list)
        # Remove any NA ensembl IDs
        results_df = results_df[~results_df['external_gene_name'].isnull()]
        convert_dict = {'start_position': int,
                        'end_position': int,
                        'strand': int,
                        'chromosome_name': str}     # This is the same way that bedtools sorts data i.e. 11 is before 2
        results_df = results_df.astype(convert_dict)
        return results_df



