import { Component, OnInit } from '@angular/core';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: true,
  imports: [CommonModule],
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  data: any;
  postData: any = { key: 'value' }; // Example POST data

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.getData();
  }

  getData(): void {
    this.dataService.getData().subscribe({
      next: (response) => {
        this.data = response;
      },
      error: (error) => {
        console.error('Error fetching data', error);
      },
      complete: () => {
        console.log('Data fetch complete');
      }
    });
  }

  postDataToServer(): void {
    this.dataService.postData(this.postData).subscribe({
      next: (response) => {
        console.log('Data posted successfully', response);
      },
      error: (error) => {
        console.error('Error posting data', error);
      },
      complete: () => {
        console.log('Data post complete');
      }
    });
  }
}
