import { Component } from '@angular/core';

@Component({
    selector: 'app-team-page',
    standalone: true,
    imports: [],
    templateUrl: './team-page.component.html',
    styleUrl: './team-page.component.css',
})

export class TeamPageComponent {
        teamMembers = [
          {
            name: 'Henrique Parede',
            description: 'Um apreciador de café, Star Wars e dormir tarde',
            avatar: 'assets/github-icon.svg',
            github: 'https://github.com/pessoa1',
            linkedin: 'https://linkedin.com/in/pessoa1'
          },
          {
            name: 'Maria Beatriz Moreira',
            description: 'Cinéfila, amante de livros e esfomeada',
            avatar: 'assets/avatar2.jpg',
            github: 'https://github.com/pessoa2',
            linkedin: 'https://linkedin.com/in/pessoa2'
          },

          {
            name: 'Pedro Brasil',
            description: 'Um fã de jogar durante as aulas',
            avatar: 'assets/avatar2.jpg',
            github: 'https://github.com/pessoa2',
            linkedin: 'https://linkedin.com/in/pessoa2'
          },

          {
            name: 'Thiago Camargo',
            description: 'Ama cachorros',
            avatar: 'assets/avatar2.jpg',
            github: 'https://github.com/pessoa2',
            linkedin: 'https://linkedin.com/in/pessoa2'
          },

          {
            name: 'Raphael Salles',
            description: 'Tem uma apreciação única por banhos',
            avatar: 'assets/avatar2.jpg',
            github: 'https://github.com/pessoa2',
            linkedin: 'https://linkedin.com/in/pessoa2'
          }
        ];
      }

