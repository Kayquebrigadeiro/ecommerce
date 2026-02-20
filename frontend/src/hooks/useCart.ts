import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';
import { useCartStore } from '@/store';
import { toast } from '@/hooks/useToast';

export function useCart() {
  const queryClient = useQueryClient();
  const { setCart, openCart } = useCartStore();

  const cartQuery = useQuery({
    queryKey: ['cart'],
    queryFn: async () => {
      const cart = await api.getCart();
      setCart(cart);
      return cart;
    },
  });

  const addToCartMutation = useMutation({
    mutationFn: ({ produto_id, quantidade }: { produto_id: number; quantidade: number }) =>
      api.addToCart(produto_id, quantidade),
    onSuccess: (data) => {
      queryClient.setQueryData(['cart'], data);
      setCart(data);
      openCart();
      toast.success('Produto adicionado ao carrinho!');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Erro ao adicionar produto');
    },
  });

  const updateItemMutation = useMutation({
    mutationFn: ({ item_id, quantidade }: { item_id: number; quantidade: number }) =>
      api.updateCartItem(item_id, quantidade),
    onSuccess: (data) => {
      queryClient.setQueryData(['cart'], data);
      setCart(data);
    },
  });

  const removeItemMutation = useMutation({
    mutationFn: (item_id: number) => api.removeCartItem(item_id),
    onSuccess: (data) => {
      queryClient.setQueryData(['cart'], data);
      setCart(data);
      toast.success('Produto removido');
    },
  });

  const clearCartMutation = useMutation({
    mutationFn: () => api.clearCart(),
    onSuccess: (data) => {
      queryClient.setQueryData(['cart'], data);
      setCart(data);
    },
  });

  return {
    cart: cartQuery.data,
    isLoading: cartQuery.isLoading,
    addToCart: addToCartMutation.mutate,
    updateItem: updateItemMutation.mutate,
    removeItem: removeItemMutation.mutate,
    clearCart: clearCartMutation.mutate,
  };
}
