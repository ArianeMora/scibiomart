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

"""
This package is based on the pybiomart package however slimmed down & with added parsing functionality.

Api reference:
https://m.ensembl.org/info/data/biomart/biomart_restful.html#wget

wget -O result.txt 'http://www.ensembl.org/biomart/martservice?query=
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >
<Dataset name = "hsapiens_gene_ensembl" interface = "default" >
<Filter name = "ensembl_gene_id" value = "ENSG00000139618,ENSG00000091483"/>
<Attribute name = "ensembl_gene_id" />
<Attribute name = "ensembl_transcript_id" />
<Attribute name = "hgnc_symbol" />
<Attribute name = "uniprotswissprot" />
</Dataset>
</Query>'
"""

import urllib3
import time
import xmltodict
import pandas as pd

from sciutil import SciUtil, SciException
from scibiomart.errors import *


class SciBiomartException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)


def query_biomart(url):
    max_attempts = 80
    attempts = 0
    sleeptime = 10  # seconds
    http = urllib3.PoolManager()
    print(url)
    while attempts < max_attempts:
        try:
            response = http.request('GET', url)
            return response.data
        except:
            print("E")
        time.sleep(sleeptime)


class SciBiomart:

    def __init__(self, url=None):
        self.mart = None
        self.dataset = None
        self.url = url or 'http://www.ensembl.org/biomart/'
        self.url = self.url if self.url[-1] == '/' else f'{self.url}/'
        self.u = SciUtil()

    def set_mart(self, mart: str):
        if self.mart:
            self.u.dp([f'Overriding current mart: {self.mart} with new mart: {mart}'])
        self.mart = mart

    def set_dataset(self, dataset: str):
        if self.dataset:
            self.u.dp([f'Overriding current dataset: {self.dataset} with new mart: {dataset}'])
        self.dataset = dataset

    def add_filters(self, filter_dict: dict) -> str:
        filter_str = ''
        for filter_name, filter_value in filter_dict.items():
            # Check if it is a list, if so parse the values to strings & then add it
            if isinstance(filter_value, list):
                filter_value = ','.join(str(val) for val in filter_value)
            filter_str += f'<Filter name = "{filter_name}" value = "{filter_value}" />'
        return filter_str

    def add_attrs(self, attr_list: list) -> str:
        attr_str = ''
        for attr_name in attr_list:
            attr_str += f'<Attribute name = "{attr_name}" />'
        return attr_str

    def build_query(self, filter_dict: dict, attr_list: list) -> str:
        """ Builds a query formatted to get values from a dataset """
        query = f'{self.url}martservice?query=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Query>' \
                f'<Query virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >' \
                f'<Dataset name = "{self.dataset}" interface = "default" >'\
                f'{self.add_filters(filter_dict)}{self.add_attrs(attr_list)}</Dataset>' \
                f'</Query>'
        return query

    def run_query(self, filter_dict: dict, attr_list: list):
        err = self.check_mart()
        if err:
            return err
        err = self.check_dataset()
        if err:
            return err
        results = query_biomart(self.build_query(filter_dict, attr_list))

        if results:
            datasets = results.decode("utf-8").split('\n')
            rows = []
            header = attr_list
            for line in datasets:
                line = line.strip().split('\t')
                rows.append(line)
            df = pd.DataFrame(rows)
            if len(attr_list) > 1:
                df.columns = header
            return df

    def list_marts(self, print_values=True) -> dict:
        """
        Prints out a list of available marts.
        """
        marts = query_biomart(f'{self.url}biomart/martservice?type=registry')
        # Marts is returned as a tsv so just print each line
        if marts:
            marts_dict = xmltodict.parse(marts.decode("utf-8"))
            try:
                listed_marts = marts_dict['MartRegistry']
                listed_marts = listed_marts['MartURLLocation']
                for db in listed_marts:
                    if print_values:
                        self.u.dp(['Database: ', db['@database']])
                        for db_attr in db:
                            print(f'{db_attr}: {db[db_attr]}')
                return listed_marts
            except Exception as e:
                self.u.err_p(['Query list_marts failed. Are you connected to the internet? Maybe try again.'])
                raise SciBiomartException(e)

    def list_datasets(self, print_values=True) -> pd.DataFrame:
        """
        Prints out a list of available datasets for a mart.
        """
        err = self.check_mart()
        if err:
            return err
        datasets = query_biomart(f'{self.url}biomart/martservice?type=datasets&mart={self.mart}')
        # Marts is returned as a tsv so just print each line
        if datasets:
            datasets = datasets.decode("utf-8")
            datasets = datasets.split('\n')
            rows = []
            header = ['name', 'description', 'number', 'id', 'unknown_col1', 'unknown_col1', 'unknown_col3', 'date']
            for line in datasets:
                line = line.strip().split('\t')
                if len(line) > 1:
                    if print_values:
                        print('\t'.join(line[1:]))
                    rows.append(line[1:])
            df = pd.DataFrame(rows)
            df.columns = header
            return df

    def list_attributes(self, print_values=True):
        """
        Lists attributes for a given dataset.
        """
        err = self.check_mart()
        if err:
            return err
        err = self.check_dataset()
        if err:
            return err
        dataset_attributes = query_biomart(f'{self.url}biomart/martservice?type=attributes&dataset='
                                           f'{self.dataset}&mart={self.mart}')
        # Marts is returned as a tsv so just print each line
        if dataset_attributes:
            dataset_attributes = dataset_attributes.decode("utf-8").split('\n')
            rows = []
            header = ['name', 'description', 'values', 'text_filters', 'qualifiers', 'label', 'id']
            for line in dataset_attributes:
                line = line.strip().split('\t')
                if len(line) > 1:
                    if print_values:
                        print('\t'.join(line))
                    rows.append(line)
            df = pd.DataFrame(rows)
            df.columns = header
            return df

    def list_configs(self, print_values=True):
        """
        Lists attributes for a given dataset.
        """
        err = self.check_mart()
        if err:
            return err
        err = self.check_dataset()
        if err:
            return err
        dataset_configs = query_biomart(f'{self.url}biomart/martservice?type=configuration&dataset'
                                        f'={self.dataset}&mart={self.mart}')
        # Marts is returned as a tsv so just print each line
        if dataset_configs:
            dataset_configs = xmltodict.parse(dataset_configs.decode("utf-8"))
            try:
                listed_configs = dataset_configs['DatasetConfig']

                if print_values:
                    self.u.dp(['Dataset: ', listed_configs['@dataset']])
                    for ds_attr in listed_configs:
                        print(f'{ds_attr}: {listed_configs[ds_attr]}')

                return listed_configs
            except Exception as e:
                self.u.err_p(['Query list_configs failed. Are you connected to the internet? Maybe try again.'])
                raise SciBiomartException(e)

    def list_filters(self, print_values=True):
        """
        Lists filters for a given dataset.
        """
        err = self.check_mart()
        if err:
            return err
        err = self.check_dataset()
        if err:
            return err
        dataset_filters = query_biomart(f'{self.url}biomart/martservice?type=filters&dataset'
                                        f'={self.dataset}&mart={self.mart}')
        # Marts is returned as a tsv so just print each line
        if dataset_filters:
            dataset_filters = dataset_filters.decode("utf-8").split('\n')
            rows = []
            # germ_line_variation_source	limit to genes with germline variant data sources	[dbSNP]
            # filters	list	=	fcatus_gene_ensembl__mart_transcript_variation__dm	name_2021
            header = ['name', 'description', 'values', 'unknown', 'text_filters',
                      'data_type', 'qualifiers', 'label', 'id']
            for line in dataset_filters:
                line = line.strip().split('\t')
                if len(line) > 1:
                    if print_values:
                        print('\t'.join(line))
                    rows.append(line)
            df = pd.DataFrame(rows)
            df.columns = header
            return df

    def check_mart(self):
        if not self.mart:
            err_msg = MART_SET_ERR
            self.u.warn_p([err_msg])
            return {'err': err_msg}

    def check_dataset(self):
        if not self.dataset:
            err_msg = DATASET_SET_ERR
            self.u.warn_p([err_msg])
            return {'err': err_msg}
