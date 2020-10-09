# scibiomart

This is just a simple wrapper around the API from BioMart, but I found existing packages were not quite sufficent 
for what I was wanting to do.

Here you can simply get the list of all genes and perform other biomart functions such as mapping between human and
mouse.

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

### See tests for more examples.

## Biomart information below

[[https://m.ensembl.org/biomart/martservice]]
# Martservices usage:

## (a) Querying BioMart

To submit a query using our webservices generate an XML document conforming to our Query XML syntax. 
This can be achieved simply by building up your query using MartView and hitting the XML button. 
This XML should be posted to http://www.ensembl.org/martservice attached to a single parameter of **query**.
 For example you could either:
- submit using wget replacing MY_XML with the XML obtained above, first removing any new lines.
```
wget -O results.txt 'http://www.ensembl.org/biomart/martservice?query=MY_XML' 
```

## (b) Retrieving Meta Data:

- to retrieve registry information: 
```
http://www.ensembl.org/biomart/martservice?type=registry
```
- to retrieve datasets available for a mart:
```
http://www.ensembl.org/biomart/martservice?type=datasets&mart=ENSEMBL_MART_ENSEMBL
```
- to retrieve attributes available for a dataset: 
```
http://www.ensembl.org/biomart/martservice?type=attributes&dataset=mpahari_gene_ensembl
```

- to retrieve filters available for a dataset: 
```
http://www.ensembl.org/biomart/martservice?type=filters&dataset=mpahari_gene_ensembl
```
- to retrieve configuration for a dataset:
```
http://www.ensembl.org/biomart/martservice?type=configuration&dataset=mpahari_gene_ensembl
```
More documentation at: [[http://www.biomart.org/other/user-docs.pdf]]

At the time of writing this the version of biomart was 0.7.

http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?>type=registry</Query>

http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Query><Query virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" ><Dataset name = "hsapiens_gene_ensembl" interface = "default" ><Filter name = "ensembl_gene_id" value = "ENSG00000139618,ENSG00000091483"/><Attribute name = "ensembl_gene_id" /></Dataset></Query>


http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Query><Query virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" ><Dataset name = "hsapiens_gene_ensembl" interface = "default" >< Filter name = "ensembl_gene_id" value = "ENSG00000139618,ENSG00000091483" /><Attribute name = "ensembl_gene_id" /><Attribute name = "hgnc_symbol" /><Attribute name = "uniprotswissprot" /></Dataset></Query>
