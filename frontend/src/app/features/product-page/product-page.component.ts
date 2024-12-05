import { Component } from '@angular/core';
import { HeaderComponent } from '../login/layout/header/header.component';
import { FooterComponent } from '../login/layout/footer/footer.component';

@Component({
    selector: 'app-product-page',
    standalone: true,
    imports: [HeaderComponent, FooterComponent],
    templateUrl: './product-page.component.html',
    styleUrl: './product-page.component.css',
})
export class ProductPageComponent {/*...*/}