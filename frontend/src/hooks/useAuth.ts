import { useMutation, useQuery } from '@tanstack/react-query';
import { api } from '@/services/api';
import { useAuthStore } from '@/store';
import { useRouter } from 'next/navigation';
import { toast } from '@/hooks/useToast';

export function useAuth() {
  const router = useRouter();
  const { user, setUser, logout: logoutStore } = useAuthStore();

  const loginMutation = useMutation({
    mutationFn: ({ username, password }: { username: string; password: string }) =>
      api.login(username, password),
    onSuccess: async () => {
      const userData = await api.getMe();
      setUser(userData);
      toast.success('Login realizado com sucesso!');
      router.push('/');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Erro ao fazer login');
    },
  });

  const registerMutation = useMutation({
    mutationFn: ({
      username,
      email,
      password,
      password2,
    }: {
      username: string;
      email: string;
      password: string;
      password2: string;
    }) => api.register(username, email, password, password2),
    onSuccess: () => {
      toast.success('Conta criada! Faça login para continuar.');
      router.push('/login');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Erro ao criar conta');
    },
  });

  const logout = async () => {
    try {
      await api.logout();
      logoutStore();
      router.push('/login');
      toast.success('Logout realizado');
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  };

  return {
    user,
    isAuthenticated: !!user,
    login: loginMutation.mutate,
    register: registerMutation.mutate,
    logout,
    isLoading: loginMutation.isPending || registerMutation.isPending,
  };
}
