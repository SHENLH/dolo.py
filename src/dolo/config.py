#from __future__ import print_function

# This module is supposed to be imported first

# it contains global variables used for configuration

# platform :
#   - python
#   - sage

# engine


class MLabBridge:

    def __init__(self):
        self.engine = None
        
    def set_engine(self, engine_name):
        
        if engine_name == 'octave':
            import pytave as engine
            self.engine = engine
            self.engine_name = engine_name
        else:
            print('Unknown engine type : {0}'.format(engine_name))

    def __call__(self, cmd, nout=0):
        if self.engine_name == 'octave':
            resp = self.engine.eval(nout, cmd)
            return resp

    def feval(self, nargout, funcname, *arguments):
        if self.engine_name == 'octave':
            return self.engine.feval(nargout, funcname, *arguments)
            
    def dynare_config(self):
        try:
            self.__call__('dynare_version;') # how to print in a robust way ?
            dynare_version = self.__call__('version',1)[0]
            if self.engine_name == "octave":
                dynare_version = dynare_version[0].tostring()
            print( '- Dynare version is : ' + str(dynare_version) )
            self.__call__('dynare_config')
        except:
            print( '- Dynare is not in your matlab/octave path' )


class DefaultInterpreter():
    
    def display(self,obj):
        print(obj)

    display_html = display

class IPythonInterpreter(DefaultInterpreter):

    def __init__(self):
        import IPython
        v = [int(e) for e in IPython.__version__.split('.')]
        if v[0] == 0 and v[1] < 11:
            raise(Exception('IPython is supported since version 0.11.'))
        from IPython.core.display import display, display_html
        self.display = display
        self.display_html = display_html
        
class SageInterpreter(DefaultInterpreter):

    def __init__(self):
        from sagenb.misc.html import HTML
        self.display_html = HTML

    def display(self,obj):

        if hasattr(obj,'_repr_html_'):
            self.display_html(obj)

        elif isinstance(obj,str):
            self.display_html(obj)
            
        else:
            print(obj)


use_engine = {
    'sylvester': False
}


#engine = MLabBridge()
#engine.set_engine('octave')
#engine("addpath('/home/pablo/Programmation/dynare/matlab/')")



save_plots = False


for IPC in [IPythonInterpreter, SageInterpreter, DefaultInterpreter]:
    try:
        print IPC
        interpreter = IPC()
        break
    except Exception as e:
        print e
        pass

del IPC

def display(obj):
    interpreter.display(obj)

# monkey patch sympy so that time symbols are printed correctly

from sympy.printing.str import  StrPrinter
StrPrinter._print_TSymbol = lambda self,x: x.__str__()
from sympy.printing.latex import LatexPrinter
LatexPrinter._print_TSymbol = lambda self,x: x.__latex__()
