.. cli:

CLI
===

CLI instructions for running scibiomart.

The CLI allows users to directly get attributes from Ensembl biomart. Filters are able to be used by passing
the filters as json strings (e.g. --f "{\"ensembl_gene_id\": \"ENSG00000139618,ENSG00000091483\"}" and attributes as a
comma separated list (e.g. --a "ensembl_gene_id,mmusculus_homolog_ensembl_gene").

Example:
--------
Here we show an example where we get the mouse ortholog for two ensembl IDs: ENSG00000139618,ENSG00000091483.

Ensembl human gene ID to mouse ortholog:

.. code-block:: bash

    scibiomart --m ENSEMBL_MART_ENSEMBL --d hsapiens_gene_ensembl --f "{\"ensembl_gene_id\": \"ENSG00000139618,ENSG00000091483\"}" --a "ensembl_gene_id,mmusculus_homolog_ensembl_gene"

Ensembl human gene ID to gene name:

.. code-block:: bash

    scibiomart --m ENSEMBL_MART_ENSEMBL --d hsapiens_gene_ensembl --f "{\"ensembl_gene_id\": \"ENSG00000139618,ENSG00000091483\"}" --a "ensembl_gene_id,entrezgene_id,hgnc_symbol"

Get all mouse gene names and uniprot symbols:

.. code-block:: bash

    scibiomart --m ENSEMBL_MART_ENSEMBL --d mmusculus_gene_ensembl --a "ensembl_gene_id,entrezgene_id,uniprotswissprot" --o mm10


Get all mouse gene names and positions and sort the data by gene starts:

.. code-block:: bash

    scibiomart --m ENSEMBL_MART_ENSEMBL --d mmusculus_gene_ensembl --a "ensembl_gene_id,external_gene_name,chromosome_name,start_position,end_position,strand" --o mm10Sorted --s t

Arguments
---------

.. argparse::
   :module: scibiomart
   :func: gen_parser
   :prog: scibiomart
   :nodefaultconst:
