const DEFAULT_AUTH0_DOMAIN = 'dev-4h501vphbrckh25y.us.auth0.com';
const DEFAULT_AUTH0_CLIENT_ID = '0Ia83ATbBrZn968GR3lIW2CHcH2eIU5T';
const DEFAULT_AUTH0_AUDIENCE = 'https://ski-routes-api';

export const AUTH0_DOMAIN = import.meta.env.VITE_AUTH0_DOMAIN ?? DEFAULT_AUTH0_DOMAIN;
export const AUTH0_CLIENT_ID = import.meta.env.VITE_AUTH0_CLIENT_ID ?? DEFAULT_AUTH0_CLIENT_ID;
export const AUTH0_AUDIENCE = import.meta.env.VITE_AUTH0_AUDIENCE ?? DEFAULT_AUTH0_AUDIENCE;

export const AUTH0_AUTHORIZATION_PARAMS = {
  redirect_uri: window.location.origin,
  ...(AUTH0_AUDIENCE ? { audience: AUTH0_AUDIENCE } : {}),
};