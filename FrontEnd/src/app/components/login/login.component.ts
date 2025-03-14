import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/user-model';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email:string;
  password: string;
  user: User | undefined;

  constructor(private authService: AuthService,
    private router: Router) {
    this.email = '';
    this.password = '';
  }

  onLogin():void{
    // TODO
  }
  loginWithGoogle():void{
    // TODO
  }
}
