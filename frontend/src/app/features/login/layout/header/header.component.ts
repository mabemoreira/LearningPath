import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-header',
    standalone: true,
    imports: [RouterLink],
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
    ];

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
}

interface NavBarPath {
    name: string;
    active: boolean;
}
