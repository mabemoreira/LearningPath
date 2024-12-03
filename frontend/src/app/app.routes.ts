import { Routes } from '@angular/router';
import { HomepageComponent } from './features/login/homepage/homepage.component';
import { ProductPageComponent } from './features/login/product-page/product-page.component';
import { TeamPageComponent } from './features/login/team-page/team-page.component';
import { PlanPageComponent } from './features/login/plan-page/plan-page.component';

export const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: HomepageComponent },
    { path: 'produto', component: ProductPageComponent },
    { path: 'equipe', component: TeamPageComponent },
    { path: 'planos', component: PlanPageComponent }
];
