
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
