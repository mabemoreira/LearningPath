import { bootstrapApplication } from '@angular/platform-browser';
import {
    provideHttpClient,
    withInterceptorsFromDi,
} from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

// Combine the configurations
const combinedConfig = {
    ...appConfig,
    providers: [
        ...(appConfig.providers || []), // Ensure any existing providers from appConfig are included
        provideHttpClient(withInterceptorsFromDi()), provideAnimationsAsync(),
    ],
};

bootstrapApplication(AppComponent, combinedConfig).catch((err) =>
    console.error(err)
);
