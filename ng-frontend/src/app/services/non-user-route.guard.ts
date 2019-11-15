import { Injectable } from '@angular/core';
import { 
    Router,
    CanActivate,
    ActivatedRouteSnapshot,
    RouterStateSnapshot
} from '@angular/router';

import { AuthService } from './auth.service';

@Injectable()
export class NonUserRouteGuard implements CanActivate {
    constructor(
        private authService: AuthService,
        private router: Router
    ) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        if (this.authService.currentUserValue == null) {
            return true;
        } else {
            this.router.navigate(['/']);
            return false;
        }
    }
}