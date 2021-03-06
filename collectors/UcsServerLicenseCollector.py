from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector


class UcsServerLicenseCollector(BaseCollector):
    def __init__(self, creds, inventory_file):
        super().__init__(creds, inventory_file)
        self.license_state = {
            "license-expired": 0,
            "not-applicable": 1,
            "license-ok": 2
        }

    def describe(self):
        yield GaugeMetricFamily("ucs_server_license", "licenses")

    def collect(self):
        print("Getting updated handles for UcsServerLicenseCollector !")
        self.get_handles()

        g = GaugeMetricFamily('ucs_port_license', 'Information about port license',
                              labels=['server', 'port_name'])
        for server, handle in self.handles.items():
            for eth_p in handle.query_classid("EtherPIo"):
                port_name = "{}-{}-{}".format(eth_p.switch_id,
                                              eth_p.aggr_port_id,
                                              eth_p.rn)
                license_state = eth_p.lic_state
                labels = [server, port_name]
                g.add_metric(labels=labels, value=self.license_state[license_state])
        yield g

        self.logout_handles()
