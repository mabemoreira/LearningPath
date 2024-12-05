import { Routes } from '@angular/router';
import { HomepageComponent } from './features/homepage/homepage.component';
import { ProductPageComponent } from './features/product-page/product-page.component';
import { TeamPageComponent } from './features/team-page/team-page.component';
import { PlanPageComponent } from './features/study-plan/plan-page/plan-page.component';
import { StudyPlanComponent } from './features/study-plan/study-plan/study-plan.component';
import { TopicModalComponent } from './features/study-plan/topic-modal/topic-modal.component';
import { ExecutePlanPageComponent } from './features/study-plan/execute-plan-page/execute-plan-page.component';

export const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: HomepageComponent },
    { path: 'produto', component: ProductPageComponent },
    { path: 'equipe', component: TeamPageComponent },
    { path: 'planos', component: PlanPageComponent },
    { path: 'planos/:id', component: StudyPlanComponent },
    { path: 'planos/:id/executar', component: ExecutePlanPageComponent },
];
