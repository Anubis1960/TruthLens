import { Component } from '@angular/core';
import { Message } from '../../utils/message';
import { v4 as uuidv4} from 'uuid';
@Component({
  selector: 'app-chatbot',
  standalone: false,
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
  data: Message[] = [];
  showChatbot: boolean = false;

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
    // Simulate bot response after 1 second
    setTimeout(() => {
      const botMessageObj: Message = {
        id: uuidv4(),
        sender: 'bot',
        content: 'This is a bot response.',
        dateTime: new Date(),
      };
      this.data.push(botMessageObj);
    }, 1000);
  }
}
