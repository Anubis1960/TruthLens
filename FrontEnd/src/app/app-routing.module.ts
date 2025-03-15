import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { DomainTableComponent } from './components/domain-table/domain-table.component';
import { canActivate } from './guard/auth.guard';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo:'/login',pathMatch:'full'}, 
  { path: 'domain', component: DomainTableComponent, /*canActivate: [canActivate] */},
  { path: 'home', component: HomeComponent, /*canActivate: [canActivate]*/ },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
