import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { catchError, finalize, map, of, switchMap } from 'rxjs';

import { AuthService } from '../../core/services/auth.service';

@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.css',
})
export class LoginPageComponent {
  private readonly formBuilder = inject(FormBuilder);
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  readonly form = this.formBuilder.group({
    email: ['owner@example.com', [Validators.required, Validators.email]],
    password: ['change-me', [Validators.required]],
  });

  loading = false;
  errorMessage = '';
  successMessage = '';

  private readonly profileLoadFailed = 'profile-load-failed';

  submit() {
    if (this.form.invalid) {
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const rawValue = this.form.getRawValue();
    this.authService
      .login(rawValue.email ?? '', rawValue.password ?? '')
      .pipe(
        switchMap(() =>
          this.authService.loadCurrentUser().pipe(
            map(() => 'ok'),
            catchError(() => of(this.profileLoadFailed)),
          ),
        ),
        finalize(() => {
          this.loading = false;
        }),
      )
      .subscribe({
        next: (result) => {
          if (result === this.profileLoadFailed) {
            this.errorMessage = 'Session started, but the profile could not be loaded.';
            return;
          }

          this.successMessage = 'Session started successfully.';
          void this.router.navigate(['/dashboard']);
        },
        error: () => {
          this.errorMessage = 'Authentication failed. Verify the backend is running and the credentials exist.';
        },
      });
  }
}