# scibiomart

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4099048.svg)](https://doi.org/10.5281/zenodo.4099048)
[![PyPI](https://img.shields.io/pypi/v/scibiomart)](https://pypi.org/project/scibiomart/)

This is just a simple wrapper around the API from BioMart, but I found existing packages were not quite sufficent 
for what I was wanting to do i.e. cli interface and python interface with tsv API.  

Here you can simply get the list of all genes and perform other biomart functions such as mapping between human and
mouse.  

Have a look at the [docs](https://arianemora.github.io/scibiomart/) which explains things in more detail.

## Installation 

```
pip install scibiomart
```

## Usage
For the most simple usage, use API which will get the latest mouse and human and map gene IDs to gene names.
### Examples

```
from scibiomart import SciBiomartApi

sb = SciBiomartApi()

# Get only the default for those genes
results_df = sb.get_mouse_default({'ensembl_gene_id': 'ENSMUSG00000029844,ENSMUSG00000032446'})

# Select attributes
results_df = sb.get_mouse_default({'ensembl_gene_id': 'ENSMUSG00000020875,ENSMUSG00000038210'},
                                     attr_list=['entrezgene_id'])
# Get all genes
results_df = sb.get_mouse_default()

# Sort the results based on TSS (takes direction into account)
results_df = sb.sort_df_on_starts(results_df)

# Get human
results_df = sb.get_human_default()
```

### Examples extended
If you are interested in more than the simple API, see the tests for all examples, however, you can list the datasets
etc, and query other attributes.

#### Print marts
```
sb = SciBiomart()
marts = sb.list_marts()
print('\n'.join(marts))
```
#### Print datasets
```
sb = SciBiomart()
sb.set_mart('ENSEMBL_MART_ENSEMBL')
err = sb.list_datasets()
```
#### List attributes
```
sb = SciBiomart()  
sb.set_mart('ENSEMBL_MART_ENSEMBL')
sb.set_dataset('fcatus_gene_ensembl')
err = sb.list_attributes()
```
#### List configs
```
sb = SciBiomart()
sb.set_mart('ENSEMBL_MART_ENSEMBL')
sb.set_dataset('fcatus_gene_ensembl')
err = sb.list_configs()
```
#### List filters
```
sb = SciBiomart()
sb.set_mart('ENSEMBL_MART_ENSEMBL')
sb.set_dataset('fcatus_gene_ensembl')
err = sb.list_filters()
```
#### Run generic query
Here we show a generic query for two genes (as a comma separated list) and the attributes we're interested in are
'ensembl_gene_id', 'hgnc_symbol', 'uniprotswissprot'.

Run query: `def run_query(self, filter_dict: dict, attr_list: list):`
i.e. you can pass it a filter dictionary and a list of attributes. This will make it quicker, you can also run it and it 
will get all genes (i.e. if filter_dict is empty).

```
sb = SciBiomart()
sb.set_mart('ENSEMBL_MART_ENSEMBL')
sb.set_dataset('hsapiens_gene_ensembl')
results = sb.run_query({'ensembl_gene_id': 'ENSG00000139618,ENSG00000091483'},
                       ['ensembl_gene_id', 'hgnc_symbol', 'uniprotswissprot'])
print(results)
```
#### Match mouse to human
Get mouse orthologs for human genes
```
sb = SciBiomart()
sb.set_mart('ENSEMBL_MART_ENSEMBL')
sb.set_dataset('hsapiens_gene_ensembl')
attributes = ['ensembl_gene_id', 'mmusculus_homolog_ensembl_gene', 'mmusculus_homolog_perc_id_r1']
results = sb.run_query({'ensembl_gene_id': 'ENSG00000139618,ENSG00000091483'},  attributes)
print(results)
```

### See docs for more info
