import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { MatDialog } from '@angular/material/dialog'
import { LoginModalComponent } from '../../login-modal/login-modal.component';
import { CommonModule } from '@angular/common';
import { LoginService } from '../../../shared/services/login.service';
import { environment } from '../../../../environments/environment';

@Component({
    selector: 'app-header',
    standalone: true,
    imports: [
        RouterLink,
        CommonModule,
    ],
    templateUrl: './header.component.html',
    styleUrl: './header.component.css',
})
export class HeaderComponent {
    nav_bar_paths: NavBarPath[] = [
        {
            name: 'produto',
            active: false,
        },
        {
            name: 'equipe',
            active: false,
        },
        {
            name: 'planos',
            active: false,
        }
    ];

    get userIsLoggedIn(): boolean {
        return !!localStorage.getItem('auth-token');
    }

    constructor(
        public dialog: MatDialog,
        public loginService: LoginService,
        public router: Router,
    ) { }

    public openLoginModal(): void {
        this.dialog.open(
            LoginModalComponent
        ).afterClosed().subscribe();
    }

    private get_path(requested_path: string): NavBarPath | undefined {
        return this.nav_bar_paths.find((path) => requested_path === path.name);
    }

    activate_path(path: string): void {
        for (const path_ of this.nav_bar_paths) {
            if (path_.name === path) {
                path_.active = true;
            } else {
                path_.active = false;
            }
        }
    }

    am_i_active(path: string): string {
        const curr_path = this.get_path(path);

        if (curr_path && curr_path.active) {
            return 'active';
        }

        return '';
    }

    logout(): void {
        this.loginService.logout().subscribe(_ => {
            localStorage.removeItem(environment.AuthToken);
            this.router.navigate(['']);
        });
    }
}

interface NavBarPath {
    name: string;
    active: boolean;
}
