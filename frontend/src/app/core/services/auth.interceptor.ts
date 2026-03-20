import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';

import { AuthService } from './auth.service';

function shouldSkipRefresh(url: string) {
  return url.includes('/auth/login') || url.includes('/auth/refresh');
}

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService);
  const headers: Record<string, string> = {};
  const token = authService.accessToken();
  const tenantSlug = authService.activeTenantSlug();

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (tenantSlug) {
    headers['X-Tenant-Slug'] = tenantSlug;
  }

  const authenticatedRequest = Object.keys(headers).length > 0 ? request.clone({ setHeaders: headers }) : request;

  return next(authenticatedRequest).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status !== 401 || shouldSkipRefresh(request.url) || !authService.refreshToken()) {
        return throwError(() => error);
      }

      return authService.refreshSession().pipe(
        switchMap((accessToken) => {
          if (!accessToken) {
            return throwError(() => error);
          }

          return next(
            request.clone({
              setHeaders: {
                ...(tenantSlug ? { 'X-Tenant-Slug': tenantSlug } : {}),
                Authorization: `Bearer ${accessToken}`,
              },
            }),
          );
        }),
        catchError((refreshError) => throwError(() => refreshError)),
      );
    }),
  );
};