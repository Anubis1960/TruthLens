import { inject } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivateFn, Router, RouterStateSnapshot } from '@angular/router';

export const canActivate: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
  const router = inject(Router);
  
  if (typeof sessionStorage !== 'undefined') {
    const user = JSON.parse(sessionStorage.getItem("user") || '{}');
    console.log("User from sessionStorage: ", user);  // Debugging line to check the user object

    return user?.user_data ? true : router.createUrlTree(['/login']);
  } else {
    return router.createUrlTree(['/login']);
  }
};
