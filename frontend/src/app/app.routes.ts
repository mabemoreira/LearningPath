import { Routes } from '@angular/router';
import { HomepageComponent } from './features/homepage/homepage.component';
import { ProductPageComponent } from './features/product-page/product-page.component';
import { TeamPageComponent } from './features/team-page/team-page.component';
import { StudyPlanPageComponent } from './features/study-plan-page/study-plan-page.component';
export const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: HomepageComponent },
    { path: 'produto', component: ProductPageComponent },
    { path: 'equipe', component: TeamPageComponent },
    { path: 'planos/:id', component: StudyPlanPageComponent },
];