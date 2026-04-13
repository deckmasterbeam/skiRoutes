export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? (import.meta.env.DEV ? 'http://localhost:5000' : '');

export const SAVE_USER_URL = `${API_BASE_URL}/api/save_user`;
