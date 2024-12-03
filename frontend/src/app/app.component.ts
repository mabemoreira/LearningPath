import { Component } from '@angular/core';
import { HeaderComponent } from './features/login/layout/header/header.component';
import { RouterOutlet } from '@angular/router';
import { ApiService } from './api.service';
import { FooterComponent } from './features/login/layout/footer/footer.component';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [HeaderComponent, RouterOutlet, FooterComponent],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent {
    title = 'Learning Path';
}
