import { Component } from '@angular/core';
import { HeaderComponent } from './features/layout/header/header.component';
import { RouterOutlet } from '@angular/router';
import { FooterComponent } from './features/layout/footer/footer.component';

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
