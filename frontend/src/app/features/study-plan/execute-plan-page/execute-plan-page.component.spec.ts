import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExecutePlanPageComponent } from './execute-plan-page.component';

describe('ExecutePlanPageComponent', () => {
  let component: ExecutePlanPageComponent;
  let fixture: ComponentFixture<ExecutePlanPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExecutePlanPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExecutePlanPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
