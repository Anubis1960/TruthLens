import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { DomainTableComponent } from './components/domain-table/domain-table.component';
import { canActivate } from './guard/auth.guard';
import { RegisterComponent } from './components/register/register.component';
import { CallbackComponent } from './components/callback/callback.component';
import { VerifyLinkComponent } from './components/verify-link/verify-link.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo:'/login',pathMatch:'full'},
  { path: 'auth/callback', component: CallbackComponent},
  { path: 'register', component: RegisterComponent},
  { path: 'domain', component: DomainTableComponent, /*canActivate: [canActivate] */},
  { path: 'home', component: HomeComponent, /*canActivate: [canActivate]*/ },
  { path: 'verify', component: VerifyLinkComponent, /*canActivate: [canActivate]*/ },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
