import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

// Phase 3.8: withCredentials sends httpOnly cookies cross-origin
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

// Refresh queue - prevents multiple simultaneous 401 refresh calls
let isRefreshing = false;
type QueueEntry = { resolve: () => void; reject: (err: unknown) => void };
let failedQueue: QueueEntry[] = [];

const processQueue = (error: unknown): void => {
  failedQueue.forEach(({ resolve, reject }) => (error ? reject(error) : resolve()));
  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise<void>((resolve, reject) => { failedQueue.push({ resolve, reject }); })
          .then(() => apiClient(originalRequest));
      }
      originalRequest._retry = true;
      isRefreshing = true;
      try {
        await apiClient.post('/auth/refresh');
        processQueue(null);
        return apiClient(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError);
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally { isRefreshing = false; }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
