import { UrlTree } from '@angular/router';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { authGuard, guestGuard } from './auth.guards';
import { AuthService } from '../services/auth.service';

describe('auth guards', () => {
  let hasUsableSession = true;

  beforeEach(() => {
    hasUsableSession = true;

    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        {
          provide: AuthService,
          useValue: {
            hasUsableSession: () => hasUsableSession,
          },
        },
      ],
    });
  });

  it('allows authenticated users in authGuard', () => {
    hasUsableSession = true;

    const result = TestBed.runInInjectionContext(() => authGuard({} as never, {} as never));

    expect(result).toBeTrue();
  });

  it('redirects unauthenticated users in authGuard', () => {
    hasUsableSession = false;

    const result = TestBed.runInInjectionContext(() => authGuard({} as never, {} as never));

    expect(result instanceof UrlTree).toBeTrue();
    expect((result as UrlTree).toString()).toBe('/login');
  });

  it('redirects authenticated users away from guestGuard', () => {
    hasUsableSession = true;

    const result = TestBed.runInInjectionContext(() => guestGuard({} as never, {} as never));

    expect(result instanceof UrlTree).toBeTrue();
    expect((result as UrlTree).toString()).toBe('/dashboard');
  });

  it('allows guests in guestGuard', () => {
    hasUsableSession = false;

    const result = TestBed.runInInjectionContext(() => guestGuard({} as never, {} as never));

    expect(result).toBeTrue();
  });
});
