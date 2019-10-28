from google.appengine.ext import ndb
set

class GpuEntry(ndb.Model):
    # properties
    gpu_name = ndb.StringProperty()
    gpu_mfg = ndb.StringProperty()  # manufacturer
    gpu_isdt = ndb.DateProperty()  # issue date

    # features
    gpu_geomsh = ndb.BooleanProperty()  # geometry shader
    gpu_tessesh = ndb.BooleanProperty()  # tesselation shader
    gpu_shint16 = ndb.BooleanProperty()  # shader int 16
    gpu_sparbind = ndb.BooleanProperty()  # sparse binding
    gpu_texcompetc2 = ndb.BooleanProperty()  # texture compression etc 2
    gpu_vxpipeline = ndb.BooleanProperty()  # vertex pipeline stores and atomic


