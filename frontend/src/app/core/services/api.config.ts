import { getRuntimeConfig } from './runtime-config';

const runtimeConfig = getRuntimeConfig();

export const apiConfig = {
  baseUrl: runtimeConfig.apiBaseUrl ?? '/api/v1',
  tenantSlugStorageKey: 'orderflow.tenant-slug',
  accessTokenStorageKey: 'orderflow.access-token',
  refreshTokenStorageKey: 'orderflow.refresh-token',
};