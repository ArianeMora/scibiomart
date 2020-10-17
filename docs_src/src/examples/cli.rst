.. cli:

CLI
===

CLI instructions for running scibiomart.

Example:

.. code-block:: bash

    scibiomart --m ENSEMBL_MART_ENSEMBL --d hsapiens_gene_ensembl --f "{\"ensembl_gene_id\": \"ENSG00000139618,ENSG00000091483\"}" --a "ensembl_gene_id,mmusculus_homolog_ensembl_gene"


Arguments
---------

.. argparse::
   :module: scibiomart
   :func: gen_parser
   :prog: scibiomart
   :nodefaultconst:
