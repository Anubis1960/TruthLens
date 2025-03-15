import { Component } from '@angular/core';
import { User } from '../../models/user-model';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar'; 
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
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
  
    constructor(private authService: AuthService, private router: Router, private snackbar: MatSnackBar) {
      this.email = '';
      this.password = '';
    }
    onRegister(): void {
      this.authService.register(this.email, this.password).subscribe({
        next: () => {
          console.log("Registered successfully.");
          this.snackbar.open('Registration successful', undefined, {
            duration: 2000,
          });
          this.email = '';
          this.password = '';
        },
        error: (err) => {
          const errorMessage = err.error?.error || 'Invalid email or password';
          this.snackbar.open(errorMessage, undefined, {
            duration: 2000,
          });
          console.log("Failed to register:", errorMessage);
        }
      });
    }    
}
