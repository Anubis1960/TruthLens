import { Component, Input } from '@angular/core';
import { Message } from '../../utils/message';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-message-panel',
  standalone: false,
  templateUrl: './message-panel.component.html',
  styleUrl: './message-panel.component.css',
  providers: [DatePipe]
})
export class MessagePanelComponent {
  @Input() messages: Message[] = [];
  
  constructor(private datePipe: DatePipe) {}

  trackById(index: number, message: Message): string {
    return message.id;
  }
  formatDate(date: Date): string {
    return this.datePipe.transform(date, 'short') || '';
  }
}
