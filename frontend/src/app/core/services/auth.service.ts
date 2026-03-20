import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { catchError, finalize, map, Observable, of, shareReplay, switchMap, tap, throwError } from 'rxjs';

import { apiConfig } from './api.config';
import { AuthTokens, CurrentUser } from '../models/api.models';

type RefreshTokenResponse = Pick<AuthTokens, 'access'> & Partial<Pick<AuthTokens, 'refresh'>>;

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly currentUserState = signal<CurrentUser | null>(null);
  private readonly accessTokenState = signal<string | null>(localStorage.getItem(apiConfig.accessTokenStorageKey));
  private readonly refreshTokenState = signal<string | null>(localStorage.getItem(apiConfig.refreshTokenStorageKey));
  private readonly activeTenantSlugState = signal<string | null>(localStorage.getItem(apiConfig.tenantSlugStorageKey));
  private refreshRequest$: Observable<string | null> | null = null;

  readonly currentUser = computed(() => this.currentUserState());
  readonly isAuthenticated = computed(() => Boolean(this.accessTokenState()));
  readonly activeTenantSlug = computed(() => this.activeTenantSlugState());

  private decodeJwtPayload(token: string): Record<string, unknown> | null {
    try {
      const payload = token.split('.')[1];
      if (!payload) {
        return null;
      }

      const normalizedPayload = payload.replace(/-/g, '+').replace(/_/g, '/');
      const paddedPayload = normalizedPayload.padEnd(Math.ceil(normalizedPayload.length / 4) * 4, '=');
      const decodedPayload = atob(paddedPayload);
      return JSON.parse(decodedPayload) as Record<string, unknown>;
    } catch {
      return null;
    }
  }

  private tokenIsValid(token: string | null) {
    if (!token) {
      return false;
    }

    const payload = this.decodeJwtPayload(token);
    if (!payload) {
      return false;
    }

    const exp = payload['exp'];
    if (typeof exp !== 'number') {
      return false;
    }

    const nowInSeconds = Math.floor(Date.now() / 1000);
    return exp > nowInSeconds;
  }

  login(email: string, password: string) {
    return this.http.post<AuthTokens>(`${apiConfig.baseUrl}/auth/login`, { email, password }).pipe(
      tap((tokens: AuthTokens) => {
        localStorage.setItem(apiConfig.accessTokenStorageKey, tokens.access);
        localStorage.setItem(apiConfig.refreshTokenStorageKey, tokens.refresh);
        this.accessTokenState.set(tokens.access);
        this.refreshTokenState.set(tokens.refresh);
      }),
    );
  }

  loadCurrentUser() {
    return this.http.get<CurrentUser>(`${apiConfig.baseUrl}/auth/me`).pipe(
      tap((user: CurrentUser) => {
        this.currentUserState.set(user);
        if (!this.activeTenantSlugState() && user.memberships.length > 0) {
          this.setActiveTenant(user.memberships[0].tenant_slug);
        }
      }),
    );
  }

  setActiveTenant(tenantSlug: string) {
    localStorage.setItem(apiConfig.tenantSlugStorageKey, tenantSlug);
    this.activeTenantSlugState.set(tenantSlug);
  }

  hasSession() {
    return Boolean(this.accessTokenState() || this.refreshTokenState());
  }

  hasUsableSession() {
    if (this.tokenIsValid(this.accessTokenState())) {
      return true;
    }

    return this.tokenIsValid(this.refreshTokenState());
  }

  accessToken() {
    return this.accessTokenState();
  }

  refreshToken() {
    return this.refreshTokenState();
  }

  refreshSession() {
    const refreshToken = this.refreshTokenState();

    if (!refreshToken) {
      this.logout();
      return of(null);
    }

    if (!this.refreshRequest$) {
      this.refreshRequest$ = this.http
        .post<RefreshTokenResponse>(`${apiConfig.baseUrl}/auth/refresh`, { refresh: refreshToken })
        .pipe(
          tap((tokens) => {
            localStorage.setItem(apiConfig.accessTokenStorageKey, tokens.access);
            this.accessTokenState.set(tokens.access);

            if (tokens.refresh) {
              localStorage.setItem(apiConfig.refreshTokenStorageKey, tokens.refresh);
              this.refreshTokenState.set(tokens.refresh);
            }
          }),
          map((tokens) => tokens.access),
          catchError((error) => {
            this.logout();
            return throwError(() => error);
          }),
          finalize(() => {
            this.refreshRequest$ = null;
          }),
          shareReplay(1),
        );
    }

    return this.refreshRequest$;
  }

  restoreSession() {
    if (!this.hasUsableSession()) {
      return of(null);
    }

    return this.loadCurrentUser().pipe(
      map((user) => user),
      catchError(() => {
        if (!this.refreshTokenState()) {
          this.logout();
          return of(null);
        }

        return this.refreshSession().pipe(
          switchMap((accessToken) => {
            if (!accessToken) {
              return of(null);
            }

            return this.loadCurrentUser();
          }),
          catchError(() => {
            this.logout();
            return of(null);
          }),
        );
      }),
    );
  }

  logout() {
    localStorage.removeItem(apiConfig.accessTokenStorageKey);
    localStorage.removeItem(apiConfig.refreshTokenStorageKey);
    localStorage.removeItem(apiConfig.tenantSlugStorageKey);
    this.accessTokenState.set(null);
    this.refreshTokenState.set(null);
    this.activeTenantSlugState.set(null);
    this.currentUserState.set(null);
  }
}