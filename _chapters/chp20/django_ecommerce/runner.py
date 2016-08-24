import os
import sys
import subprocess
from django.test.runner import DiscoverRunner
from django_ecommerce.guitest_settings import SERVER_ADDR


class LiveServerTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        retval = super(LiveServerTestRunner, self).setup_databases(**kwargs)
        self.spawn_server()
        return retval

    def spawn_server(self):
        gui_settings = 'django_ecommerce.guitest_settings'
        server_command = ["./manage.py", "runserver",
                          SERVER_ADDR, "--settings="+gui_settings]
        self.server_p = subprocess.Popen(
            server_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            preexec_fn=os.setsid
        )
        print("server process started up... continuing with test execution")

    def kill_server(self):
        try:
            print("killing server process...")
            os.killpg(os.getpgid(self.server_p.pid), 15)
            self.server_p.wait()
        except:
            print("exception", sys.exc_info()[0])

    def teardown_databases(self, old_config, **kwargs):
        self.kill_server()
        return super(LiveServerTestRunner, self).teardown_databases(
            old_config, **kwargs)
