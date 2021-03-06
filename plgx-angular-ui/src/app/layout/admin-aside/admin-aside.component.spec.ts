import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminAsideComponent } from './admin-aside.component';

describe('AdminAsideComponent', () => {
  let component: AdminAsideComponent;
  let fixture: ComponentFixture<AdminAsideComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdminAsideComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminAsideComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
