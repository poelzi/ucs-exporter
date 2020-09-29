from prometheus_client.core import GaugeMetricFamily
from BaseCollector import BaseCollector


class UcsmChassisFaultCollector(BaseCollector):
    def __init__(self, creds, config):
        super().__init__(creds, config)

    def describe(self):
        yield GaugeMetricFamily("ucsm_chassis_metrics", "ucsm_chassis_fault_collector")

    def collect(self):
        print("UcsmChassisFaultCollector: Get updated handles !")
        self.get_handles()
        g = GaugeMetricFamily('ucsm_chassis_faults', 'UCSM server chassis faults',
                              labels=['server', 'fault', 'severity', 'description'])
        for server, handle in self.handles.items():
            sys = handle.query_dn("sys")
            chassis = handle.query_children(sys, class_id="EquipmentChassis")
            for chassi in chassis:
                faults = handle.query_children(chassi, class_id="FaultInst")
                print("Faults ..... ", faults, server)
                if faults:
                    for fault in faults:
                        g.add_metric(labels=[server, fault.cause, fault.severity, fault.descr],
                                     value=0)
        yield g

        self.logout_handles()
