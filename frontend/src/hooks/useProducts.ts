import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';
import type { Product } from '@/types';

export function useProducts() {
  return useQuery({
    queryKey: ['products'],
    queryFn: () => api.getProducts(),
  });
}

export function useProduct(id: number) {
  return useQuery({
    queryKey: ['product', id],
    queryFn: () => api.getProduct(id),
    enabled: !!id,
  });
}

export function useFeaturedProducts() {
  return useQuery({
    queryKey: ['products', 'featured'],
    queryFn: () => api.getFeaturedProducts(),
  });
}
