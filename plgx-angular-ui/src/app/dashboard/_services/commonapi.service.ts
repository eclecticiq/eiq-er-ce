import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpInterceptor, HttpParams} from '@angular/common/http';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../../environments/environment'
import { map } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class CommonapiService {

  constructor(private http: HttpClient) { }
  public Dashboard(){
      return this.http.get(environment.api_url+"/dashboard");
  }
  public Hosts_count(){
      return this.http.get(environment.api_url+"/hosts/count");
  }

  public alerts_graph_api(source,duration,type,date){
    return this.http.get(environment.api_url+"/alerts/graph?source="+source+"&duration="+duration+"&type="+type+"&date="+date);
}
public alerts_graph_api_filter_with_Host_identifier(source,duration,type,date,host_identifier){
  return this.http.get(environment.api_url+"/alerts/graph?source="+source+"&duration="+duration+"&type="+type+"&date="+date+"&host_identifier="+host_identifier);
}
  public alerts_source_count_api(){
    return this.http.get(environment.api_url+"/alerts/count_by_source");
  }
  public alerts_source_count_api_Host_identifier(host_identifier){
    return this.http.get(environment.api_url+"/alerts/count_by_source?host_identifier="+host_identifier);
  }
  public  alerts_source_count_api_resolved(){
    return this.http.get(environment.api_url+"/alerts/count_by_source?resolved=true");
  }
  public Hosts_main(){
      return this.http.post(environment.api_url+"/hosts", {"alerts_count":false});
  }
  public hostsnames_main(){
      return this.http.post(environment.api_url+"/hosts", {'platform':'windows'});
  }
  public hosts_filter(status, platform){
    return this.http.post(environment.api_url+"/hosts", {'status': status, 'platform':platform});
  }

  public host_name_api(node_id){
      let urlop = environment.api_url+"/hosts/";
      return this.http.get(urlop + node_id);
  }
  public additional_config_api(node_id){
      return this.http.post(environment.api_url+"/hosts/additional_config", {'node_id' : node_id});
  }
  public view_config_api(node_id){
    return this.http.post(environment.api_url+"/hosts/config", {'node_id' : node_id});
}
  public recent_activity_count_api(id){
      return this.http.post(environment.api_url+"/hosts/recent_activity/count", {'node_id' : id});
  }

  public recent_activity_data_api(query_name, query_id){
      let param3 = localStorage.getItem('activity_nodekey');
      return this.http.post(environment.api_url+"/hosts/recent_activity", {'node_id' : param3, 'query_name': query_name, 'start': 0, 'limit':query_id});
  }
  public iocs_api(){
      return this.http.get(environment.api_url+"/iocs");
  }

  public rules_api(){
      return this.http.post(environment.api_url+"/rules",{});
  }
  public edit_rule_api(rules_id,object){
    let rule_url = environment.api_url+"/rules/";
    return this.http.post(rule_url + rules_id,object);
  }
  public ruleadd_api(object){
    return this.http.post(environment.api_url+"/rules/add",object);
  }
  public update_rule_api(rule_id){
    let urlop = environment.api_url+"/rules/";
    return this.http.get(urlop + rule_id);
  }
  public rule_alerts_export(object){
  return this.http.post(environment.api_url+"/alerts/alert_source/export",object,{ responseType: "blob",headers: { 'Content-Type': 'application/json' }});
}
  public packs_api(){
      return this.http.post(environment.api_url+"/packs",{});
  }

  public update_queries_in_pack_api(queries_id,object){
    let urlop = environment.api_url+"/queries/";
    return this.http.post(urlop + queries_id,object,{ headers: { 'Content-Type': 'application/json' }});
  }
  public queries_api(){
      return this.http.post(environment.api_url+"/queries",{});
  }

  public queriesadd_api(object){
      return this.http.post(environment.api_url+"/queries/add",object);
  }
  public update_queries_in_query_api(queries_id,object){
    let urlop = environment.api_url+"/queries/";
    return this.http.post(urlop + queries_id,object,{ headers: { 'Content-Type': 'application/json' }});
  }
  public Alert_data(alert_id){
    let urlop = environment.api_url+"/alerts/";
    return this.http.get(urlop + alert_id);
  }

  public Alert_system_events_and_state_data(alert_id){
    let urlop = environment.api_url+"/alerts/"+alert_id+"/events";
    return this.http.get(urlop);
  }
  public get_alerts_aggregated_data(alert_id){
    let urlop = environment.api_url+"/alerts/"+alert_id+"/alerted_events";
    return this.http.get(urlop);
  }

  public Alerts(alertName, alertCount){
      return this.http.post(environment.api_url+"/alerts", {'source': alertName, 'startPage': 0, 'perPageRecords': alertCount });
  }
  public AlertsResolve(alerts_data){
    let urlresolve = environment.api_url+"/alerts";
    return this.http.put(urlresolve,alerts_data);
  }
  public DisableHost(host_id){
    let urlresolve = environment.api_url+"/hosts/";
    let url_file = (urlresolve + host_id + "/delete");
    return this.http.put(url_file, {});
  }
  public hosts_enablenodes_api(host_id){
    let urlresolve = environment.api_url+"/hosts/";
    let url_file = (urlresolve + host_id + "/enable");
    return this.http.put(url_file, {});
  }
  public Alerts_data_count(){
    return this.http.post(environment.api_url+"/alerts", {'startPage': 0,'limit':10});
}
  public get_Query_data(query_id){
    let urlop = environment.api_url+"/queries/";
    return this.http.get(urlop + query_id);
  }
  public Openc2_api(){

      return this.http.post(environment.api_url+"/response",{});
  }
  // Start Management
  public changePassword(Old_password, New_password, Confirm_new_password){
      return this.http.post(environment.api_url+"/management/changepw",
        {
          'old_password': Old_password,
          'new_password': New_password,
          'confirm_new_password': Confirm_new_password
        }
      );
  }

  public configuredEmail(){
      return this.http.get<any>(environment.api_url+"/email/configure");
  }
  public UpdateconfigureEmail(SenderEmail, SenderPassword, SmtpAddress, SmtpPort, EmailRecipients, use_ssl, use_tls){
      return this.http.post(environment.api_url+"/email/configure",
        {
          "emailRecipients": EmailRecipients,
          "email": SenderEmail,
          "smtpAddress": SmtpAddress,
          "password": SenderPassword,
          "smtpPort": SmtpPort,
          "use_ssl":use_ssl,
          "use_tls":use_tls
        }
      );
  }
  public TestEmail(EmailRecipients, SenderEmail, SmtpAddress, SenderPassword, SmtpPort, use_ssl, use_tls){
    return this.http.post(environment.api_url+"/email/test",
    {
      "emailRecipients": EmailRecipients,
      "email": SenderEmail,
      "smtpAddress": SmtpAddress,
      "password": SenderPassword,
      "smtpPort": SmtpPort,
      "use_ssl":use_ssl,
      "use_tls":use_tls
    }
    );
  }

  public updatePurgeData(NumberOfDays){
      return this.http.post(environment.api_url+"/management/purge/update",
        {
          'days': NumberOfDays
        }
      );
  }
  public getPurgeData(){
    return this.http.get(environment.api_url+"/management/purge/update");
  }
  public getConfigurationSettings(){
    return this.http.get<any>(environment.api_url+"/management/settings");
}
public putConfigurationSettings(Purge_Duration,Alert_Aggregation_Duration,){
  return this.http.put(environment.api_url+"/management/settings",
 { "purge_data_duration": Purge_Duration,
    "alert_aggregation_duration": Alert_Aggregation_Duration
  }
  );
}
public getAntiVirusEngines(){
  return this.http.get(environment.api_url+"/management/virustotal/av_engine");
}
public postAntiVirusEngines(data){
  return this.http.post(environment.api_url+"/management/virustotal/av_engine",data);
}

  // END Management

  public carves_api(){
    return this.http.post(environment.api_url+"/carves", {});
}
public carves_download_api(carves_id){

  let urlop = environment.api_url+"/carves/download/";
  return this.http.get(urlop + carves_id,{responseType: "blob",reportProgress:true,observe:"events"});
  //return this.http.get(urlop + carves_id,{responseType: "blob", headers: {'Accept': 'application/tar'}});
  }
public carves_delete_api(session_id){
  return this.http.post(environment.api_url+"/carves/delete", {"session_id": session_id});
}

public yara_add_api(file_data: File){
      var uploadData = new FormData();
      uploadData.append('file', file_data[0], file_data[0].name);
      console.log(uploadData);
    return this.http.post(environment.api_url+"/yara/add", uploadData);
}
public yara_view_api(event_type){
    return this.http.post(environment.api_url+"/yara/view", {"file_name": event_type});
}
public yara_delete_api(yara_name){
    return this.http.post(environment.api_url+"/yara/delete", {"file_name": yara_name});
}
public yara_api(){
    return this.http.get(environment.api_url+"/yara");
}

public ioc_api(){
    return this.http.get(environment.api_url+"/iocs");
}
public ioc_update_api(object){
  console.log("IOC_services",environment.api_url+"/iocs/add",object);
return this.http.post(environment.api_url+"/iocs/add",object);
}
public status_log(res_id){
  return this.http.post(environment.api_url+"/hosts/status_logs", {"node_id" : res_id});
}
public hosts_export(){
  return this.http.get(environment.api_url+"/hosts/export",{ headers: { 'Content-Type': 'text/csv;charset=utf-8;' }});
}

public response_action(res_id){
    return this.http.post(environment.api_url+"/response/status", {"node_id" : res_id});
}
public Distrbuted_row(res_id){
    return this.http.post(environment.api_url+"/distributed/add", {"node_id" : res_id});
}

public Hosts_data(){
    return this.http.post(environment.api_url+"/hosts", {"status":true, "alerts_count":false});
}
public Apikey_data(){
    return this.http.get(environment.api_url+"/management/apikeys");
}
public Apikey_postdata(ibmxForceKey,ibmxForcePass,vt_key,alienVaultOTXKey){
    return this.http.post(environment.api_url+"/management/apikeys",{"IBMxForceKey":ibmxForceKey,"IBMxForcePass":ibmxForcePass,"vt_key":vt_key,"otx_key":alienVaultOTXKey});
}

public Response_agent_update(user_name, password,type, target, actuator_id,){
  console.log(user_name,password,type, actuator_id, target)
  return this.http.post(environment.api_url+"/response/add",{
    "action": "upgrade",
    "actuator_id": actuator_id,
    "host_user":user_name,
    "host_password": password,
    "type":type,
    "target": target
  });
}

public Response_agent_uninstall(user_name, password,type, actuator_id){
  console.log(user_name,password,type, actuator_id)
  return this.http.post(environment.api_url+"/response/agent_uninstall",{
    "host_identifier": actuator_id,
    "user":user_name,
    "password": password,
    "type":type,
  });
}

  public update_queries_api(queries_id){
      let urlop = environment.api_url+"/queries/";
      return this.http.get(urlop + queries_id);
  }

  public configs_api(){
    return this.http.get(environment.api_url+"/configs/all");
  }
  public configs_api_shallow_deep_update(update_data){
    return this.http.put(environment.api_url+"/configs/toggle",update_data);
  }
  public options_api(){
    return this.http.get(environment.api_url+"/options");
}
public options_upload(object){
return this.http.post(environment.api_url+"/options/add",object);
}

public associated_api(){
return this.http.post(environment.api_url+"/queries/packed", {});
}
public config_upload(object){
  return this.http.post(environment.api_url+"/configs/update", object);
  }
  public pack_upload_api(file_data: File, category_val){
    console.log(file_data);
    var pack_uploadData = new FormData();
    pack_uploadData.append('category',category_val);
    pack_uploadData.append('file', file_data[0], file_data[0].name);

    return this.http.post(environment.api_url+"/packs/upload", pack_uploadData);
  }

  public Queries_add_api(object){
    console.log("Payload is ",object);
    return this.http.post(environment.api_url+"/distributed/add", object);
  }

  public live_Queries_tables_schema(){
    return this.http.get(environment.api_url+"/schema?export_type=json");
}
  //Begin:: Tags
   public Tags_data(){
     return this.http.get(environment.api_url+"/tags");
   }
   public tags_api(){
     return this.http.get(environment.api_url+"/tags");
   }
   public add_tags_api(tags_val){
     console.log(tags_val);
      return this.http.post(environment.api_url+"/tags/add", {'tag':tags_val});
   }
   public delete_tags_api(tags_val){
     return this.http.post(environment.api_url+"/tags/delete",{"tag":tags_val});
   }
   //Host
   public hosts_addtag_api(node_id,tags){
     let urlop = environment.api_url+"/hosts/";
     let tags_list = tags.split(',');
     return this.http.post(urlop + node_id + '/tags', {'tag':tags_list[tags_list.length-1]});
   }
   public hosts_removetags_api(node_id,tag){
     let urlop = environment.api_url+"/hosts/";
     const options = {
       headers: new HttpHeaders({
         'Content-Type': 'application/json',
       }),
       body: {
         "tag":tag
       }
     };
     return this.http.delete(urlop + node_id + '/tags', options);
   }
   //Packs
   public packs_addtag_api(pack_id,tags){
     let urlop = environment.api_url+"/packs/";
     let tags_list = tags.split(',');
     return this.http.post(urlop + pack_id + '/tags', {'tag':tags_list[tags_list.length-1]});
   }
   public packs_removetags_api(pack_id,tag){
     let urlop = environment.api_url+"/packs/";
     const options = {
       headers: new HttpHeaders({
         'Content-Type': 'application/json',
       }),
       body: {
         "tag":tag
       }
     };
     return this.http.delete(urlop + pack_id + '/tags', options);
   }
   //Queries
   public queries_addtag_api(query_id,tags){
     let urlop = environment.api_url+"/queries/";
     let tags_list = tags.split(',');
     return this.http.post(urlop + query_id + '/tags', {'tag':tags_list[tags_list.length-1]});
   }
   public queries_removetags_api(query_id,tag){
     let urlop = environment.api_url+"/queries/";
     const options = {
       headers: new HttpHeaders({
         'Content-Type': 'application/json',
       }),
       body: {
         "tag":tag
       }
     };
     return this.http.delete(urlop + query_id + '/tags', options);
   }
   //Tagged
   public tagged_api(tags_val){
     return this.http.post(environment.api_url+"/tags/tagged", {"tags":tags_val});
   }
   public host_tagged_api(hosttags_val){
     return this.http.post(environment.api_url+"/hosts/tagged", {"tags":hosttags_val});
   }
   public pack_tagged_api(packtags_val){
     return this.http.post(environment.api_url+"/packs/tagged", {"tags":packtags_val});
   }
   public query_tagged_api(qrytags_val){
     return this.http.post(environment.api_url+"/queries/tagged", {"tags":qrytags_val});
   }
   //End:: Tags

   public search_csv_export(object){

    return this.http.post(environment.api_url+"/hosts/search/export",object,{responseType: "blob", headers: {'Accept': 'application/csv'}});
    }

    public alerts_export(object){
      return this.http.post(environment.api_url+"/alerts/alert_source/export",object,{responseType: "blob", headers: {'Accept': 'application/csv'}});
    }

    public recent_activity_search_csv_export(object){

    return this.http.post(environment.api_url+"/hosts/search/export",object,{responseType: "blob", headers: {'Accept': 'application/csv'}});
    }
    public Alerted_entry(alert_id){
      let urlop = environment.api_url+"/alerts/";
      return this.http.get(urlop + alert_id);
    }
    public cpt_upgrade_api(host_identifier){
      return this.http.post(environment.api_url+"/response/agent_uninstall", {"host_identifier":host_identifier});
    }

    public delete_host(host_id){
      let urlop = environment.api_url+"/hosts/";
     const options = {
       headers: new HttpHeaders({
         'Content-Type': 'application/json',
       })
     };
     return this.http.delete(urlop + host_id + '/delete', options);

    }
    public deleteApipacks(pack_id){
      let urlop = environment.api_url+"/packs/";
     const options = {
       headers: new HttpHeaders({
         'Content-Type': 'application/json',
       })
     };
     return this.http.delete(urlop + pack_id + '/delete', options);
    }
    public deleteApiQueries(query_id){
      let urlop = environment.api_url+"/queries/";
     const options = {
       headers: new HttpHeaders({
         'Content-Type': 'application/json',
       })
     };
     return this.http.delete(urlop + query_id + '/delete', options);

    }

    public Host_rules_api(id){
      const options = {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        })
      };
        return this.http.get(environment.api_url+"/hosts/"+id+"/alerts/distribution",options);
    }


}
