import { ApplicationConfig, inject, provideAppInitializer } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { firstValueFrom } from 'rxjs';

import { appRoutes } from './app.routes';
import { authInterceptor } from './core/services/auth.interceptor';
import { AuthService } from './core/services/auth.service';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(appRoutes),
    provideAppInitializer(() => firstValueFrom(inject(AuthService).restoreSession())),
    provideHttpClient(withInterceptors([authInterceptor])),
  ],
};