import os
import datetime as dt
from flask import json
from binascii import b2a_hex


SERVER_URL = ""
TO_CAPTURE_COLUMNS = ["md5"]
IOC_COLUMNS = ["md5", "sha1", "sha256", "domain_name", "remote_address", "url"]
DEFAULT_PLATFORMS=['windows','linux','darwin','freebsd']
clients = {}
websockets = {}
public_server = False
socketio = None


class PolyReconPackData:
    linux_recon_enabled = True
    windows_recon_enabled = True
    darwin_recon_enabled = True
    polylogyx_recon_pack_windows = {
        "packs": {"polylogyx_recon_pack_windows": {"platform": "windows", "version": "2.9.0",
                                                   "queries": {"system_info": {
                                                       "query": "select * from system_info;",
                                                       "interval": 86400, "platform": "windows",
                                                       "version": "2.9.0",
                                                       "description": "System info",
                                                       "value": "System info",
                                                       "snapshot": True}, "os_version": {
                                                       "query": "select * from os_version;",
                                                       "interval": 86400, "platform": "windows",
                                                       "version": "2.9.0",
                                                       "description": "Os details",
                                                       "value": "Os details", "snapshot": True},
                                                       "interface_details": {
                                                           "query": "select ia.interface, address,  mac,ibytes, obytes from interface_details id join interface_addresses ia on ia.interface = id.interface where length(mac) > 0 and mac!='00:00:00:00:00:00' order by (ibytes + obytes) desc;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Mac address info",
                                                           "value": "Mac address info",
                                                           "snapshot": True},
                                                       "win_epp_table": {
                                                           "query": "select * from win_epp_table;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Endpoint Status ",
                                                           "value": "Endpoint Status",
                                                           "snapshot": True}, "time": {
                                                           "query": "select unix_time, timestamp from time;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Current time of system",
                                                           "value": "Current time of system",
                                                           "snapshot": True}, "certificates": {
                                                           "query": "select common_name, issuer, self_signed, not_valid_after, path from certificates;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Installed certificates info",
                                                           "value": "Installed certificates info",
                                                           "snapshot": True}, "etc_hosts": {
                                                           "query": "select * from etc_hosts;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Etc hosts",
                                                           "value": "Etc hosts",
                                                           "snapshot": True}, "patches": {
                                                           "query": "select hotfix_id, description, installed_on from patches;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Installed patches",
                                                           "value": "Installed patches",
                                                           "snapshot": True},
                                                       "kva_speculative_info": {
                                                           "query": "select * from kva_speculative_info;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "snapshot": True},
                                                       "kernel_info": {
                                                           "query": "select path, version, arguments from kernel_info;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Kernel Info",
                                                           "value": "Kernel Info",
                                                           "snapshot": True},
                                                       "startup_items": {
                                                           "query": "select name, path, status from win_startup_items;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Startup Items",
                                                           "value": "Startup Items",
                                                           "snapshot": True},
                                                       "chrome_extensions": {
                                                           "query": "select identifier, version, description, path from chrome_extensions;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Chrome Extensions",
                                                           "value": "Chrome Extensions"},
                                                       "scheduled_tasks": {
                                                           "query": "select path, hidden, next_run_time, last_run_message from scheduled_tasks;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Scheduled Tasks",
                                                           "value": "Scheduled Tasks",
                                                           "snapshot": True},
                                                       "win_programs": {
                                                           "query": "select name, version from win_programs;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Programs Installed",
                                                           "value": "Programs Installed"},
                                                       "firefox_addons": {
                                                           "query": "select identifier, version, description, path from firefox_addons;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Firefox adding",
                                                           "value": "Etc hosts",
                                                           "snapshot": True},
                                                       "win_services": {
                                                           "query": "select ws.module_path,ws.path, case IfNull (ws.module_path , '') when '' then (select wh.sha1 from win_hash wh where wh.path=ws.path limit 1 )  else (select wh.sha1 from win_hash wh where wh.path=ws.module_path limit 1)  end as sha1 from win_services ws;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Windows services",
                                                           "value": "Windows services",
                                                           "snapshot": True},
                                                       "appcompat_shims": {
                                                           "query": "select ach.*,(select sha1 from win_hash wh where wh.path=ach.path limit 1 ) as sha1 from appcompat_shims ach;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "",
                                                           "value": "",
                                                           "snapshot": True},
                                                       "ie_extensions": {
                                                           "query": "select iee.path,iee.name,iee.version,(select sha1 from win_hash wh where wh.path=iee.path limit 1 ) as sha1  from ie_extensions iee;",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Internet Explorer extensions installed",
                                                           "value": "Internet Explorer extensions installed",
                                                           "snapshot": True},
                                                       "drivers": {
                                                           "query": "select d.image, d.provider, d.signed,(select sha1 from win_hash wh where wh.path=d.image limit 1 ) as sha1 from drivers d where d.provider not like '%Microsoft%' and d.image!='';",
                                                           "interval": 86400,
                                                           "platform": "windows",
                                                           "version": "2.9.0",
                                                           "description": "Drivers installed",
                                                           "value": "Drivers installed",
                                                           "snapshot": True}}}}}
    polylogyx_recon_pack_linux = {"packs": {"polylogyx_recon_pack_linux": {"platform": "linux", "version": "1.5.2",
                                                                           "queries": {"system_info": {
                                                                               "query": "select * from system_info;",
                                                                               "interval": 86400, "platform": "linux",
                                                                               "version": "2.9.0",
                                                                               "description": "System info",
                                                                               "value": "System info",
                                                                               "snapshot": True},
                                                                               "os_version": {
                                                                                   "query": "select * from os_version;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Os details",
                                                                                   "value": "Os details",
                                                                                   "snapshot": True},
                                                                               "interface_details": {
                                                                                   "query": "select ia.interface, address,  mac,ibytes, obytes from interface_details id join interface_addresses ia on ia.interface = id.interface where length(mac) > 0 and mac!='00:00:00:00:00:00' order by (ibytes + obytes) desc;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Mac address info",
                                                                                   "value": "Mac address info",
                                                                                   "snapshot": True}, "time": {
                                                                                   "query": "select unix_time, timestamp from time;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Current time of system",
                                                                                   "value": "Current time of system",
                                                                                   "snapshot": True}, "etc_hosts": {
                                                                                   "query": "select * from etc_hosts;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Etc hosts",
                                                                                   "value": "Etc hosts",
                                                                                   "snapshot": True},
                                                                               "kernel_info": {
                                                                                   "query": "select path, version, arguments from kernel_info;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Kernel Info",
                                                                                   "value": "Kernel Info",
                                                                                   "snapshot": True},
                                                                               "chrome_extensions": {
                                                                                   "query": "select identifier, version, description, path from chrome_extensions;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Chrome Extensions",
                                                                                   "value": "Chrome Extensions",
                                                                                   "snapshot": True},
                                                                               "firefox_addons": {
                                                                                   "query": "select identifier, version, description, path from firefox_addons;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Firefox adding",
                                                                                   "value": "Etc hosts",
                                                                                   "snapshot": True},
                                                                               "deb_packages": {
                                                                                   "query": "select * from deb_packages;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Debian Packages Installed",
                                                                                   "value": "Debian Packages Installed",
                                                                                   "snapshot": True},
                                                                               "rpm_packages": {
                                                                                   "query": "select * from rpm_packages;",
                                                                                   "interval": 86400,
                                                                                   "platform": "linux",
                                                                                   "version": "2.9.0",
                                                                                   "description": "Packages Installed",
                                                                                   "value": "Packages Installed",
                                                                                   "snapshot": True}}}}}
    polylogyx_recon_pack_darwin = {"packs": {"polylogyx_recon_pack_darwin": {"platform": "darwin", "queries": {
        "system_info": {"query": "select * from system_info;", "interval": 120, "platform": "darwin",
                        "version": "2.9.0",
                        "description": "System info", "value": "System info", "snapshot": True},
        "os_version": {"query": "select * from os_version;", "interval": 86400, "platform": "darwin",
                       "version": "2.9.0",
                       "description": "Os details", "value": "Os details", "snapshot": True}, "interface_details": {
            "query": "select ia.interface, address,  mac,ibytes, obytes from interface_details id join interface_addresses ia on ia.interface = id.interface where length(mac) > 0 and mac!='00:00:00:00:00:00' order by (ibytes + obytes) desc;",
            "interval": 86400, "platform": "darwin", "version": "2.9.0", "description": "Mac address info",
            "value": "Mac address info", "snapshot": True},
        "time": {"query": "select unix_time, timestamp from time;", "interval": 86400, "platform": "darwin",
                 "version": "2.9.0", "description": "Current time of system", "value": "Current time of system",
                 "snapshot": True},
        "etc_hosts": {"query": "select * from etc_hosts;", "interval": 86400, "platform": "darwin", "version": "2.9.0",
                      "description": "Etc hosts", "value": "Etc hosts", "snapshot": True},
        "kernel_info": {"query": "select path, version, arguments from kernel_info;", "interval": 86400,
                        "platform": "darwin", "version": "2.9.0", "description": "Kernel Info", "value": "Kernel Info",
                        "snapshot": True},
        "chrome_extensions": {"query": "select identifier, version, description, path from chrome_extensions;",
                              "interval": 86400, "platform": "darwin", "version": "2.9.0",
                              "description": "Chrome Extensions", "value": "Chrome Extensions", "snapshot": True},
        "firefox_addons": {"query": "select identifier, version, description, path from firefox_addons;",
                           "interval": 86400,
                           "platform": "darwin", "version": "2.9.0", "description": "Firefox adding",
                           "value": "Etc hosts",
                           "snapshot": True},
        "certificates": {"query": "select common_name, issuer, self_signed, not_valid_after, path from certificates;",
                         "interval": 86400, "platform": "darwin", "version": "2.9.0",
                         "description": "Installed certificates info", "value": "Installed certificates info",
                         "snapshot": True},
        "startup_items": {"query": "select name, path, status from win_startup_items;", "interval": 86400,
                          "platform": "darwin", "version": "2.9.0", "description": "Startup Items",
                          "value": "Startup Items", "snapshot": True}}}}}


class PolyLogyxConstants:
    DEFAULT_OPTIONS = {
        "custom_plgx_EnableLogging": "true",
        "custom_plgx_EnableSSL": "true",
        "custom_plgx_LogFileName": "C:\\Program Files\\plgx_osquery\\plgx-win-extension.log",
        "custom_plgx_LogLevel": "3",
        "custom_plgx_LogModeQuiet": "0",
        "custom_plgx_EnableWatcher": "true",
        "custom_plgx_MemoryLimit": "150",
        "schedule_splay_percent": 10,
        "custom_plgx_LogFileNameLinux": "/tmp/plgx-agent.log",
    }


class PolyLogyxServerDefaults:
    plgx_config_all_options = "plgx_config_all_options"
    plgx_config_all_settings = "plgx_config_all_settings"
    default_type = "default"
    current_ip = 'https://localhost:9000'
    BASE_URL = "/src/plgx-esp"
    POLYLOGYX_OSQUERY_SCHEMA_JSON = {}
    RECON_INTERVAL = 30


class QueryConstants:
    UNSIGNED_JSON = {"sign_info": "Unsigned"}
    PRODUCT_STATE_QUERY = '''SELECT product_type AS product_type,product_state AS product_state,SUM(sum__count) AS product_count
 FROM(SELECT product_type AS product_type, product_state AS product_state,sum(count) AS sum__count
 FROM (SELECT jsonb_array_elements(data)->>'product_type' as product_type,jsonb_array_elements(data)->>'product_state' as product_state,COUNT(jsonb_array_elements(data)->>'product_state') as count FROM node_data where name='win_epp_table' and data::TEXT !='""'::TEXT and data::TEXT !='[]'::TEXT group by product_type,product_state order by count DESC) AS expr_qry GROUP BY product_type, product_state ORDER BY sum__count DESC LIMIT 10000) AS expr_qry GROUP BY product_type, product_state ORDER BY product_count DESC LIMIT 10000;'''
    PRODUCT_SIGNATURES_QUERY = '''SELECT product_type AS product_type,product_signatures AS product_signatures,SUM(sum__count) AS product_count FROM(SELECT product_type AS product_type, product_signatures AS product_signatures,sum(count) AS sum__count FROM (SELECT jsonb_array_elements(data)->>'product_type' as product_type,jsonb_array_elements(data)->>'product_signatures' as product_signatures,COUNT(jsonb_array_elements(data)->>'product_signatures') as count FROM node_data where name='win_epp_table' and data::TEXT !='""'::TEXT and data::TEXT !='[]'::TEXT group by product_type,product_signatures order by count DESC) AS expr_qry GROUP BY product_type, product_signatures ORDER BY sum__count DESC LIMIT 10000) AS expr_qry GROUP BY product_type, product_signatures ORDER BY product_count DESC LIMIT 10000;'''


class EventQueries:
    TOTAL_FILE_EVENTS = "select count(*) from result_log where name like '%win_file_events%';"
    TOTAL_FILE_EVENTS_LINUX = "select count(*) from result_log where name like '%file_events%' and name not like '%win_file_events%' and name not like '%win_pefile_events%';"
    TOTAL_SOCKET_EVENTS_LINUX = "select count(*) from result_log where name like '%socket_events%' and name not like '%win_socket_events%';"


class UtilQueries:
    TOP_FIVE_PROGRAM = "select columns ->> 'path' as path,count(columns ->> 'path' ) as count from result_log where name like 'win_process_events' and columns ->> 'action'='PROC_CREATE' group by path order by count desc limit 5;"
    BOTTOM_FIVE_PROGRAM = "select columns ->> 'path' as path,count(columns ->> 'path' ) as count from result_log where name like 'win_process_events'  and columns ->> 'action'='PROC_CREATE' group by path order by count  limit 5;"
    TOP_FIVE_PORTS_LINUX = "SELECT columns->>'remote_port' as path, COUNT(columns->>'remote_port') as count  FROM result_log WHERE name like '%socket_events%' and name not like '%win_socket_events%' GROUP BY path ORDER BY count DESC LIMIT 5;"
    TOP_FIVE_IPS_LINUX = "SELECT columns->>'remote_address' as path, COUNT(columns->>'remote_address') as count  FROM result_log WHERE name like '%socket_events%' and name not like '%win_socket_events%' GROUP BY path ORDER BY count DESC LIMIT 5;"
    TOP_FIVE_PROGRAM_LINUX = "select columns ->> 'path' as path,count(columns ->> 'path' ) as count from result_log where name like '%process_events%' and name not like '%win_process_events%' group by path order by count desc limit 5;"
    BOTTOM_FIVE_PROGRAM_LINUX = "select columns ->> 'path' as path,count(columns ->> 'path' ) as count from result_log where name like '%process_events%' and name not like '%win_process_events%'   group by path order by count ASC  limit 5;"
    ALERT_RECON_QUERIES_JSON = {
    "scheduled_queries": [
        {
            "name": "win_file_events",
            "before_event_interval": 30,
            "after_event_interval": 60
        },
        {
            "name": "win_process_events",
            "before_event_interval": 30,
            "after_event_interval": 60
        }, {
            "name": "win_registry_events",
            "before_event_interval": 30,
            "after_event_interval": 60
        }, {
            "name": "win_socket_events",
            "before_event_interval": 30,
            "after_event_interval": 60
        }, {
            "name": "win_http_events",
            "before_event_interval": 30,
            "after_event_interval": 60
        }
    ],
    "live_queries": [
        {
            "name": "win_epp_table",
            "query": "select * from win_epp_table;"
        }
    ]
}
    UNSIGNED_JSON = {"sign_info": "Unsigned"}
    UNSIGNED_BINARY = "SELECT count(*) FROM result_log WHERE name like '%win_image_load_events%' and columns @> '" + json.dumps(UNSIGNED_JSON) + "'; "
    ETC_HOSTS_QUERY = "SELECT  count(*) AS count FROM (SELECT jsonb_array_elements(data)->>'hostnames' as hostnames FROM node_data left join node n on n.id=node_id WHERE name = 'etc_hosts' and platform = 'windows' and data::TEXT !='\"\"'::TEXT and data::TEXT !='[]'::TEXT LIMIT 1000000) AS expr_qry ;"
    ETC_HOSTS_LINUX_QUERY = "SELECT  count(*) AS count FROM (SELECT jsonb_array_elements(data)->>'hostnames' as hostnames FROM node_data left join node n on n.id=node_id WHERE name = 'etc_hosts' and platform not in ('windows','darwin') and data::TEXT !='\"\"'::TEXT and data::TEXT !='[]'::TEXT LIMIT 1000000) AS expr_qry ;"


class KernelQueries:
    MAC_ADDRESS_QUERY = "select  address, mask, mac,  description,manufacturer,connection_id,connection_status,enabled from interface_details id join interface_addresses ia on ia.interface = id.interface where length(mac) > 0 order by (ibytes + obytes) desc;"
    KERNEL_VERSION_LINUX_QUERY = '''SELECT jsonb_array_elements(data)->>'version' as version,COUNT(jsonb_array_elements(data)->>'version') as count FROM node_data left join node n on n.id=node_id WHERE name='kernel_info' and platform not in  ('windows','darwin') and data::TEXT !='""'::TEXT and data::TEXT !='[]'::TEXT GROUP BY version ORDER BY count DESC LIMIT 1000000;'''
    RMP_DEB_PACKAGES = "SELECT  count(*) AS count FROM (SELECT jsonb_array_elements(data)->>'name' as package_name FROM node_data  WHERE name in ('rpm_packages','deb_packages')  and data::TEXT !='\"\"'::TEXT and data::TEXT !='[]'::TEXT LIMIT 1000000) AS expr_qry ;"
    KERNEL_VERSION_QUERY = '''SELECT jsonb_array_elements(data)->>'version' as version,COUNT(jsonb_array_elements(data)->>'version') as count FROM node_data left join node n on n.id=node_id WHERE name='kernel_info' and platform = 'windows' and data::TEXT !='""'::TEXT and data::TEXT !='[]'::TEXT GROUP BY version ORDER BY count DESC LIMIT 1000000;'''
    CHROME_IE_EXTENSIONS_QUERY = "SELECT name AS name, count(*) AS count FROM (SELECT jsonb_array_elements(data)->>'path' as path, name FROM node_data WHERE name in ('chrome_extensions', 'ie_extensions') and data::TEXT !='\"\"'::TEXT and data::TEXT !='[]'::TEXT LIMIT 1000000) AS expr_qry GROUP BY name ORDER BY count DESC LIMIT 10000;"
    CHROME_EXTENSIONS_QUERY = "SELECT name AS name, count(*) AS count FROM (SELECT jsonb_array_elements(data)->>'path' as path, name FROM node_data WHERE name in ('chrome_extensions') and data::TEXT !='\"\"'::TEXT and data::TEXT !='[]'::TEXT LIMIT 1000000) AS expr_qry GROUP BY name ORDER BY count DESC LIMIT 10000;"
    CHROME_FIREFOX_EXTENSIONS_QUERY = "SELECT name AS name, count(*) AS count FROM (SELECT jsonb_array_elements(data)->>'path' as path, name FROM node_data left join node n on n.id=node_id WHERE name in ('chrome_extensions', 'firefox_addons') and data::TEXT !='\"\"'::TEXT and platform not in ('windows','darwin') and data::TEXT !='[]'::TEXT LIMIT 1000000) AS expr_qry GROUP BY name ORDER BY count DESC LIMIT 10000;"


class PlugInQueries:
    VIRUS_TOTAL_QUERY = "SELECT count(*) FROM virus_total WHERE detections > 0;"
    IBM_THREAT_INTEL_QUERY = "select count(*) from ibm_force_exchange ;"


class SystemInfoQueries:
    SYSTEM_STATE_QUERIES = [
        'win_epp_table',
        'patches',
        'os_version',
        'kernel_info',
        'startup_items',
        'drivers',
        'etc_hosts',
        'osquery_info',
        'wmi_cli_event_consumers',
        'wmi_script_event_consumers',
        'users',
        'uptime',
        'certificates',
        'chrome_extensions',
        'ie_extensions',
        'scheduled_tasks',
        'appcompat_shims',
        'powershell_events_script_blocks'
    ]
    SYSTEM_EVENT_QUERIES = [
        'win_file_events',
        'win_process_events',
        'win_process_open_events',
        'win_remote_thread_events',
        'win_pe_file_events',
        'win_removable_media_events',
        'win_http_events',
        'win_socket_events',
        'win_image_load_events',
        'win_dns_events',
        'win_dns_response_events',
        'win_registry_events',
        'win_ssl_events'
    ]


class DefaultInfoQueries:
    DEFAULT_QUERIES = {
    "system_info": "select * from system_info;", "os_version": "select * from os_version;",
    "interface_details": KernelQueries.MAC_ADDRESS_QUERY
}
    DEFAULT_INFO_QUERIES_FREEBSD = {
    "time": "select unix_time, timestamp from time;",
    "etc_hosts": "select * from etc_hosts;"
}
    DEFAULT_INFO_QUERIES = {
    "win_epp_table": "select * from win_epp_table;",
    "time": "select unix_time, timestamp from time;",
    "certificates": "select common_name, issuer, self_signed, not_valid_after, path from certificates;",
    "etc_hosts": "select * from etc_hosts;",
    "patches": "select hotfix_id, description, installed_on from patches;",
    "kva_speculative_info": "select * from kva_speculative_info;",
    "kernel_info": "select path, version, arguments from kernel_info;",
    "startup_items": "select name, path, status from win_startup_items;",
    "chrome_extensions": "select identifier, version, description, path from chrome_extensions;",
    "scheduled_tasks": "select path, hidden, next_run_time, last_run_message from scheduled_tasks;",
    "win_programs": "select name, version from win_programs;",
    "firefox_addons": "select identifier, version, description, path from firefox_addons;",
    "extensions": "select * from osquery_extensions;",
}
    DEFAULT_HASHES_QUERY = {
    "win_services": "select ws.module_path,ws.path, case IfNull (ws.module_path , '') when '' then (select wh.sha1 from win_hash wh where wh.path=ws.path limit 1 )  else (select wh.sha1 from win_hash wh where wh.path=ws.module_path limit 1)  end as sha1 from win_services ws;",
    "appcompat_shims": "select ach.*,(select sha1 from win_hash wh where wh.path=ach.path limit 1 ) as sha1 from appcompat_shims ach;",
    "ie_extensions": "select iee.path,iee.name,iee.version,(select sha1 from win_hash wh where wh.path=iee.path limit 1 ) as sha1  from ie_extensions iee;",
    "drivers": "select d.image, d.provider, d.signed,(select sha1 from win_hash wh where wh.path=d.image limit 1 ) as sha1 from drivers d where d.provider not like '%Microsoft%' and d.image!='';",

}
    DEFAULT_INFO_QUERIES_MACOS = {
    "time": "select unix_time, timestamp from time;",
    "chrome_extensions": "select identifier, version, description, path from chrome_extensions;",
    "kernel_info": "select path, version, arguments from kernel_info;",
    "certificates": "select common_name, issuer, self_signed, not_valid_after, path from certificates;",
    "firefox_addons": "select identifier, version, description, path from firefox_addons;",
    "etc_hosts": "select * from etc_hosts;",
    "startup_items": "select name, path, status from win_startup_items;"
}
    DEFAULT_INFO_QUERIES_LINUX = {
    "time": "select unix_time, timestamp from time;",
    "kernel_info": "select path, version, arguments from kernel_info;",
    "etc_hosts": "select * from etc_hosts;",
    "chrome_extensions": "select identifier, version, description, path from chrome_extensions;",
    "firefox_addons": "select identifier, version, description, path from firefox_addons;",
    "rpm_packages": "select * from rpm_packages;",
    "deb_packages": "select * from deb_packages;"

}
    DEFAULT_INFO_DESCRIPTION = {
        "win_epp_table": "The status of the Anti-Virus solution on your computer. If the product_state is not 'On' and 'product_signatures' are not 'Up-to-date' (wherever applicable) your computer might be at risk.",
        "win_services": "A Windows service, or a daemon on Unix, is a computer program that operates in the background and are often loaded automatically on startup. They can run even withou a user session. Below table provides a list of services running on your computer. Malwares can install themselves as service on a system to gain persistence. Clicking on the links in the <hash coulmn name>, you can get a reputation check of the services installed on your system.",
        "startup_items": "The following applications are automatically started with the launch of your system. Having too many entries in the start_up items can increase the boot time of your system. Malwares can install themselves as a start_up item on a system to gain persistence. Clicking on the links in the <hash coulmn name>, you can get a reputation check of the start_up items installed on your system.",
        "win_programs": "",
        "appcompat_shims": "Appcompat shims are created on Microsoft to be able to support compatibility of an application on various versions of the operating system without having to re-build the entire application. For more on shims (https://blogs.technet.microsoft.com/askperf/2011/06/17/demystifying-shims-or-using-the-app-compat-toolkit-to-make-your-old-stuff-work-with-your-new-stuff/). Malwares leverage shim data bases (SDBs) as a persistence mechanism. The following table lists the SDBs on your system. Clicking on the links in the <hash coulmn name>, you can get a reputation check of the shims installed on your system.",
        "scheduled_tasks": "scheuduled_tasks (or cron jobs) are the program run by a Task Scheduler component of the operating system to run specified jobs at regular intervals. Malware (https://www.csoonline.com/article/2621116/malware/malware-loves-windows-task-scheduler.html) have abused this feature of operating systems. The following table provides the various scheduled tasks configured on your system. Clicking on the links in the <hash coulmn name>, you can get a reputation check of the scheduled_tasks items installed on your system.",
        "chrome_extensions": "Malwares, specially adwares or spywares, have been disuising themselves as browser extensions, especially if the extension was not installed from the trusted stores. For more information: https://www.enisa.europa.eu/publications/info-notes/malware-in-browser-extensions. The following table lists the various Chrome extensions on your system. The same list can also be obtained by typing 'chrome://extensions/' in your Chrome's address bar. If you see anything suspicious, uninstall the extension.",
        "ie_extensions": "Malwares, specially adwares or spywares, have been disuising themselves as browser extensions, especially if the extension was not installed from the trusted stores. For more information: https://www.enisa.europa.eu/publications/info-notes/malware-in-browser-extensions. The following table lists the various IE extensions on your system. If you see anything suspicious, uninstall the extension.",
        "time": "The following table provides your system time stamp in Unix (https://en.wikipedia.org/wiki/Unix_time) and UTC (https://en.wikipedia.org/wiki/Coordinated_Universal_Time) formats. The timestamp represent the time at which the agent starts (usually every reboot time after the installation)",
        "certificates": "Digital certificates (https://en.wikipedia.org/wiki/Public_key_certificate) are used to establish the identity, and trust, of the software programs. The following table lists the various digital certifcates installed on your system, their providers, reputation, expiry date and the signer details.",
        "etc_hosts": "hosts file is used by an operating system to resolve a computer (or an internet domain) to an address. This link (https://blog.malwarebytes.com/cybercrime/2016/09/hosts-file-hijacks/) describes on how malware can make use of hosts file. The following table lists the entries in the hosts file of your computer",
        "patches": "Operating system vendors regularly release software updates and patches for their operating system. An unpatched system adds to the risk and vulnerability of the computer. For the latest cumulative list of updates released by Microsoft click here (https://support.microsoft.com/en-us/help/894199/software-update-services-and-windows-server-update-services-2018). The following table lists the updates installed on your computer",
        "kva_speculative_info": "e following table provides the presence (or absence) of mitigations for the Spectre and Meltdown vulnerabilites. To know more about fix of these vulnerabilites on Windows operating systems click here (https://support.microsoft.com/en-us/help/4073119/protect-against-speculative-execution-side-channel-vulnerabilities-in). Mitigations for Spectre - Kernel VA Shadowing. Kernel VA Shadowing Enabled (kva_shadow_enabled: 1 => Yes and 0 => No ). ----> With User pages marked global (kva_shadow_user_global: 1 => Yes and 0 => No )"
    }

    DEFAULT_VERSION_INFO_QUERIES = {
        "_osquery_version": "Snapshot query to find out the osquery running in agent",
        "_extension_version": "Snapshot query to find out the extension running in agent"
    }