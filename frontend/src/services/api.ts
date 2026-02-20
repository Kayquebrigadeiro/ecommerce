import axios, { AxiosInstance, AxiosError } from 'axios';
import type { Product, Cart, Order, Payment, User, AuthTokens } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para adicionar token
    this.api.interceptors.request.use((config) => {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
      }
      return config;
    });

    // Interceptor para renovar token
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
              const response = await axios.post(`${API_URL}/api/token/refresh/`, {
                refresh: refreshToken,
              });
              const { access } = response.data;
              localStorage.setItem('access_token', access);
              originalRequest.headers.Authorization = `Bearer ${access}`;
              return this.api(originalRequest);
            }
          } catch (refreshError) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Auth
  async login(username: string, password: string): Promise<AuthTokens> {
    const { data } = await this.api.post<AuthTokens>('/api/token/', { username, password });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  }

  async register(username: string, email: string, password: string, password2: string) {
    const { data } = await this.api.post('/api/register/', { username, email, password, password2 });
    return data;
  }

  async logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      await this.api.post('/api/logout/', { refresh: refreshToken });
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  async getMe(): Promise<User> {
    const { data } = await this.api.get<User>('/api/usuarios/me/');
    return data;
  }

  // Products
  async getProducts(): Promise<Product[]> {
    const { data } = await this.api.get<Product[]>('/api/produtos/');
    return data;
  }

  async getProduct(id: number): Promise<Product> {
    const { data } = await this.api.get<Product>(`/api/produtos/${id}/`);
    return data;
  }

  async getFeaturedProducts(): Promise<Product[]> {
    const { data } = await this.api.get<Product[]>('/api/produtos/?featured=true');
    return data.slice(0, 6); // Primeiros 6 como featured
  }

  // Cart
  async getCart(): Promise<Cart> {
    const { data } = await this.api.get<Cart>('/api/carrinho/');
    return data;
  }

  async addToCart(produto_id: number, quantidade: number = 1): Promise<Cart> {
    const { data } = await this.api.post<Cart>('/api/carrinho/adicionar/', {
      produto_id,
      quantidade,
    });
    return data;
  }

  async updateCartItem(item_id: number, quantidade: number): Promise<Cart> {
    const { data } = await this.api.patch<Cart>(`/api/carrinho/atualizar/${item_id}/`, {
      quantidade,
    });
    return data;
  }

  async removeCartItem(item_id: number): Promise<Cart> {
    const { data } = await this.api.delete<Cart>(`/api/carrinho/remover/${item_id}/`);
    return data;
  }

  async clearCart(): Promise<Cart> {
    const { data } = await this.api.delete<Cart>('/api/carrinho/limpar/');
    return data;
  }

  // Orders
  async getOrders(): Promise<Order[]> {
    const { data } = await this.api.get<Order[]>('/api/pedidos/');
    return data;
  }

  async getOrder(id: number): Promise<Order> {
    const { data } = await this.api.get<Order>(`/api/pedidos/${id}/`);
    return data;
  }

  async createOrderFromCart(): Promise<Order> {
    const { data } = await this.api.post<Order>('/api/pedidos/criar_do_carrinho/');
    return data;
  }

  // Payments
  async createPayment(pedido_id: number, metodo: string): Promise<Payment> {
    const { data } = await this.api.post<Payment>('/api/pagamentos/', {
      pedido_id,
      metodo,
    });
    return data;
  }

  async getPayments(): Promise<Payment[]> {
    const { data } = await this.api.get<Payment[]>('/api/pagamentos/');
    return data;
  }

  async getPaymentHistory(): Promise<Payment[]> {
    const { data } = await this.api.get<Payment[]>('/api/pagamentos/historico/');
    return data;
  }
}

export const api = new ApiService();
