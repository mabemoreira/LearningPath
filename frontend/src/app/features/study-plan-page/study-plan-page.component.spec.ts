import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyPlanPageComponent } from './study-plan-page.component';

describe('StudyPlanPageComponent', () => {
  let component: StudyPlanPageComponent;
  let fixture: ComponentFixture<StudyPlanPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudyPlanPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StudyPlanPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
