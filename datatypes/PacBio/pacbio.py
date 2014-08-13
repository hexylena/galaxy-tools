
class pacbio(Text):
    file_ext = 'html'
    composite_type = 'auto_primary_file'
    def generate_primary_file(self, dataset=None):
        page = '<html><head><title>PacBio data %s</title></head><body><p><ul>' % dataset
        for composite_name, composite_file in self.get_composite_files(dataset=dataset).iteritems():
            page += '<li><a href="%s">%s</a></li>' % (composite_name,
                                                      composite_name)
        page += '</ul></body></html>'
        return page

class SMRTCell(PacBio):
    file_ext = 'html'
    composite_type = 'auto_primary_file'

    def __init__(self, **kwd):
        Text.__init__(self, **kwd)
        # Main files
        self.add_composite_file('data.1.xfer.xml', optional=True)
        self.add_composite_file('data.2.xfer.xml', optional=True)
        self.add_composite_file('data.3.xfer.xml', optional=True)
        self.add_composite_file('data.mcd.h5',     is_binary=True, optional=True)
        self.add_composite_file('data.metadata.xml', optional=True)
        #  /Analysis_Results/
        self.add_composite_file('analysis.1.bax.h5', is_binary=True, optional=True)
        self.add_composite_file('analysis.1.log', is_binary=True, optional=True)
        self.add_composite_file('analysis.1.subreads.fasta', optional=True)
        self.add_composite_file('analysis.1.subreads.fastq', optional=True)
        self.add_composite_file('analysis.2.bax.h5', is_binary=True, optional=True)
        self.add_composite_file('analysis.2.log', is_binary=True, optional=True)
        self.add_composite_file('analysis.2.subreads.fasta', optional=True)
        self.add_composite_file('analysis.2.subreads.fastq', optional=True)
        self.add_composite_file('analysis.3.bax.h5', is_binary=True, optional=True)
        self.add_composite_file('analysis.3.log', is_binary=True, optional=True)
        self.add_composite_file('analysis.3.subreads.fasta', optional=True)
        self.add_composite_file('analysis.3.subreads.fastq', optional=True)
        self.add_composite_file('analysis.bas.h5', is_binary=True, optional=True)
        self.add_composite_file('analysis.sts.csv',optional=True)
        self.add_composite_file('analysis.sts.xml',optional=True)


    def generate_primary_file(self, dataset=None):
        page = '<html><head><title>SMRT Cell %s</title></head><body><p><ul>' % dataset
        for composite_name, composite_file in self.get_composite_files(dataset=dataset).iteritems():
            page += '<li><a href="%s">%s</a></li>' % (composite_name,
                                                      composite_name)
        page += '</ul></body></html>'
        return page
