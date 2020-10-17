************
sci-biomart
************

This is just a simple wrapper around the API from BioMart, but I found existing packages were not quite sufficent
for what I was wanting to do.

Here you can simply get the list of all genes and perform other biomart functions such as mapping between human and
mouse.

It is available under the `GNU General Public License (Version 3) <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.

Please post questions and issues related to sci-loc2gene on the `Issues <https://github.com/ArianeMora/scibiomart/issues>`_  section of the GitHub repository.


Running sci-biomart
===================

1. Install sci-biomart (:ref:`Installing <installing>`)

2. View examples in (:ref:`Examples <Examples>`)

3. Look at CLI examples in (:ref:`cli <examples/cli>`)

Extending sci-biomart
=====================

1. Make a pull request on github.


Biomart information below
=========================

The information in this section is taken directly from:
`Martservices usage <https://m.ensembl.org/biomart/martservice>`_

(a) Querying BioMart
--------------------

To submit a query using our webservices generate an XML document conforming to our Query XML syntax.
This can be achieved simply by building up your query using MartView and hitting the XML button.
This XML should be posted to http://www.ensembl.org/martservice attached to a single parameter of **query**.
 For example you could either:
- submit using wget replacing MY_XML with the XML obtained above, first removing any new lines.

.. code-block:: bash

    wget -O results.txt 'http://www.ensembl.org/biomart/martservice?query=MY_XML'


(b) Retrieving Meta Data:
-------------------------

- to retrieve registry information: http://www.ensembl.org/biomart/martservice?type=registry

- to retrieve datasets available for a mart: http://www.ensembl.org/biomart/martservice?type=datasets&mart=ENSEMBL_MART_ENSEMBL

- to retrieve attributes available for a dataset: http://www.ensembl.org/biomart/martservice?type=attributes&dataset=mpahari_gene_ensembl

- to retrieve filters available for a dataset: http://www.ensembl.org/biomart/martservice?type=filters&dataset=mpahari_gene_ensembl

- to retrieve configuration for a dataset: http://www.ensembl.org/biomart/martservice?type=configuration&dataset=mpahari_gene_ensembl

More documentation at: [[http://www.biomart.org/other/user-docs.pdf]]

At the time of writing this the version of biomart was 0.7.

(c) Example queries:
--------------------
.. code-block:: bash

    http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?>type=registry</Query>
    http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Query><Query virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" ><Dataset name = "hsapiens_gene_ensembl" interface = "default" ><Filter name = "ensembl_gene_id" value = "ENSG00000139618,ENSG00000091483"/><Attribute name = "ensembl_gene_id" /></Dataset></Query>
    http://www.ensembl.org/biomart/martservice?query=<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE Query><Query virtualSchemaName = "default" formatter = "TSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" ><Dataset name = "hsapiens_gene_ensembl" interface = "default" >< Filter name = "ensembl_gene_id" value = "ENSG00000139618,ENSG00000091483" /><Attribute name = "ensembl_gene_id" /><Attribute name = "hgnc_symbol" /><Attribute name = "uniprotswissprot" /></Dataset></Query>
