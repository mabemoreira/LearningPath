import { Component } from '@angular/core';

@Component({
  selector: 'app-study-plan-page',
  standalone: true,
  imports: [],
  templateUrl: './study-plan-page.component.html',
  styleUrl: './study-plan-page.component.css'
})
export class StudyPlanPageComponent {
  studyPlan = {
    name: "Plano",
    topics: [
      {
        name: "Tópico",
        done: true,
      },
    ]
  };


}
