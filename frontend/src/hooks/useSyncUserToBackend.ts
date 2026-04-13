import { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { SAVE_USER_URL } from '../config/api';
import { AUTH0_AUDIENCE } from '../config/auth';

export function useSyncUserToBackend() {
  const [userLogged, setUserLogged] = useState(false);
  const { getAccessTokenSilently, isAuthenticated, user, isLoading } = useAuth0();

  useEffect(() => {
    if (isAuthenticated && user && !isLoading && !userLogged) {
      if (!user.sub) {
        console.warn('Skipping /api/save_user because Auth0 user has no sub claim.');
        return;
      }

      const payload = {
        sub: user.sub,
        email: user.email ?? null,
        name: user.name ?? null,
      };

      const syncUser = async () => {
        try {
          const accessToken = await getAccessTokenSilently(
            AUTH0_AUDIENCE
              ? { authorizationParams: { audience: AUTH0_AUDIENCE } }
              : undefined,
          );

          const response = await fetch(SAVE_USER_URL, {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          });

          if (!response.ok) {
            const errorBody = await response.text();
            console.error('Failed to save user to backend:', response.status, errorBody);
            return;
          }

          setUserLogged(true);
        } catch (error) {
          console.error('Failed to reach backend /api/save_user:', error);
        }
      };

      void syncUser();
    }
  }, [getAccessTokenSilently, isAuthenticated, user, isLoading, userLogged]);
}
