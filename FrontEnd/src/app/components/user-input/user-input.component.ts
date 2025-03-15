import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-user-input',
  standalone: false,
  templateUrl: './user-input.component.html',
  styleUrl: './user-input.component.css'
})
export class UserInputComponent {
  @Output() sendMessageEmitter = new EventEmitter<string>()
  message: string = ""

  sendMessage(){
    this.sendMessageEmitter.emit(this.message);
    this.message = '';
  }
}
