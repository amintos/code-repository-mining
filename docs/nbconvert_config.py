c = get_config()

#Export all the notebooks in the current directory to the sphinx_howto format.
c.NbConvertApp.notebooks = ['raw-notebooks/Analysis of Twitter and CVE reference data.ipynb']
c.NbConvertApp.export_format = 'html'
c.Exporter.template_file = 'full_custom'
