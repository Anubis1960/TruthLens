import { Component, EventEmitter, Output, ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-user-input',
  standalone: false,
  templateUrl: './user-input.component.html',
  styleUrl: './user-input.component.css'
})
export class UserInputComponent {
  @Output() sendMessageEmitter = new EventEmitter<string>()
  message: string = ""

  @ViewChild('chatContainer') chatContainer!: ElementRef;

  sendMessage() {
    if (this.message.trim()) {
      this.sendMessageEmitter.emit(this.message);
      this.message = '';
      setTimeout(() => this.scrollToBottom(), 0);  // Ensure scroll happens after UI update
    }
  }

  private scrollToBottom() {
    if (this.chatContainer) {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    }
  }
}
