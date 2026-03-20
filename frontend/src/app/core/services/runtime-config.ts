type OrderFlowRuntimeConfig = {
  apiBaseUrl?: string;
};

declare global {
  interface Window {
    __ORDERFLOW_CONFIG__?: OrderFlowRuntimeConfig;
  }
}

export function getRuntimeConfig(): OrderFlowRuntimeConfig {
  return window.__ORDERFLOW_CONFIG__ ?? {};
}