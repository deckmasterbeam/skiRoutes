import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { Auth0Provider } from '@auth0/auth0-react'
import { AUTH0_AUTHORIZATION_PARAMS, AUTH0_CLIENT_ID, AUTH0_DOMAIN } from './config/auth'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Auth0Provider
      domain={AUTH0_DOMAIN}
      clientId={AUTH0_CLIENT_ID}
      authorizationParams={AUTH0_AUTHORIZATION_PARAMS}
    >
      <App />
    </Auth0Provider>
  </StrictMode>
)
