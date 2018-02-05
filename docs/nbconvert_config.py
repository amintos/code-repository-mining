c = get_config()

#Export all the notebooks in the current directory to the sphinx_howto format.
c.NbConvertApp.notebooks = ['index.pynb']
c.NbConvertApp.export_format = 'html'
c.Exporter.template_file = 'full_custom'
