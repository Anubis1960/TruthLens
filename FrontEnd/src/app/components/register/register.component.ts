import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
@Component({
  selector: 'app-register',
  standalone: false,
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  email:string;
    password: string;
    user: User | undefined;
  
    constructor(private service: AuthService, private router: Router) {
      this.email = '';
      this.password = '';
    }
}
