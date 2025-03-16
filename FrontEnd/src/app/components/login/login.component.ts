import { Component } from '@angular/core';
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
    console.log(this.email, "email to send")
    console.log(this.password, "password to send")
    this.authService.login(this.email,this.password).subscribe({
      next: (data: User)=>{
        this.user = data;
        sessionStorage.setItem("user",JSON.stringify(this.user));
        this.router.navigateByUrl('/home');
      },
      error: () => {
        console.log("Failed to log in.");
      }
    })
  }
  
  loginWithGoogle():void{
    console.log("Google Auth selected...");
    window.location.href = 'http://localhost:5000/login';
  }
}
