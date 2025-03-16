import { Component } from '@angular/core';
import { Message } from '../../utils/message';
import { v4 as uuidv4} from 'uuid';
import {HttpClient, HttpParams} from '@angular/common/http';
@Component({
  selector: 'app-chatbot',
  standalone: false,
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  data: Message[] = [];
  showChatbot: boolean = false;

  constructor(private http: HttpClient) {
  }

  toggleChatbot() {
    this.showChatbot = !this.showChatbot;
  }

  getMessage($event: string) {
    let messageObj: Message = {
      id: uuidv4(),
      sender: "user",
      content: $event,
      dateTime: new Date()
    }
    this.data.push(messageObj);

    const body = {
      prompt: $event
    }

    this.http.post('http://localhost:5000/api/chat/send', body).subscribe({
      next: (data: any) => {

        let response = data['response'];

        const botMessageObj: Message = {
          id: uuidv4(),
          sender: 'bot',
          content: response,
          dateTime: new Date(),
        };
        this.data.push(botMessageObj);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }
}
