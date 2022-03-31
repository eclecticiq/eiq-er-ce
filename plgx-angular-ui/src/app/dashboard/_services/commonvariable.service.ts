import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CommonVariableService {
  APP_NAME="EclecticIQ"
  Version="CE 3.0"
  version_in_readme_content="3.0"
  CopyRightYear='2021'
  Windows_plgx_cpt_exe={'version':"v3.0.0","MD5_checksum":"1e10f94937d844a9edb99a92db359226"}
  Linux_plgx_cpt={'version':"v3.0.0","MD5_checksum":"0597fdc55f5f1c0244500930c930e7c1"}
  Darwin_plgx_cpt_sh={'version':"-","MD5_checksum":"4899f3b203d63acef7e5ac633660040d"}
  Windows_x64_plgx_osqueryd_exe={'version':"4.0.2","MD5_checksum":"1271fe50a8493618b6f0029b293d8826"}
  Windows_x64_plgx_win_extension_ext_exe={'version':"v3.0.0","MD5_checksum":"3af2fdffb907da582c2cb3eb2b67d75d"}
  Windows_x86_plgx_osqueryd_exe={'version':"3.2.6","MD5_checksum":"6b007b7a1c86252d993094c4a425558f"}
  Linux_plgx_osqueryd={'version':"4.3.0","MD5_checksum":"47bb0f8c8cafd1cc147b964a8d39b80c"}
  Linux_plgx_linux_extension_ext={'version':"v1.0.40.2","MD5_checksum":"121157d0db89c8fdb060d9bc3ea45743"}
  constructor() { }
}
