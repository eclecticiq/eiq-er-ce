import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangeUserPasswordComponent } from './change-user-password.component';

describe('ChangeUserPassowrdComponent', () => {
  let component: ChangeUserPasswordComponent;
  let fixture: ComponentFixture<ChangeUserPasswordComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChangeUserPasswordComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChangeUserPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
