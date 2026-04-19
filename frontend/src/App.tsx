import { useAuth0 } from "@auth0/auth0-react";
import { useSyncUserToBackend } from "./hooks/useSyncUserToBackend";
import "./App.css";
import { RoutesPage } from "./routesPage";

function App() {
  const {
    isLoading,
    isAuthenticated,
    error,
    loginWithRedirect: login,
    logout: auth0Logout,
    user,
  } = useAuth0();

  useSyncUserToBackend();

  const handleSignup = () => {
    login({ authorizationParams: { screen_hint: "signup" } });
  };

  const handleLogout = () => {
    auth0Logout({ logoutParams: { returnTo: window.location.origin } });
  };

  const handleLogin = () => {
    login();
  };

  if (isLoading) return "Loading...";

  return (
    <>
      {isAuthenticated ? (
        <>
          <p>Logged in as {user?.email}</p>
          <h1>User Profile</h1>
          <pre>{JSON.stringify(user, null, 2)}</pre>
          <button onClick={handleLogout}>Logout</button>
        </>
      ) : (
        <>
          {error && <p>Error: {error.message}</p>}
          <button onClick={handleSignup}>Signup</button>
          <button onClick={handleLogin}>Login</button>
        </>
      )}
      <RoutesPage />
    </>
  );
}

export default App;
