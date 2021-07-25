# -*- coding:utf-8 -*-

container_names = [
    "cpu_ut",
    "net_i",
    "net_o",
    "fs_r",
    "fs_w"
]

container_pqls = [
    'sum(irate(container_cpu_usage_seconds_total{image!="",container_label_io_kubernetes_pod_name=""}[1m])) without (cpu)',
    'sum(rate(container_network_transmit_bytes_total{image!="",container_label_io_kubernetes_pod_name=""}[1m])) without (interface)',
    'sum(rate(container_network_receive_bytes_total{image!="",container_label_io_kubernetes_pod_name=""}[1m])) without (interface)',
    'sum(rate(container_fs_reads_bytes_total{image!="",container_label_io_kubernetes_pod_name=""}[1m])) without (device)',
    'sum(rate(container_fs_writes_bytes_total{image!="",container_label_io_kubernetes_pod_name=""}[1m])) without (device)'
]


dif_format_names = [
    "cpu_co",
    "mem_by"
]

dif_format_pqls = [
    'machine_cpu_cores',
    'machine_memory_bytes'
]

pdu_names = [
    "pdu_kw"
]

pdu_pqls = [
    'pdu_output_unit_kw'
]

pod_names = [
    "cpu_us",
    "mem_rs",
    "fs_us",
    "cpu_ut",
    "net_i",
    "net_o",
    "fs_r",
    "fs_w"
]

pod_pqls = [
    'sum by(container_label_io_kubernetes_pod_name, container_label_io_kubernetes_namespace) (rate(container_cpu_usage_seconds_total{image!="",container_label_io_kubernetes_pod_name!=""}[1m]))',
    'sum by(container_label_io_kubernetes_pod_name, container_label_io_kubernetes_namespace) (container_memory_rss{image!="",container_label_io_kubernetes_pod_name!=""})',
    'sum by(container_label_io_kubernetes_pod_name, container_label_io_kubernetes_namespace) (container_fs_usage_bytes{image!="",container_label_io_kubernetes_pod_name!=""})',
    'sum(irate(container_cpu_usage_seconds_total{image!="",container_label_io_kubernetes_pod_name!=""}[1m])) without (cpu)',
    'sum(rate(container_network_transmit_bytes_total{image!="",container_label_io_kubernetes_pod_name!=""}[1m])) without (interface)',
    'sum(rate(container_network_receive_bytes_total{image!="",container_label_io_kubernetes_pod_name!=""}[1m])) without (interface)',
    'sum(rate(container_fs_reads_bytes_total{image!="",container_label_io_kubernetes_pod_name!=""}[1m])) without (device)',
    'sum(rate(container_fs_writes_bytes_total{image!="",container_label_io_kubernetes_pod_name!=""}[1m])) without (device)'
]

vm_names = [
    "cpu_us",
    "cpu_id",
    "cpu_io",
    "cpu_ir",
    "cpu_ni",
    "cpu_so",
    "cpu_st",
    "cpu_sy",
    "cpu_ur",
    "mem_to",
    "mem_us",
    "mem_bu",
    "mem_ca",
    "mem_fr",
    "mem_sr",
    "mem_su",
    "disk_r",
    "disk_w",
    "net_o",
    "net_i",
    "intr",
    "mem_to"
]

vm_pqls = [
    '1-(sum(rate(node_cpu_seconds_total{cpu!="",mode="idle"}[1m])) without (cpu))',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="idle"}[1m])) without (cpu)',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="iowait"}[1m])) without (cpu)',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="irq"}[1m])) without (cpu)',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="nice"}[1m])) without (cpu)',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="softirq"}[1m])) without (cpu)',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="steal"}[1m])) without (cpu)',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="system"}[1m])) without (cpu)',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="user"}[1m])) without (cpu)',
    'node_memory_MemTotal_bytes',
    '1-(node_memory_MemFree_bytes/ node_memory_MemTotal_bytes)',
    'node_memory_Buffers_bytes/ node_memory_MemTotal_bytes',
    'node_memory_Cached_bytes/ node_memory_MemTotal_bytes',
    'node_memory_MemFree_bytes/ node_memory_MemTotal_bytes',
    'node_memory_SReclaimable_bytes/ node_memory_MemTotal_bytes',
    'node_memory_SUnreclaim_bytes/ node_memory_MemTotal_bytes',
    'sum(node_disk_read_bytes_total) without (device)',
    'sum(node_disk_written_bytes_total) without (device)',
    'sum(irate(node_network_transmit_bytes_total[1m])) without (device)',
    'sum(irate(node_network_receive_bytes_total[1m])) without (device)',
    'avg_over_time(node_intr_total[1m])',
    'sum(rate(container_memory_usage_bytes{image!=""}[1m]))'
]


ma_names = [
    "CPU-Usage",
    "SYS-Usage",
    "MEM-Usage",
    "IO-Usage",
    "Inlet-Temp",
    "Exhaust-Temp",
    "Pwr-Consumption"
]

ma_pqls = [
    '1-(sum(rate(node_cpu_seconds_total{cpu!="",mode="idle"}[1m])) without (cpu))',
    'sum(rate(node_cpu_seconds_total{cpu!="",mode="system"}[1m])) without (cpu)',
    '1-(node_memory_MemFree_bytes/ node_memory_MemTotal_bytes)',
    'irate(node_disk_io_time_seconds_total [5m])'
    'ipmi_temperatures{sensor=~".*CPU.*"}',
    'ipmi_temperatures{sensor!~".*CPU.*"}',
    'ipmi_power_supply_status'
]