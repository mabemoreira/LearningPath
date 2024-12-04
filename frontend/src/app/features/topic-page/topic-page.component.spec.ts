import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicPageComponent } from './topic-page.component';

describe('TopicPageComponent', () => {
  let component: TopicPageComponent;
  let fixture: ComponentFixture<TopicPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopicPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TopicPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
