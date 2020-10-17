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
This package is similar to pybiomart.

Api reference:
https://m.ensembl.org/info/data/biomart/biomart_restful.html#wget

"""

import urllib3
import xmltodict
import pandas as pd

from sciutil import SciUtil, SciException
from scibiomart.errors import *


class SciBiomartException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)


class SciBiomart:

    def __init__(self, url=None):
        self.mart = None
        self.dataset = None
        self.url = url or 'http://www.ensembl.org/biomart/'
        self.url = self.url if self.url[-1] == '/' else f'{self.url}/'
        self.u = SciUtil()
        self.dataset_version = ''
        self.session = urllib3.PoolManager()
        self.df = None  # Stores the most recent dataframe.

    def query_biomart(self, query):
        try:
            response = self.session.request('GET', query)
            return response.data
        except Exception as e:
            self.u.err_p(['query_biomart: Error running biomart query: ', query])
            raise SciBiomartException(str(e))

    def set_mart(self, mart: str):
        if self.mart:
            self.u.dp([f'Overriding current mart: {self.mart} with new mart: {mart}'])
        self.mart = mart

    def set_dataset(self, dataset: str):
        if self.dataset:
            self.u.dp([f'Overriding current dataset: {self.dataset} with new dataset: {dataset}'])
        self.dataset = dataset
        # Here we do a cheeky and even though people don't ask for it, we're going to go and add the dataset
        # version to the label of the dataset (this way people can trace it back)
        dataset_configs = self.list_configs(False)
        if dataset_configs['@version']:
            self.dataset_version = f'{dataset}-{dataset_configs["@version"]}'

    def add_filters(self, filter_dict: dict) -> str:
        filter_str = ''
        if filter_dict:
            for filter_name, filter_value in filter_dict.items():
                # Check if it is a list, if so parse the values to strings & then add it
                if isinstance(filter_value, list):
                    filter_value = ','.join(str(val) for val in filter_value)
                filter_str += f'<Filter name = "{filter_name}" value = "{filter_value}" />'
        return filter_str

    def add_attrs(self, attr_list: list) -> str:
        attr_str = ''
        if attr_list:
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
        results = self.query_biomart(self.build_query(filter_dict, attr_list))

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
            self.df = df
            return df

    def list_marts(self, print_values=True) -> dict:
        """
        Prints out a list of available marts.
        """
        marts = self.query_biomart(f'{self.url}martservice?type=registry')
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
        datasets = self.query_biomart(f'{self.url}martservice?type=datasets&mart={self.mart}')
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
            self.df = df
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
        dataset_attributes = self.query_biomart(f'{self.url}martservice?type=attributes&dataset='
                                           f'{self.dataset}&mart={self.mart}')
        # Marts is returned as a tsv so just print each line
        if dataset_attributes:
            dataset_attributes = dataset_attributes.decode("utf-8").split('\n')
            rows = []
            # Made this up so use with caution.
            header = ['name', 'description', 'values', 'text_filters', 'qualifiers', 'label', 'id']
            for line in dataset_attributes:
                line = line.strip().split('\t')
                if len(line) > 1:
                    if print_values:
                        print('\t'.join(line))
                    rows.append(line)
            df = pd.DataFrame(rows)
            df.columns = header
            self.df = df
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
        dataset_configs = self.query_biomart(f'{self.url}martservice?type=configuration&dataset'
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
        dataset_filters = self.query_biomart(f'{self.url}martservice?type=filters&dataset'
                                        f'={self.dataset}&mart={self.mart}')
        # Marts is returned as a tsv so just print each line
        if dataset_filters:
            dataset_filters = dataset_filters.decode("utf-8").split('\n')
            rows = []
            # Made this up so use with caution.
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
            self.current_df = df
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

    def save_as_csv(self, df: pd.DataFrame, file_path: str):
        self.u.save_df(df, f'{file_path}{self.dataset_version}.csv')
        return f'{file_path}{self.dataset_version}.csv'

    def close_session(self):
        """ Terminate any connections that are hanging. """
        self.session.clear()

    def get_current_df(self):
        """ Return the most recent query. """
        return self.df

    @staticmethod
    def sort_df_on_starts(results_df):
        """
        Sorts a results dataframe by chr, start, and end. This allows us to do fast matching in
        other tools i.e. when we're looking at annotating regions to genes. (sciloc2gene)

        We sort this in the same way that our peak files are sorted using samtools.
        """

        starts = results_df['start_position'].values
        ends = results_df['end_position'].values
        strands = results_df['strand'].values
        fake_starts = []
        i = 0
        for strand in strands:
            # Lets make this have a "fake" start based on the TSS
            if strand < 0:
                fake_starts.append(ends[i])
            else:
                fake_starts.append(starts[i])
            i += 1
        # Again, lets use the ordering of the index keys
        results_df['fake_starts'] = fake_starts
        # Sort on fake starts and chr
        sorted_df = results_df.sort_values(['chromosome_name', 'fake_starts'], ascending=[True, True])
        # Drop our fake col
        sorted_df = sorted_df.drop(['fake_starts'], axis=1)
        return sorted_df
