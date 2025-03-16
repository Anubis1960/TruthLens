import { Component, OnInit } from '@angular/core';
import { NewsService } from '../../services/news.service';
import { News } from '../../utils/news';

@Component({
  selector: 'app-news',
  standalone: false,
  templateUrl: './news.component.html',
  styleUrls: ['./news.component.css']
})
export class NewsComponent implements OnInit {
  selectedMsg?: News;  // Make sure selectedMsg is typed as News
  news: News[] = [];  // Array of News objects
  Object = Object;  // Expose the global Object to the template

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.fetchNews();
  }

  fetchNews(): void {
    this.newsService.fetchNews().subscribe(
      (data: any[]) => {
        this.news = data.map(item => ({
          domain: item.domain,
          articles: item.articles,  // Ensure this is of type { [key: string]: string }
          stats: item.stats
        }));
        // Set default selected message to the first news item
        if (this.news.length > 0) {
          this.selectedMsg = this.news[0];
        }
      },
      (error) => {
        console.error('Error fetching news:', error);
      }
    );
  }

  onMessageSelected(message: News): void {
    this.selectedMsg = message;
  }
}