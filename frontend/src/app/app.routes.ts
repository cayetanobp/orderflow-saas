import { Routes } from '@angular/router';

import { authGuard, guestGuard } from './core/guards/auth.guards';
import { CustomersPageComponent } from './features/customers/customers-page.component';
import { DashboardPageComponent } from './features/dashboard/dashboard-page.component';
import { LoginPageComponent } from './features/login/login-page.component';
import { OrdersPageComponent } from './features/orders/orders-page.component';

export const appRoutes: Routes = [
  { path: 'login', component: LoginPageComponent, canActivate: [guestGuard] },
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  { path: 'dashboard', component: DashboardPageComponent, canActivate: [authGuard] },
  { path: 'customers', component: CustomersPageComponent, canActivate: [authGuard] },
  { path: 'orders', component: OrdersPageComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: 'dashboard' },
];