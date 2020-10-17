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

import argparse
import sys
import json

from sciutil import SciUtil

from scibiomart import __version__
from scibiomart import SciBiomart


def print_help():
    lines = ['-h Print help information.']
    print('\n'.join(lines))


def run(args):

    sb = SciBiomart()
    if args.marts:  # Check if the user wanted to print the marts
        sb.list_marts(True)
        return
    sb.set_mart(args.m) # Otherwise set the mart
    if args.datasets: # Check if the user wanted to print the datasets
        sb.list_datasets(True)
        return
    sb.set_dataset(args.d) # Otherwise set the dataset
    if args.filters: # Check if the user wanted to print the filters
        sb.list_filters(True)
        return
    if args.attrs: # Check if the user wanted to print the filters
        sb.list_attributes(True)
        return
    if args.configs:
        sb.list_configs(True)
        return
    # Otherwise they actually have a query so we run it
    # Convert the filetrs string to a dict
    if args.f:
        filters = json.loads(args.f)
    else:
        filters = None
    if args.a:
        attrs = args.a.split(",")
    else:
        attrs = None
    if not attrs and args.s:  # We need the start and ends at least
        attrs = ['external_gene_name', 'chromosome_name', 'start_position', 'end_position', 'strand']
    sb.u.dp(['Running query on:',
             '\nMart: ', sb.mart,
             '\nDataset: ', sb.dataset_version,
             '\nFilters: ', filters,
             '\nAttributes: ', attrs])
    results_df = sb.run_query(filters, attrs)
    if args.s == 't':  # Check if we need to sort the file
        convert_dict = {'start_position': int,
                        'end_position': int,
                        'strand': int,
                        'chromosome_name': str}
        sb.u.warn_p(['Removing any genes with no gene name... Required for sorting.'])

        results_df = results_df[~results_df['external_gene_name'].isnull()]

        results_df = results_df.astype(convert_dict)
        results_df = sb.sort_df_on_starts(results_df)  # Note the user would have had to select the starts and ends

    saved_file = sb.save_as_csv(results_df, args.o)
    sb.u.dp(['Saved the output to:', saved_file])


def gen_parser():
    parser = argparse.ArgumentParser(description='sciloc2gene')
    parser.add_argument('--m', type=str, help='Mart: e.g. ENSEMBL_MART_ENSEMBL, '
                                              '\n \tuse --marts to see available marts.')
    parser.add_argument('--d', type=str, help='Dataset: e.g. hsapiens_gene_ensembl, mmusculus_gene_ensembl... '
                                              '\n \tuse --datasets to see available datasets.')
    parser.add_argument('--a', type=str, default=None, help='Attributes formatted as a JSON object'
                                              '\n \tuse --attrs to see available attributes.')
    parser.add_argument('--f', type=str, default=None, help='Filters as a comma separated list surrounded by "".'
                                              '\n \tuse --filters to see available filters.')
    parser.add_argument('--o', type=str, default='', help='Output folder')
    parser.add_argument('--s', type=str, default='f', help='Sort the dataframe before returning on gene starts (used '
                                                           'for programs that require a sorted file e.g. sciloc2gene.')
    parser.add_argument('--marts', type=str, default=None, help='Lists available marts.')
    parser.add_argument('--datasets', type=str, default=None, help='Lists available datasets for a specific mart '
                                                     '(must use --m option)')
    parser.add_argument('--attrs', type=str, default=None, help='Lists available attributes for a mart and dataset '
                                                    '(must use --m and --d options).')
    parser.add_argument('--filters', type=str, default=None, help='Lists available filters for a mart and dataset '
                                                    '(must use --m and --d options).')
    parser.add_argument('--configs', type=str, default=None, help='Lists configs filters for a mart and dataset '
                                                    '(must use --m and --d options).')
    return parser


def main(args=None):
    parser = gen_parser()
    if args:
        sys.argv = args
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
    elif sys.argv[1] in {'-v', '--v', '-version', '--version'}:
        print(f'scibiomart v{__version__}')
        sys.exit(0)
    else:
        print(f'scibiomart v{__version__}')
        args = parser.parse_args(args)
        # RUN!
        run(args)
    # Done - no errors.
    sys.exit(0)


if __name__ == "__main__":
    #main()
    main(["--m", f'ENSEMBL_MART_ENSEMBL',
          "--d", f'hsapiens_gene_ensembl',
          "--a", "ensembl_gene_id,external_gene_name,chromosome_name,start_position,end_position,strand",
          "--s", "t"])

    # ----------- Example below -----------------------
    """
    main(["--m", f'ENSEMBL_MART_ENSEMBL',
          "--d", f'hsapiens_gene_ensembl',
          "--f", '{"ensembl_gene_id": "ENSG00000139618,ENSG00000091483"}',
          "--a", "ensembl_gene_id,mmusculus_homolog_ensembl_gene"])
              
    scibiomart --m ENSEMBL_MART_ENSEMBL --d mmusculus_gene_ensembl --a "ensembl_gene_id,external_gene_name,chromosome_name,start_position,end_position,strand" --o mm10Sorted --s t

    """
