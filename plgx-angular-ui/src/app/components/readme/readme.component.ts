import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { CommonVariableService } from '../../dashboard/_services/commonvariable.service';
import { Location } from '@angular/common';

@Component({
  selector: 'app-readme',
  templateUrl: './readme.component.html',
  styleUrls: ['./readme.component.css']
})
export class ReadmeComponent implements OnInit {

  cpt_down:any;
  route: string;
  currentURL='';
  ProjectName=this.commonvariable.APP_NAME
  Version=this.commonvariable.version_in_readme_content
  Windows_plgx_cpt_exe=this.commonvariable.Windows_plgx_cpt_exe
  Linux_plgx_cpt=this.commonvariable.Linux_plgx_cpt
  Darwin_plgx_cpt_sh=this.commonvariable.Darwin_plgx_cpt_sh
  Windows_x64_plgx_osqueryd_exe=this.commonvariable.Windows_x64_plgx_osqueryd_exe
  Windows_x64_plgx_win_extension_ext_exe=this.commonvariable.Windows_x64_plgx_win_extension_ext_exe
  Windows_x86_plgx_osqueryd_exe=this.commonvariable.Windows_x86_plgx_osqueryd_exe
  Linux_plgx_osqueryd=this.commonvariable.Linux_plgx_osqueryd
  Linux_plgx_linux_extension_ext=this.commonvariable.Linux_plgx_linux_extension_ext
  CopyRightYear=this.commonvariable.CopyRightYear
  constructor(
    private _Activatedroute:ActivatedRoute,
    private router: Router,
    private commonvariable: CommonVariableService,
  ) { }

  ngOnInit() {
  }

  downloadFile(e,val){
    this.currentURL = window.location.href;
    let toArray = this.currentURL.split(':');
    this.cpt_down = toArray[0] + ":" + toArray[1] + ":9000/downloads/" + val;
    // this.cpt_down = "https://13.232.172.29:9000/downloads/" + val;
    console.log("url",this.cpt_down);
    window.open(this.cpt_down,'_blank');
  }

}
