import os
from glob import glob
import subprocess as sp
from textwrap import dedent

from ..common.output import inform

class NeuronBackend(object):

    def __init__(self, target):
        try:
            sp.check_call(['nrniv', '--version'])
        except OSError:
            import getnrn
            inform('Will fetch and install the latest NEURON version', indent=2)
            getnrn.install_neuron()
            
        self.modelpath = target
        self.extra_pars = []
        try:
            self.stdout = self.compile_modfiles()
        except sp.CalledProcessError as err:
            self.stderr = err.output
            self.returncode = err.returncode
            inform('Error compiling modfiles:', self.stderr, indent=2)


    def compile_modfiles(self):
        inform('Compiling modfiles', indent=1)
        init_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.realpath(self.modelpath)))
        out = 0
        if len(glob('*.mod')) > 0:
            out = sp.check_output(['nrnivmodl'])
            inform(out, indent=2)
        os.chdir(init_dir)
        return out
        

    def run(self):
        p = sp.Popen(['nrniv'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        cmd = '''\
        load_file("noload.hoc")
        cvode_active(1)
        load_file("%s")
        %s
        ''' % (self.modelpath, '\n'.join(self.extra_pars))
        stdout, stderr = p.communicate(dedent(cmd))
        with open('/tmp/osb_test.nrn.stdout', 'w') as f:
            f.write(stdout)
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = p.returncode

    def register_query(self, name, cmd=''):
        query = '{{%s}{print "%s: ", %s}}' % (cmd, name, name)
        inform('registred nrn query:', query, indent=2)
        self.extra_pars.append(query)
        return name

    def fetch_query(self, key):
        import re
        m = re.search(key+':'+'\s*([0-9]*\.?[0-9]+)\s*', self.stdout)
        if m:
            return m.groups()[0]
        else:
            print 'not found!'
            raise KeyError

    def query_area(self, secname):
        name = self.register_query('area_%s'%secname, 'forsec "%s" {for (x,0) area_%s+=area(x)}'%(secname,secname))
        return name
            
    def query_temperature(self):
        return self.register_query('temperature', 'temperature=celsius')










