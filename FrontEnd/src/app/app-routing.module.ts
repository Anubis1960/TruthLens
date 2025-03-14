import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { DomainTableComponent } from './components/domain-table/domain-table.component';
const routes: Routes = [
  {path:'' , component: LoginComponent},
  {path:'home' , component: HomeComponent},
  {path: 'domain', component: DomainTableComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
