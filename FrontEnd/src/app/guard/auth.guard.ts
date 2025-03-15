import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';

export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  if(typeof sessionStorage !== 'undefined'){
    const user = JSON.parse(sessionStorage.getItem("user") || '{}');
    return user.user_data !== undefined ? true : inject(Router).createUrlTree(['/login'])
  }else{
    return inject(Router).createUrlTree(['/login']);
  }
};
