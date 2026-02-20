import { create } from 'zustand';
import type { User, Cart, Product } from '@/types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  logout: () => set({ user: null, isAuthenticated: false }),
}));

interface CartState {
  cart: Cart | null;
  isCartOpen: boolean;
  setCart: (cart: Cart | null) => void;
  openCart: () => void;
  closeCart: () => void;
  toggleCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  cart: null,
  isCartOpen: false,
  setCart: (cart) => set({ cart }),
  openCart: () => set({ isCartOpen: true }),
  closeCart: () => set({ isCartOpen: false }),
  toggleCart: () => set((state) => ({ isCartOpen: !state.isCartOpen })),
}));

interface WishlistState {
  wishlist: Product[];
  addToWishlist: (product: Product) => void;
  removeFromWishlist: (productId: number) => void;
  isInWishlist: (productId: number) => boolean;
}

export const useWishlistStore = create<WishlistState>((set, get) => ({
  wishlist: [],
  addToWishlist: (product) =>
    set((state) => ({
      wishlist: [...state.wishlist, product],
    })),
  removeFromWishlist: (productId) =>
    set((state) => ({
      wishlist: state.wishlist.filter((p) => p.id !== productId),
    })),
  isInWishlist: (productId) => get().wishlist.some((p) => p.id === productId),
}));

interface UIState {
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading }),
}));
