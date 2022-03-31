import { Component, OnInit } from '@angular/core';
import { CommonapiService } from '../../../dashboard/_services/commonapi.service';
import { CommonVariableService } from '../../../dashboard/_services/commonvariable.service';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import swal from 'sweetalert';
import { Location } from '@angular/common';
import Swal from 'sweetalert2';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-configure-email',
  templateUrl: './configure-email.component.html',
  styleUrls: ['./configure-email.component.css']
})
export class ConfigureEmailComponent implements OnInit {

  ConfigureEmail: FormGroup;
  submitted = false;
  error: any;
  Updated = false;
  result: any;
  configured_email: any;
  conf_email: any;
  conf_recipient_data: any;
  conf_email_data: any;
  conf_password_data: any;
  conf_server_data: any;
  conf_port_data: number = 465;
  use_ssl:boolean
  EmailSubmit: any;
  EmailTest: any;
  sslConnection:boolean = false;
  tlsConnection:boolean = false;
  noneConnection:boolean = false;
  constructor(
    private fb: FormBuilder,
    private commonapi: CommonapiService,
    private commonvariable: CommonVariableService,
    private _location: Location,
    private titleService: Title,

  ) { }

  ngOnInit() {
    this.titleService.setTitle(this.commonvariable.APP_NAME+"-"+"Email Setting" );

    this.ConfigureEmail = this.fb.group({
      senderEmail: ['', Validators.required],
      senderPassword: ['', Validators.required],
      smtpServer: ['', Validators.required],
      smtpPort: ['', Validators.required],
      emailRecipients: ['', Validators.required]
    });

    this.commonapi.configuredEmail().subscribe(res => {
      this.conf_email = res;
      console.log(this.conf_email);
      this.conf_recipient_data = res.data.emailRecipients;
      this.conf_email_data = res.data.email;
      this.conf_password_data = res.data.password;
      this.conf_server_data = res.data.smtpAddress;
      this.conf_port_data = res.data.smtpPort;
      this.sslConnection=res.data.use_ssl;
      this.tlsConnection=res.data.use_tls;
      if(!this.sslConnection && !this.tlsConnection){
        this.noneConnection = true;
      }
    })
  }
  get f() { return this.ConfigureEmail.controls; }

  onSubmit() {
    this.submitted = true;
    if (this.ConfigureEmail.invalid) {
      return;
    }
    else {
      Swal.fire({
        title: 'Are you sure want to update?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#518c24',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, Update!'
      }).then((result) => {
        if (result.value) {
          Swal.fire({
            title: 'Please Wait..',
            onBeforeOpen: () => {
              Swal.showLoading()
            }
          })
          this.commonapi.UpdateconfigureEmail(this.f.senderEmail.value, this.f.senderPassword.value,
            this.f.smtpServer.value, this.f.smtpPort.value, this.f.emailRecipients.value, this.sslConnection, this.tlsConnection).subscribe(res => {
              this.EmailSubmit = res;
              Swal.close()
              if (this.EmailSubmit.status == 'failure') {
                swal({
                  icon: 'warning',
                  title: this.EmailSubmit.status,
                  text: this.EmailSubmit.message,

                })
              } else {

                  swal({
                    icon: 'success',
                    title: this.EmailSubmit.status,
                    text: this.EmailSubmit.message,
                    buttons: [false],
                    timer: 2000

                  })

                // })
              }
            });
        }
      })
    }
  }
  isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
  }
  validateEmailRecipients(emailRecipients) {
    var recipients = emailRecipients.toString();
    var emails = recipients.split(',')
    var valid = true;
    var regex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    for (var i = 0; i < emails.length; i++) {
      if (emails[i] === "" || !regex.test(emails[i].replace(/\s/g, ""))) {
        valid = false;
      }
    }
    return valid;
  }
  testEmail(arg) {
    if (arg.value.senderEmail == undefined) {
      Swal.fire({
        icon: 'warning',
        title: 'Please enter Senders email',
        showConfirmButton: false,
        timer: 2000
      })
    }
    else if (arg.value.senderPassword == undefined) {
      Swal.fire({
        icon: 'warning',
        title: 'Please enter Senders password',
        showConfirmButton: false,
        timer: 2000
      })
    }
    else if (arg.value.smtpServer == undefined) {
      Swal.fire({
        icon: 'warning',
        title: 'Please enter SMTP Server',
        showConfirmButton: false,
        timer: 2000
      })
    }
    else if (arg.value.emailRecipients == undefined) {
      Swal.fire({
        icon: 'warning',
        title: 'Please enter Email Recipients',
        showConfirmButton: false,
        timer: 2000
      })
    }

    else if (!this.isEmail(arg.value.senderEmail)) {
      Swal.fire({
        icon: 'warning',
        title: 'Please enter a valid email address',
        showConfirmButton: false,
        timer: 2000
      })
      return false;
    }
    else if (!this.validateEmailRecipients(arg.value.emailRecipients)) {
      Swal.fire({
        icon: 'warning',
        title: 'One of your email recipients is invalid. Use comma separated emails',
        showConfirmButton: false,
        timer: 2000
      })
      return false;
    }
    if (this.validateEmailRecipients(arg.value.emailRecipients)) {
      Swal.fire({
        title: 'Checking Email Credentials',
        onBeforeOpen: () => {
          Swal.showLoading()
        }
      })
      this.commonapi.TestEmail(arg.value.emailRecipients, arg.value.senderEmail, arg.value.smtpServer, arg.value.senderPassword, arg.value.smtpPort, this.sslConnection, this.tlsConnection).subscribe(res => {
        this.EmailTest = res;
        Swal.close();
        if (this.EmailTest.status == 'failure') {
          Swal.fire({
            icon: 'warning',
            title: this.EmailTest.status,
            text: this.EmailTest.message,
            showConfirmButton: false,
            timer: 2000

          })
        } else {
          // Swal.fire({
          //   icon: 'success',
          //   title: this.EmailTest.status,
          //   text: this.EmailTest.message,
          //   showConfirmButton: false,
          //   timer: 2000

          // })
          swal({
            icon: 'success',
            title: this.EmailTest.status,
            text: this.EmailTest.message,
            buttons: [false],
            timer: 2000

          })
        }
      })
    }
  }
  numberOnly(event): boolean {
    const charCode = (event.which) ? event.which : event.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
      return false;
    }
    return true;
  }

  goBack() {
    this._location.back();
  }

  clearForm() {
    this.submitted = false;
    this._location.back();
    setTimeout(() => {
      this.conf_port_data = 465;
    }, 100);
  }
}
