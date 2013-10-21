from django.forms import ModelForm
from wStationMgr.models import Server,BaseTreeNode

class MyServerForm(ModelForm):
   class Meta:
      model = Server



