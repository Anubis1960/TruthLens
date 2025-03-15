import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

const BASE_URL = 'http://localhost:5000';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private web_socket: Socket
  constructor() {
    this.web_socket = new Socket({
      url: BASE_URL,
      options:{},
    });
   }
   
   // this method is used to start connection/handhshake of socket with server
  connectSocket(message:any) {
    this.web_socket.emit('connect', message);
  }

  // this method is used to get response from server
  receiveStatus() {
    return this.web_socket.fromEvent('/get-response');
  }

  // this method is used to end web socket connection
  disconnectSocket() {
    this.web_socket.disconnect();
 }
}
