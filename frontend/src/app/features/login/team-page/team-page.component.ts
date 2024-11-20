import { Component } from '@angular/core';

@Component({
    selector: 'app-team-page',
    standalone: true,
    imports: [],
    templateUrl: './team-page.component.html',
    styleUrl: './team-page.component.css',
})

export class TeamPageComponent {
    team = [
        {
          name: 'Pessoa',
          description: 'Culpa deserunt sint deserunt duis. Dolore qui eu aliquip labore.',
          githubLink: '#',
          linkedinLink: '#',
        },
        {
          name: 'Pessoa',
          description: 'Culpa deserunt sint deserunt duis. Dolore qui eu aliquip labore.',
          githubLink: '#',
          linkedinLink: '#',
        },
        {
          name: 'Pessoa',
          description: 'Culpa deserunt sint deserunt duis. Dolore qui eu aliquip labore.',
          githubLink: '#',
          linkedinLink: '#',
        },
        {
          name: 'Pessoa',
          description: 'Culpa deserunt sint deserunt duis. Dolore qui eu aliquip labore.',
          githubLink: '#',
          linkedinLink: '#',
        },
        {
          name: 'Pessoa',
          description: 'Culpa deserunt sint deserunt duis. Dolore qui eu aliquip labore.',
          githubLink: '#',
          linkedinLink: '#',
        },
      ];
    }

