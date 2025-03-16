import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/user-model';
import { MatSnackBar } from '@angular/material/snack-bar';
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

  constructor(private authService: AuthService, private router: Router, private snackbar: MatSnackBar) {
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
        this.router.navigateByUrl('/verify');
      },
      error: (err) => {
        const errorMessage = err.error?.error || 'Invalid email or password';
        this.snackbar.open(errorMessage, undefined, {
          duration: 2000,
        });
        console.log("Failed to register:", errorMessage);
        console.log("Failed to log in.");
      }
    })
  }
  
  loginWithGoogle():void{
    console.log("Google Auth selected...");
    window.location.href = 'http://localhost:5000/login';
  }
}
